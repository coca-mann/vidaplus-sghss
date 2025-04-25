from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.backoffice.views.compras import (
    FornecedorViewSet,
    ItemPedidoViewSet,
    PedidoCompraViewSet
)
from backend.backoffice.views.estoque import (
    EstoqueSuprimentoViewSet,
    SuprimentoViewSet,
    UnidadeMedidaViewSet
)
from backend.backoffice.views.financeiro import (
    CategoriaFinanceiraViewSet,
    LancamentoFinanceiroViewSet
)
from backend.backoffice.views.gestaohospitalar import (
    AlaViewSet,
    LeitoViewSet,
    LogOcupacaoLeitoViewSet
)


router = DefaultRouter()
router.register('fornecedor', FornecedorViewSet)
router.register('itempedidocompra', ItemPedidoViewSet)
router.register('pedidocompra', PedidoCompraViewSet)
router.register('estoquesuprimento', EstoqueSuprimentoViewSet)
router.register('suprimento', SuprimentoViewSet)
router.register('unidademedida', UnidadeMedidaViewSet)
router.register('categoriafinanceira', CategoriaFinanceiraViewSet)
router.register('lancamentofinanceiro', LancamentoFinanceiroViewSet)
router.register('ala', AlaViewSet, basename='ala')
router.register('leito', LeitoViewSet)
router.register('logleito', LogOcupacaoLeitoViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
