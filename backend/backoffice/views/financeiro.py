from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from backend.backoffice.permissions import IsFinanceAdmin
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
@extend_schema(
    tags=["Financeiro"],
    description=(
        "API para gerenciar categorias financeiras. "
        "Somente administradores DIRGERAL, DIRFINAN e DIRADMIN podem criar, editar ou excluir. "
        "Pacientes e médicos não têm acesso a este recurso."
    ),
    responses={
        200: CategoriaFinanceiraSerializer,
        403: OpenApiResponse(description="Sem permissão para executar esta ação."),
    },
    examples=[
        OpenApiExample(
            'Exemplo de categoria',
            value={
                "idCategoria": 1,
                "nome": "Consultas",
                "tipo": "REC",
                "descricao": "Receitas provenientes de consultas"
            }
        ),
    ],
)
class CategoriaFinanceiraViewSet(ModelViewSet):
    queryset = CategoriaFinanceira.objects.all()
    serializer_class = CategoriaFinanceiraSerializer
    permission_classes = [IsAuthenticated, IsFinanceAdmin]


@extend_schema(
    tags=["Financeiro"],
    description=(
        "API para gerenciar lançamentos financeiros. "
        "Somente administradores DIRGERAL, DIRFINAN e DIRADMIN podem criar, editar ou excluir. "
        "Pacientes e médicos não têm acesso a este recurso."
    ),
    responses={
        200: LancamentoFinanceiroSerializer,
        403: OpenApiResponse(description="Sem permissão para executar esta ação."),
    },
    examples=[
        OpenApiExample(
            'Exemplo de lançamento',
            value={
                "idLancamento": 1,
                "idLocal": 2,
                "idCategoria": 1,
                "idFornecedor": 5,
                "dataLancamento": "2024-03-01T10:00:00Z",
                "valor": "125.00",
                "formaPagamento": "PIX"
            }
        ),
    ],
)
class LancamentoFinanceiroViewSet(ModelViewSet):
    queryset = LancamentoFinanceiro.objects.all()
    serializer_class = LancamentoFinanceiroSerializer
    permission_classes = [IsAuthenticated, IsFinanceAdmin]
