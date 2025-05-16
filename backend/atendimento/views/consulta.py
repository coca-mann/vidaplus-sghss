from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
from drf_spectacular.utils import extend_schema, OpenApiExample, extend_schema_view
from backend.atendimento.models.consulta import Consulta
from backend.atendimento.models.exame import Exame
from backend.atendimento.models.consulta_exame import ConsultaExame
from backend.atendimento.serializers.consulta import ConsultaSerializer, ConsultaExamesSerializer
from backend.atendimento.serializers.medicamento import MedicamentoSerializer, RemoveMedicamentoSerializer
from backend.atendimento.serializers.exame import AddExameRequestSerializer
from backend.pessoa.models.saude import ProfissionalSaude
from backend.pessoa.models.paciente import Paciente

'''
CONSULTA
- Somente profissionais com realiza_consulta = True podem criar atendimentos
- Permitir atualizar informações sem perder dados
- Criar campos em medicamentosPrescritos: nome, dosagem, intervalo
- Criar campos em examesSolicitados: tipoExame, dataSolicitacao, dataRealizacao, resultadoExame, status
- Atualizar campos de exames conforme atualização no model Exame
'''
@extend_schema(
    tags=['Consultas'],
    description=(
        "API para gerenciamento de consultas. "
        "Apenas profissionais habilitados podem criar consultas. "
        "Inclui endpoints para medicamentos, exames, telemedicina e controle de status."
    )
)
@extend_schema_view(
    list=extend_schema(
        summary="Listar consultas",
        description="Lista todas as consultas que o usuário autenticado pode visualizar.",
        responses={200: ConsultaSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Detalhar consulta",
        description="Retorna os detalhes de uma consulta específica.",
        responses={200: ConsultaSerializer}
    ),
    create=extend_schema(
        summary="Criar consulta",
        description="Cria uma nova consulta para o profissional autenticado.",
        responses={201: ConsultaSerializer}
    ),
    update=extend_schema(
        summary="Atualizar consulta",
        description="Atualiza todos os dados de uma consulta existente.",
        responses={200: ConsultaSerializer}
    ),
    partial_update=extend_schema(
        summary="Atualização parcial de consulta",
        description="Atualiza parcialmente os dados de uma consulta.",
        responses={200: ConsultaSerializer}
    ),
    destroy=extend_schema(
        exclude=True  # Oculta do Swagger, conforme já está no seu código
    ),
)
class ConsultaViewSet(ModelViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer
    permission_classes = [IsAuthenticated]

    def check_permissions(self, request):
        super().check_permissions(request)
        
        if request.method == 'POST':
            user = request.user
            
            if user.is_staff:
                return
            
            try:
                profissional = ProfissionalSaude.objects.get(idUsuario=user)

                pode_criar_consulta = False
                for especialidade in profissional.especialidades.all():
                    if especialidade.realiza_consulta:
                        pode_criar_consulta = True
                        break
                
                if not pode_criar_consulta:
                    raise PermissionDenied("Você não tem permissão para criar consultas. Nenhuma de suas especialidades permite essa ação.")
                
                id_profissional_na_requisicao = request.data.get('idProfissional')
                if id_profissional_na_requisicao and int(id_profissional_na_requisicao) != profissional.idProfissional:
                    raise PermissionDenied("Você só pode criar consultas para você mesmo como profissional.")
                    
            except ProfissionalSaude.DoesNotExist:
                raise PermissionDenied("Apenas profissionais de saúde podem criar consultas.")
            
            except Exception as e:
                raise PermissionDenied(f"Erro ao verificar as permissões: {str(e)}")

    def perform_create(self, serializer):
        user = self.request.user
        
        if not user.is_staff:
            try:
                profissional = ProfissionalSaude.objects.get(idUsuario=user)
                serializer.validated_data['idProfissional'] = profissional
            except ProfissionalSaude.DoesNotExist:
                pass
        
        serializer.save()
            
    def get_queryset(self):
        queryset = Consulta.objects.all()
        user = self.request.user

        try:
            profissional = ProfissionalSaude.objects.get(idUsuario=user)
            return queryset.filter(idProfissional=profissional)
        except:
            pass

        try:
            paciente = Paciente.objects.get(idUsuario=user)
            return queryset.filter(idPaciente=paciente)
        except:
            pass

        if user.is_staff:
            return queryset
        
        return Consulta.objects.none()
    
    @extend_schema(exclude=True)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        summary="Listar consultas pendentes",
        description="Listar todas as consultas com status 'Agendada' para o usuário autenticado.",
        responses={200: ConsultaSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def consultas_pendentes(self, request):
        consultas = self.get_queryset().filter(status='AGEN')
        serializer = self.get_serializer(consultas, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Cancelar consulta",
        description="Cancelar a consulta informada e altera seu status para 'Cancelada'.",
        responses={200: ConsultaSerializer}
    )
    @action(detail=True, methods=['post'])
    def cancelar_consulta(self, request, pk=None):
        consulta = self.get_object()
        consulta.status = 'CANC'
        consulta.save()
        serializer = self.get_serializer(consulta)
        return Response(serializer.data)
    
    @extend_schema(
            description='Realiza a alteração do status da consulta para Realizada.',
            summary="Marcar a consulta como Realizada",
            responses={200: ConsultaSerializer},
    )
    @action(detail=True, methods=['post'])
    def realizar_consulta(self, request, pk=None):
        consulta = self.get_object()
        consulta.status = 'REAL'
        consulta.dataHoraAtendimento = datetime.now()
        consulta.save()
        serializer = self.get_serializer(consulta)
        return Response(serializer.data)
    
    @extend_schema(
        request=MedicamentoSerializer,
        responses={200: ConsultaSerializer},
        description="Adicionar um medicamento à consulta",
        summary="Adicionar medicamento às Medicações Prescritas",
        examples=[
            OpenApiExample(
                'Exemplo de adição de medicamento',
                value={
                    "nome": "Dipirona",
                    "dosagem": "500mg",
                    "intervalo": "8 horas",
                    "duracao": "5 dias",
                    "observacoes": "Tomar após as refeições"
                },
                request_only=True,
            )
        ]
    )
    @action(detail=True, methods=['post'])
    def add_medicamento(self, request, pk=None):
        consulta = self.get_object()
        medicamento = request.data.get('medicamento', {})
        
        user = request.user
        if not user.is_staff:
            try:
                profissional = ProfissionalSaude.objects.get(idUsuario=user)
                if consulta.idProfissional.idProfissional != profissional.idProfissional:
                    raise PermissionDenied("Você só pode modificar consultas que você mesmo criou.")
            except ProfissionalSaude.DoesNotExist:
                raise PermissionDenied("Apenas profissionais de saúde podem modificar consultas.")

        serializer = MedicamentoSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if consulta.medicamentoPrescrito is None:
            consulta.medicamentoPrescrito = []

        for i, med in enumerate(consulta.medicamentoPrescrito):
            if med.get('nome') == medicamento.get('nome'):
                consulta.medicamentoPrescrito[i] = medicamento
                consulta.save()
                return Response(self.get_serializer(consulta).data)
            
        consulta.medicamentoPrescrito.append(medicamento)
        consulta.save()
        
        return Response(self.get_serializer(consulta).data)

    @extend_schema(
        request=RemoveMedicamentoSerializer,
        responses={200: ConsultaSerializer},
        summary="Remover medicamento das Medicações Prescritas",
        description="Remove um medicamento da consulta",
        examples=[
            OpenApiExample(
                'Exemplo de remoção de medicamento',
                value={
                    "nome": "Dipirona"
                },
                request_only=True,
            )
        ]
    )
    @action(detail=True, methods=['post'])
    def remove_medicamento(self, request, pk=None):
        consulta = self.get_object()
        
        user = request.user
        if not user.is_staff:
            try:
                profissional = ProfissionalSaude.objects.get(idUsuario=user)
                if consulta.idProfissional.idProfissional != profissional.idProfissional:
                    raise PermissionDenied("Você só pode modificar consultas que você mesmo criou.")
            except ProfissionalSaude.DoesNotExist:
                raise PermissionDenied("Apenas profissionais de saúde podem modificar consultas.")
        
        serializer = RemoveMedicamentoSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        nome_medicamento = serializer.validated_data.get('nome')
        
        if consulta.medicamentoPrescrito is None:
            return Response(self.get_serializer(consulta).data)
        
        medicamento_encontrado = False
        for med in consulta.medicamentoPrescrito:
            if med.get('nome') == nome_medicamento:
                medicamento_encontrado = True
                break
        
        if not medicamento_encontrado:
            return Response(
                {"detail": f"Medicamento '{nome_medicamento}' não encontrado na consulta."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        consulta.medicamentoPrescrito = [
            med for med in consulta.medicamentoPrescrito
            if med.get('nome') != nome_medicamento
        ]
        
        consulta.save()
        return Response(self.get_serializer(consulta).data)
    
    @extend_schema(
            description='Listar os medicamentos de uma consulta.',
            summary="Listar todos os Medicamentos Prescritos",
            responses={200: ConsultaSerializer},
    )
    @action(detail=True, methods=['get'])
    def listar_medicamentos(self, request, pk=None):
        consulta = self.get_object()
        return Response(self.get_serializer(consulta).data)
    
    @extend_schema(
            description='Listar os exames de uma consulta.',
            summary="Listar os exames de uma consulta",
            responses={200: ConsultaExamesSerializer},
    )
    @action(detail=True, methods=['get'])
    def listar_exames(self, request, pk=None):
        consulta = self.get_object()
        serializer = ConsultaExamesSerializer(consulta)
        return Response(serializer.data)
    
    @extend_schema(
            description='Adiciona um link para uma videoconferência de telemedicina.',
            summary="Adicionar link de telemedicina",
            responses={200: ConsultaSerializer},
            examples=[
            OpenApiExample(
                'Exemplo de adição de link para telemedicina',
                value={
                    "linkTeleconsulta": "https://meet.google.com/123-qwe-asd",
                },
                request_only=True,
            )
        ]
    )
    @action(detail=True, methods=['post'])
    def add_telemedicina_link(self, request, pk=None):
        consulta = self.get_object()
        link = request.data.get('link')

        if not link:
            raise ValidationError("Informe um link para telemedicina online.")
        
        consulta.linkTeleconsulta = link
        consulta.save()
        return Response(self.get_serializer(consulta).data)
    
    @extend_schema(
            description='Remove o link para uma videoconferência de telemedicina.',
            summary="Remover link de telemedicina",
            responses={200: ConsultaSerializer},
    )
    @action(detail=True, methods=['post'])
    def remove_telemedicina_link(self, request, pk=None):
        consulta = self.get_object()
        consulta.linkTeleconsulta = ""
        consulta.save()

        return Response(self.get_serializer(consulta).data)
    
    @extend_schema(
        description='Adiciona um exame à consulta.',
        request=AddExameRequestSerializer,
        responses={200: ConsultaSerializer},
        summary="Adicionar um exame a consulta",
        examples=[
            OpenApiExample(
                'Exemplo de adição de exame',
                value={
                    "tipoExame": "Hemograma",
                    "detalhes": "Verificar níveis de hemoglobina"
                },
                request_only=True,
            )
        ]
    )
    @action(detail=True, methods=['post'])
    def add_exame(self, request, pk=None):
        consulta = self.get_object()
        
        if 'tipoExame' not in request.data:
            raise ValidationError("É necessário informar o tipo de exame.")
        
        exame_data = {
            'idPaciente': consulta.idPaciente,
            'idProfissionalSolicitante': consulta.idProfissional,
            'idLocal': consulta.idLocal,
            'tipoExame': request.data.get('tipoExame'),
            'detalhesSolicitacao': request.data.get('detalhes', ''),
            'status': 'SOLI',
            'resultadoExame': {}
        }

        exame = Exame.objects.create(**exame_data)

        ConsultaExame.objects.create(idConsulta=consulta, idExame=exame)

        return Response(self.get_serializer(consulta).data)
    
    @extend_schema(
        description='Cancela um exame da consulta.',
        request=AddExameRequestSerializer,
        responses={200: ConsultaSerializer},
        summary="Cancelar um exame da consulta",
        examples=[
            OpenApiExample(
                'Exemplo',
                value={
                    "idExame": 1,
                },
                request_only=True,
            )
        ]
    )
    @action(detail=True, methods=['post'])
    def cancel_exame(self, request, pk=None):
        consulta = self.get_object()
        id_exame = request.data.get('idExame')

        if not id_exame:
            raise ValidationError("É necessário informar o ID do exame em 'idExame'.")
        
        try:
            consulta_exame = ConsultaExame.objects.get(idConsulta=consulta, idExame=id_exame)
        except ConsultaExame.DoesNotExist:
            raise ValidationError("Este exame não está vinculado a esta consulta.")
        
        exame = consulta_exame.idExame
        exame.status = 'CANC'
        exame.save()

        return Response(self.get_serializer(consulta).data)
