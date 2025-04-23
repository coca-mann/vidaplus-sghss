from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from backend.backoffice.models.compras import (
    Fornecedor,
    ItemPedidoCompra,
    PedidoCompra
)
from backend.backoffice.serializers.compras import (
    FornecedorSerializer,
    ItemPedidoSerializer,
    PedidoCompraSerializer
)

'''
FORNECEDOR E PEDIDO COMPRA
- Somente administradores do tipo DIRFINAN, DIRGERAL, DIRADMIN e GESTOR podem ver, editar e excluir dados.
- Pacientes e médicos não pode ver essas informações
'''
class FornecedorViewSet(ModelViewSet):
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer
    permission_classes = [IsAuthenticated]


class ItemPedidoViewSet(ModelViewSet):
    queryset = ItemPedidoCompra.objects.all()
    serializer_class = ItemPedidoSerializer
    permission_classes = [IsAuthenticated]

class PedidoCompraViewSet(ModelViewSet):
    queryset = PedidoCompra.objects.all()
    serializer_class = PedidoCompraSerializer
    permission_classes = [IsAuthenticated]
