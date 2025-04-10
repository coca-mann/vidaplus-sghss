from rest_framework import serializers
from backend.atendimento.models.prontuario import Prontuario


class ProntuarioSerializer(serializers.ModelSerializer):


    class Meta:
        model = Prontuario
        fields = '__all__'
