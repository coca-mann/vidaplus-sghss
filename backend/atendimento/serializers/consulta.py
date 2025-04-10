from rest_framework import serializers
from backend.atendimento.models.consulta import (
    AtendimentoConsulta,
    Consulta
)


class ConsultaSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Consulta
        fields = '__all__'


class AtendimentoConsultaSerializer(serializers.ModelSerializer):


    class Meta:
        model = AtendimentoConsulta
        fields = '__all__'
