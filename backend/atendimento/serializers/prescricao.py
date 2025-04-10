from rest_framework import serializers
from backend.atendimento.models.prescricao import Prescricao


class PrescricaoSerializer(serializers.ModelSerializer):


    class Meta:
        model = Prescricao
        fields = '__all__'
