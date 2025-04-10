from rest_framework import serializers
from backend.atendimento.models.exame import Exame


class ExameSerializer(serializers.ModelSerializer):


    class Meta:
        model = Exame
        fields = '__all__'
