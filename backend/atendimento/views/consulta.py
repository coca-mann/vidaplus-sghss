from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from backend.atendimento.models.consulta import (Consulta)
from backend.atendimento.serializers.consulta import (ConsultaSerializer)

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

