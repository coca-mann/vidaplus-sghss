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

'''
CATEGORIA E LANCAMENTO
- Somente administradores do tipo DIRGERAL, DIRFINAN e DIRADMIN podem criar, editar e excluir dados
- Pacientes e médicos não podem ver essas informações
'''
class CategoriaFinanceiraViewSet(ModelViewSet):
    queryset = CategoriaFinanceira.objects.all()
    serializer_class = CategoriaFinanceiraSerializer
    permission_classes = [IsAuthenticated]


class LancamentoFinanceiroViewSet(ModelViewSet):
    queryset = LancamentoFinanceiro.objects.all()
    serializer_class = LancamentoFinanceiroSerializer
    permission_classes = [IsAuthenticated]
