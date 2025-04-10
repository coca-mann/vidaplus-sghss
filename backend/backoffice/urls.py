from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.backoffice.views.compras import (
    FornecedorViewSet,
    ItemPedidoViewSet,
    PedidoCompraViewSet
)


router = DefaultRouter()
router.register('fornecedor', FornecedorViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
