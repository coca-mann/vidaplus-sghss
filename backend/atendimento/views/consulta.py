from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from datetime import datetime
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from backend.atendimento.models.consulta import Consulta
from backend.atendimento.models.exame import Exame
from backend.atendimento.models.consulta_exame import ConsultaExame
from backend.atendimento.serializers.consulta import ConsultaSerializer
from backend.atendimento.serializers.medicamento import MedicamentoSerializer, RemoveMedicamentoSerializer
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
    
    @action(detail=False, methods=['get'])
    def consultas_hoje(self, request):
        hoje = datetime.now().date()
        consultas = self.get_queryset().filter(dataHoraConsulta__date=hoje, status='AGEN')
        serializer = self.get_serializer(consultas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def consultas_pendentes(self, request):
        consultas = self.get_queryset().filter(status='AGEN')
        serializer = self.get_serializer(consultas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancelar_consulta(self, request, pk=None):
        consulta = self.get_object()
        consulta.status = 'CANC'
        consulta.save()
        serializer = self.get_serializer(consulta)
        return Response(serializer.data)
    
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
        description="Adiciona um medicamento à consulta",
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


    @action(detail=True, methods=['get'])
    def listar_medicamentos(self, request, pk=None):
        consulta = self.get_object()
        return Response(self.get_serializer(consulta).data)
    
    @action(detail=True, methods=['get'])
    def listar_exames(self, request, pk=None):
        consulta = self.get_object()
        return Response(consulta.examesSolicitados or [])
    
    @action(detail=True, methods=['post'])
    def add_telemedicina_link(self, request, pk=None):
        consulta = self.get_object()
        link = request.data.get('link')

        if not link:
            raise ValidationError("Informe um link para telemedicina online.")
        
        consulta.linkTeleconsulta = link
        consulta.save()
        return Response(self.get_serializer(consulta).data)
    
    @action(detail=True, methods=['post'])
    def remove_telemedicina_link(self, request, pk=None):
        consulta = self.get_object()
        consulta.linkTeleconsulta = ""
        consulta.save()

        return Response(self.get_serializer(consulta).data)
    
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
