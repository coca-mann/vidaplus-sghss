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


class AlaViewSet(ModelViewSet):
    queryset = Ala.objects.all()
    serializer_class = AlaSerializer
    permission_classes = [IsAuthenticated]


class LeitoViewSet(ModelViewSet):
    queryset = Leito.objects.all()
    serializer_class = LeitoSerializer
    permission_classes = [IsAuthenticated]


class LogOcupacaoLeitoViewSet(ModelViewSet):
    queryset = LogOcupacaoLeito.objects.all()
    serializer_class = LogOcupacaoLeitoSerializer
    permission_classes = [IsAuthenticated]
