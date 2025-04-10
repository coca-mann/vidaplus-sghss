from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from backend.atendimento.models.consulta import (
    Consulta,
    AtendimentoConsulta
)
from backend.atendimento.serializers.consulta import (
    ConsultaSerializer,
    AtendimentoConsultaSerializer
)


class ConsultaViewSet(ModelViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer
    permission_classes = [IsAuthenticated]


class AtendimentoConsultaViewSet(ModelViewSet):
    queryset = AtendimentoConsulta.objects.all()
    serializer_class = AtendimentoConsultaSerializer
    permission_classes = [IsAuthenticated]
