from rest_framework import serializers
from backend.backoffice.models.estoque import (
    EstoqueSuprimento,
    Suprimento,
    UnidadeMedida
)


class EstoqueSuprimeiroSerializer(serializers.ModelSerializer):


    class Meta:
        model = EstoqueSuprimento
        fields = '__all__'


class SuprimeiroSerializer(serializers.ModelSerializer):


    class Meta:
        model = Suprimento
        fields = '__all__'



class UnidadeMedidaSerializer(serializers.ModelSerializer):


    class Meta:
        model = UnidadeMedida
        fields = '__all__'
