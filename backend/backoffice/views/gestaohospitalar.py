from django.utils import timezone
from django.db import transaction
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import OpenApiExample, extend_schema
from backend.backoffice.serializers.gestaohospitalar import InternarPacienteSerializer, LiberarPacienteSerializer
from backend.backoffice.models.gestaohospitalar import (
    Ala,
    Leito,
    LogOcupacaoLeito
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
            description="Realiza a internação de um paciente em um leito"
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
            description="Realiza a liberação de um paciente em um leito"
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


'''
LOG LEITOS
- Médicos podem internar pacientes, e liberar leitos
- Administradores não podem internar nem liberar leitos
- Pacientes podem ver apenas seus próprios leitos ocupado
'''
class LogOcupacaoLeitoViewSet(ModelViewSet):
    queryset = LogOcupacaoLeito.objects.all()
    serializer_class = LogOcupacaoLeitoSerializer
    permission_classes = [IsAuthenticated]
