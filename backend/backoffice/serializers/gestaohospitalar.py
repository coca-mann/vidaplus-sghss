from rest_framework import serializers
from backend.backoffice.models.gestaohospitalar import (
    Ala,
    Leito,
    LogOcupacaoLeito
)


class AlaSerializer(serializers.ModelSerializer):


    class Meta:
        model = Ala
        fields = '__all__'


class LeitoSerializer(serializers.ModelSerializer):


    class Meta:
        model = Leito
        fields = '__all__'


class LogOcupacaoLeitoSerializer(serializers.ModelSerializer):


    class Meta:
        model = LogOcupacaoLeito
        fields = '__all__'
