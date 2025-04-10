from rest_framework import serializers
from backend.backoffice.models.financeiro import (
    CategoriaFinanceira,
    LancamentoFinanceiro
)


class CategoriaFinanceiraSerializer(serializers.ModelSerializer):


    class Meta:
        model = CategoriaFinanceira
        fields = '__all__'


class LancamentoFinanceiroSerializer(serializers.ModelSerializer):


    class Meta:
        model = LancamentoFinanceiro
        fields = '__all__'
