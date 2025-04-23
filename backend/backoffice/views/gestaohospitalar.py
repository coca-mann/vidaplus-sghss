from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
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

'''
ALA
- Somente administradores podem editar alas
- Médicos podem ver alas com leitos ocupados
- Pacientes não podem ver alas
'''
class AlaViewSet(ModelViewSet):
    queryset = Ala.objects.all()
    serializer_class = AlaSerializer
    permission_classes = [IsAuthenticated]

'''
LEITOS
- Somente administradores podem editar leitos
- Médicos podem ver detalhes dos pacientes nos leitos
'''
class LeitoViewSet(ModelViewSet):
    queryset = Leito.objects.all()
    serializer_class = LeitoSerializer
    permission_classes = [IsAuthenticated]

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
