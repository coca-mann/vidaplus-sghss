from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse, extend_schema_view
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
    tags=["Financeiro"]
)
@extend_schema_view(
    list=extend_schema(
        summary="Listar categorias financeiras",
        description="Lista todas as categorias financeiras cadastradas.",
        responses={200: CategoriaFinanceiraSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Detalhar categoria financeira",
        description="Recupera os detalhes de uma categoria financeira específica.",
        responses={200: CategoriaFinanceiraSerializer}
    ),
    create=extend_schema(
        summary="Criar categoria financeira",
        description="Cadastra uma nova categoria financeira.",
        examples=[
            OpenApiExample(
                'Exemplo de categoria',
                value={
                    "nome": "Consultas",
                    "tipo": "REC",
                    "descricao": "Receitas provenientes de consultas"
                }
            ),
        ],
        responses={201: CategoriaFinanceiraSerializer}
    ),
    update=extend_schema(
        summary="Atualizar categoria financeira",
        description="Atualiza todos os dados de uma categoria financeira existente.",
        responses={200: CategoriaFinanceiraSerializer}
    ),
    partial_update=extend_schema(
        summary="Atualização parcial de categoria financeira",
        description="Atualiza parcialmente os dados de uma categoria financeira.",
        responses={200: CategoriaFinanceiraSerializer}
    ),
    destroy=extend_schema(
        summary="Remover categoria financeira",
        description="Remove uma categoria financeira do sistema.",
        responses={204: OpenApiResponse(description="Categoria removida com sucesso")}
    ),
)
class CategoriaFinanceiraViewSet(ModelViewSet):
    queryset = CategoriaFinanceira.objects.all()
    serializer_class = CategoriaFinanceiraSerializer
    permission_classes = [IsAuthenticated, IsFinanceAdmin]


@extend_schema(
    tags=["Financeiro"]
)
@extend_schema_view(
    list=extend_schema(
        summary="Listar lançamentos financeiros",
        description="Lista todos os lançamentos financeiros cadastrados.",
        responses={200: LancamentoFinanceiroSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Detalhar lançamento financeiro",
        description="Recupera os detalhes de um lançamento financeiro específico.",
        responses={200: LancamentoFinanceiroSerializer}
    ),
    create=extend_schema(
        summary="Criar lançamento financeiro",
        description="Cadastra um novo lançamento financeiro.",
        examples=[
            OpenApiExample(
                'Exemplo de lançamento',
                value={
                    "idLocal": 2,
                    "idCategoria": 1,
                    "idFornecedor": 5,
                    "valor": "125.00",
                    "formaPagamento": "PIX"
                }
            ),
        ],
        responses={201: LancamentoFinanceiroSerializer}
    ),
    update=extend_schema(
        summary="Atualizar lançamento financeiro",
        description="Atualiza todos os dados de um lançamento financeiro existente.",
        responses={200: LancamentoFinanceiroSerializer}
    ),
    partial_update=extend_schema(
        summary="Atualização parcial de lançamento financeiro",
        description="Atualiza parcialmente os dados de um lançamento financeiro.",
        responses={200: LancamentoFinanceiroSerializer}
    ),
    destroy=extend_schema(
        summary="Remover lançamento financeiro",
        description="Remove um lançamento financeiro do sistema.",
        responses={204: OpenApiResponse(description="Lançamento removido com sucesso")}
    ),
)
class LancamentoFinanceiroViewSet(ModelViewSet):
    queryset = LancamentoFinanceiro.objects.all()
    serializer_class = LancamentoFinanceiroSerializer
    permission_classes = [IsAuthenticated, IsFinanceAdmin]
