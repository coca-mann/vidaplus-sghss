from django.utils import timezone
from django.db import transaction
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from backend.backoffice.serializers.gestaohospitalar import InternarPacienteSerializer, LiberarPacienteSerializer, AtualizarStatusSerializer
from backend.backoffice.models.gestaohospitalar import (
    Ala,
    Leito,
    LogOcupacaoLeito,
    STATUS_LEITO
)
from backend.backoffice.serializers.gestaohospitalar import (
    AlaSerializer,
    LeitoSerializer,
    LogOcupacaoLeitoSerializer
)
from backend.backoffice.permissions import AlaPermission
from backend.pessoa.models.core import Administrador
from backend.pessoa.models.saude import ProfissionalSaude
from backend.local.models import Local
from backend.pessoa.models.paciente import Paciente


'''
ALA
- Somente administradores podem editar alas
- Médicos podem ver alas com leitos ocupados
- Pacientes não podem ver alas
'''
@extend_schema(tags=['Gestão hospitalar'])
@extend_schema_view(
    list=extend_schema(
        description="Lista todas as alas disponíveis conforme as permissões do usuário.",
        summary="Listar alas"
    ),
    retrieve=extend_schema(
        description="Recupera detalhes de uma ala específica.",
        summary="Detalhar ala"
    ),
    create=extend_schema(
        description="Cria uma nova ala (apenas administradores).",
        summary="Criar ala"
    ),
    update=extend_schema(
        description="Atualiza uma ala existente (apenas administradores).",
        summary="Atualizar ala"
    ),
    partial_update=extend_schema(
        description="Atualiza parcialmente uma ala (apenas administradores).",
        summary="Atualizar parcialmente ala"
    ),
    destroy=extend_schema(
        description="Remove uma ala (apenas administradores).",
        summary="Remover ala"
    ),
)
class AlaViewSet(ModelViewSet):
    serializer_class = AlaSerializer
    permission_classes = [IsAuthenticated, AlaPermission]

    def get_queryset(self):
        user = self.request.user

        if Administrador.objects.filter(idUsuario=user).exists():
            return Ala.objects.all()
        
        if ProfissionalSaude.objects.filter(idUsuario=user).exists():
            alas_com_leitos_ocupados = Leito.objects.filter(status='OCUP').values_list('idAla', flat=True).distinct()

            return Ala.objects.filter(idAla__in=alas_com_leitos_ocupados)
        
        return Ala.objects.none()


'''
LEITOS
- Somente administradores podem editar leitos
- Médicos podem ver detalhes dos pacientes nos leitos
'''
@extend_schema(tags=['Gestão hospitalar'])
@extend_schema_view(
    list=extend_schema(
        description="Lista todos os leitos do hospital.",
        summary="Listar leitos"
    ),
    retrieve=extend_schema(
        description="Recupera detalhes de um leito específico.",
        summary="Detalhar leito"
    ),
    create=extend_schema(
        description="Cria um novo leito (apenas administradores).",
        summary="Criar leito"
    ),
    update=extend_schema(
        description="Atualiza um leito existente (apenas administradores).",
        summary="Atualizar leito"
    ),
    partial_update=extend_schema(
        description="Atualiza parcialmente um leito.",
        summary="Atualizar parcialmente leito"
    ),
    destroy=extend_schema(
        description="Remove um leito (apenas administradores).",
        summary="Remover leito"
    ),
)
class LeitoViewSet(ModelViewSet):
    queryset = Leito.objects.all()
    serializer_class = LeitoSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):

        context = super().get_serializer_context()
        user = self.request.user

        context['mostrar_detalhes_paciente'] = (
            Administrador.objects.filter(idUsuario=user).exists() or
            ProfissionalSaude.objects.filter(idUsuario=user).exists()
        )

        return context
    
    @extend_schema(
            request=InternarPacienteSerializer,
            responses={200: LogOcupacaoLeitoSerializer},
            description="Realiza a internação de um paciente em um leito",
            summary="Internar um paciente em um leito"
    )

    @action(detail=True, methods=['post'], url_path='internar_paciente')
    def internar_paciente(self, request, pk=None):
        leito = self.get_object()

        if leito.status == 'OCUP':
            return Response(
                {'detail': 'Este leito já está ocupado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = request.user
        if not ProfissionalSaude.objects.filter(idUsuario=user).exists():
            return Response(
                {'detail': 'Apenas profissionais de saúde podem internar pacientes.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = InternarPacienteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data

        paciente = Paciente.objects.get(pk=validated_data['idPaciente'])
        local = Local.objects.get(pk=validated_data['idLocal'])
        profissional = ProfissionalSaude.objects.get(pk=validated_data['idProfissionalInternacao'])

        data_saida = validated_data.get('dataHoraSaida', None)

        with transaction.atomic():

            log_ocupacao = LogOcupacaoLeito.objects.create(
                idLocal=local,
                idPaciente=paciente,
                idLeito=leito,
                idProfissionalInternacao=profissional,
                dataHoraEntrada=validated_data['dataHoraEntrada'],
                dataHoraSaida=data_saida,
                motivoInternacao=validated_data['motivoInternacao'],
                observacao=validated_data.get('observacao', '')
            )

            leito.status = 'OCUP'
            leito.idPaciente = paciente
            leito.save()

        log_serializer = LogOcupacaoLeitoSerializer(log_ocupacao)
        return Response(log_serializer.data, status=status.HTTP_201_CREATED)
    
    @extend_schema(
            request=LiberarPacienteSerializer,
            responses={200: LogOcupacaoLeitoSerializer},
            description="Realiza a liberação de um paciente em um leito",
            summary="Liberar o paciente de um leito"
    )
    @action(detail=True, methods=['post'], url_path='liberar_paciente')
    def liberar_paciente(self, request, pk=None):
        leito = self.get_object()

        if leito.status != 'OCUP':
            return Response(
                {'detail': 'Este leito não está ocupado.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = request.user
        if not ProfissionalSaude.objects.filter(idUsuario=user).exists():
            return Response(
                {'detail': 'Apenas profissional de saúde podem liberar pacientes.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = LiberarPacienteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data

        profissional_liberacao = ProfissionalSaude.objects.get(pk=validated_data['idProfissionalLiberacao'])

        try:
            log_ocupacao = LogOcupacaoLeito.objects.filter(
                idLeito=leito,
                dataHoraSaida__isnull=True
            ).latest('dataHoraEntrada')
        except LogOcupacaoLeito.DoesNotExist:
            return Response(
                {'detail': 'Não foi encontrado registro de ocupação aberto para este leito.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        with transaction.atomic():
            log_ocupacao.idProfissionalLiberacao = profissional_liberacao
            log_ocupacao.dataHoraSaida = validated_data['dataHoraSaida']
            log_ocupacao.motivoLiberacao = validated_data['motivoLiberacao']

            if 'observacao' in validated_data:
                log_ocupacao.observacao = validated_data['observacao']

            log_ocupacao.save()

            leito.status = 'HIGI'
            leito.idPaciente = None
            leito.save()

        log_serializer = LogOcupacaoLeitoSerializer(log_ocupacao)
        return Response(log_serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
            request=AtualizarStatusSerializer,
            responses={200, LeitoSerializer},
            description="Atualiza o status de um leito que não está ocupado por um paciente.",
            summary='Atualizar status de um leito'
    )
    @action(detail=True, methods=['post'], url_path='atualizar_status')
    def atualizar_status(self, request, pk=None):
        leito = self.get_object()
        user = request.user
        
        if leito.idPaciente is not None:
            return Response(
                {'detail': 'Este leito está ocupado por um paciente e não pode mudar de status.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if 'status' not in request.data:
            return Response(
                {'detail': 'É necessário fornecer um status para atualização.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        novo_status = request.data['status']

        valid_statuses = [choice[0] for choice in STATUS_LEITO]
        if novo_status not in valid_statuses:
            return Response(
                {'detail': f'Status inválido. Opções válidas: {", ".join(valid_statuses)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if novo_status == 'OCUP':
            return Response(
                {'detail': 'Não é possível alterar o status para OCUP sem associar um paciente. Use a função internar_paciente.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        leito.status = novo_status
        leito.save()

        serializer = self.get_serializer(leito)
        return Response(serializer.data, status=status.HTTP_200_OK)


'''
LOG LEITOS
- Médicos podem internar pacientes, e liberar leitos
- Administradores não podem internar nem liberar leitos
- Pacientes podem ver apenas seus próprios leitos ocupado
'''
@extend_schema(tags=['Gestão hospitalar'])
@extend_schema_view(
    list=extend_schema(
        description='Lista todos os registros de ocupação de leitos acessíveis ao usuário.',
        summary='Listar logs de ocupação'
    ),
    retrieve=extend_schema(
        description='Recupera um registro específico de ocupação de leito.',
        summary='Detalhar log de ocupação'
    ),
)
class LogOcupacaoLeitoViewSet(ReadOnlyModelViewSet):
    serializer_class = LogOcupacaoLeitoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        try:
            paciente = Paciente.objects.filter(idUsuario=user)
            return LogOcupacaoLeito.objects.filter(idPaciente=paciente).select_related('idLocal', 'idLeito', 'idProfissionalInternacao', 'idProfissionalLiberacao')
        except Paciente.DoesNotExist:
            return Response(
                {'detail': 'Nenhum log de ocupação de leito encontrado para este paciente.'},
                status=status.HTTP_404_NOT_FOUND
            )
