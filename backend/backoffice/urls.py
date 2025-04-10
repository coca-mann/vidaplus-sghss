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


router = DefaultRouter()
router.register('fornecedor', FornecedorViewSet)
router.register('itempedidocompra', ItemPedidoViewSet)
router.register('pedidocompra', PedidoCompraViewSet)
router.register('estoquesuprimento', EstoqueSuprimentoViewSet)
router.register('suprimento', SuprimentoViewSet)
router.register('unidademedida', UnidadeMedidaViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
