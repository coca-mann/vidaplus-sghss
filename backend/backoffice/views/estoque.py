from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from backend.backoffice.models.estoque import (
    EstoqueSuprimento,
    Suprimento,
    UnidadeMedida
)
from backend.backoffice.serializers.estoque import (
    EstoqueSuprimeiroSerializer,
    SuprimeiroSerializer,
    UnidadeMedidaSerializer
)


class EstoqueSuprimentoViewSet(ModelViewSet):
    queryset = EstoqueSuprimento.objects.all()
    serializer_class = EstoqueSuprimeiroSerializer
    permission_classes = [IsAuthenticated]


class SuprimentoViewSet(ModelViewSet):
    queryset = Suprimento.objects.all()
    serializer_class = SuprimeiroSerializer
    permission_classes = [IsAuthenticated]


class UnidadeMedidaViewSet(ModelViewSet):
    queryset = UnidadeMedida.objects.all()
    serializer_class = UnidadeMedidaSerializer
    permission_classes = [IsAuthenticated]
