from rest_framework import serializers
from backend.backoffice.models.compras import (
    Fornecedor,
    ItemPedidoCompra,
    PedidoCompra
)


class FornecedorSerializer(serializers.ModelSerializer):


    class Meta:
        model = Fornecedor
        fields = '__all__'


class ItemPedidoSerializer(serializers.ModelSerializer):


    class Meta:
        model = ItemPedidoCompra
        fields = '__all__'


class PedidoCompraSerializer(serializers.ModelSerializer):


    class Meta:
        model = PedidoCompra
        fields = '__all__'
