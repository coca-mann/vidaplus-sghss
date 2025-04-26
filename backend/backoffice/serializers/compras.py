import datetime
from rest_framework import serializers
from backend.backoffice.models.compras import (
    Fornecedor,
    ItemPedidoCompra,
    PedidoCompra
)
from backend.backoffice.models.estoque import Suprimento
from backend.local.models import Local


class FornecedorSerializer(serializers.ModelSerializer):


    class Meta:
        model = Fornecedor
        fields = '__all__'

    def validate_cpfCnpj(self, value):
        value = ''.join(filter(str.isdigit, value))

        if len(value) != 11 and len(value) != 14:
            raise serializers.ValidationError('CPF/CNPJ deve ter 11 ou 14 dígitos.')
        
        return value


class ItemPedidoSerializer(serializers.ModelSerializer):
    nome_suprimento = serializers.SerializerMethodField()
    valor_total = serializers.SerializerMethodField()


    class Meta:
        model = ItemPedidoCompra
        fields = '__all__'

    def get_nome_suprimento(self, obj):
        return obj.idSuprimento.nome if obj.idSuprimento else None
    
    def get_valor_total(self, obj):
        return obj.quantidade * obj.valorUnitario
    
    def validate(self, data):

        if data.get('quantidade', 0) <= 0:
            raise serializers.ValidationError(
                {"quantidade": "A quantidade deve ser maior que zero."}
            )
        
        if data.get('valorUnitario', 0) <= 0:
            raise serializers.ValidationError(
                {"valorUnitario": "O valor unitário deve ser maior que zero."}
            )
        
        return data


class PedidoCompraSerializer(serializers.ModelSerializer):
    nome_fornecedor = serializers.SerializerMethodField()
    nome_local = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField(source='get_status_display', read_only=True)
    itens = serializers.SerializerMethodField()


    class Meta:
        model = PedidoCompra
        fields = '__all__'

    def get_nome_fornecedor(self, obj):
        return obj.idFornecedor.nomeFantasia if obj.idFornecedor else None
    
    def get_nome_local(self, obj):
        return obj.idLocal.nome if obj.idLocal else None
    
    def get_itens(self, obj):
        return ItemPedidoCompra.objects.filter(idPedido=obj.idPedido).count()
    
    def validate(self, data):
        if data.get('dataEntregaPrevista') and data.get('dataEntregaPrevista') < datetime.date.today():
            raise serializers.ValidationError(
                {"dataEntregaPrevista": "A data de entrega prevista deve ser futura."}
            )
        
        return data
