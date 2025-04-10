from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from backend.backoffice.models.financeiro import (
    CategoriaFinanceira,
    LancamentoFinanceiro
)
from backend.backoffice.serializers.financeiro import (
    CategoriaFinanceiraSerializer,
    LancamentoFinanceiroSerializer
)


class CategoriaFinanceiraViewSet(ModelViewSet):
    queryset = CategoriaFinanceira.objects.all()
    serializer_class = CategoriaFinanceiraSerializer
    permission_classes = [IsAuthenticated]


class LancamentoFinanceiroViewSet(ModelViewSet):
    queryset = LancamentoFinanceiro.objects.all()
    serializer_class = LancamentoFinanceiroSerializer
    permission_classes = [IsAuthenticated]
