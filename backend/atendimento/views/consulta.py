from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from datetime import datetime
from backend.atendimento.models.consulta import Consulta
from backend.atendimento.serializers.consulta import ConsultaSerializer
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
            
            from backend.pessoa.models.saude import ProfissionalSaude
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
            from backend.pessoa.models.saude import ProfissionalSaude
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

        if not all(key in medicamento for key in ['nome', 'dosagem', 'intervalo']):
            raise ValidationError("O medicamento deve conter 'nome', 'dosagem' e 'intervalo'")
        
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

    @action(detail=True, methods=['post'])
    def remove_medicamento(self, request, pk=None):
        consulta = self.get_object()
        nome_medicamento = request.data.get('nome')

        if not nome_medicamento:
            raise ValidationError("É necessário informar o nome do medicamento a ser removido.")
        
        if consulta.medicamentoPrescrito is None:
            return Response(self.get_serializer(consulta).data)
        
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
    
    @action(detail=True, methods=['post'])
    def add_exame(self, request, pk=None):
        consulta = self.get_object()
        exame = request.data.get('exame', {})

        if not all(key in exame for key in ['tipoExame', 'dataSolicitacao']):
            raise ValidationError("O exame deve conter 'tipoExame' e 'dataSolicitacao'.")
        
        if consulta.examesSolicitados is None:
            consulta.examesSolicitados = []

        for i, ex in enumerate(consulta.examesSolicitados):
            if (ex.get('tipoExame') == exame.get('tipoExame') and ex.get('dataSolicitacao') == exame.get('dataSolicitacao')):
                consulta.examesSolicitados[i] = exame
                consulta.save()
                return Response(self.get_serializer(consulta).data)
            
        consulta.examesSolicitados.append(exame)
        consulta.save()

        return Response(self.get_serializer(consulta).data)
    
    @action(detail=True, methods=['post'])
    def remove_exame(self, request, pk=None):
        consulta = self.get_object()
        tipo_exame = request.data.get('tipoExame')
        data_solicitacao = request.data.get('dataSolicitacao')

        if not tipo_exame or not data_solicitacao:
            raise ValidationError("É necessário informar o tipo e a data de solicitação do exame a ser removido.")
        
        if consulta.examesSolicitados is None:
            return Response(self.get_serializer(consulta).data)
        
        consulta.examesSolicitados = [
            ex for ex in consulta.examesSolicitados
            if not (ex.get('tipoExame') == tipo_exame and ex.get('dataSolicitacao') == data_solicitacao)
        ]

        consulta.save()
        return Response(self.get_serializer(consulta).data)
    
    @action(detail=True, methods=['get'])
    def listar_exames(self, request, pk=None):
        consulta = self.get_object()
        return Response(consulta.examesSolicitados or [])
