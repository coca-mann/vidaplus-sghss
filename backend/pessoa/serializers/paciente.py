from rest_framework import serializers
from backend.pessoa.models.paciente import Paciente


class PacienteSerializer(serializers.ModelSerializer):


    class Meta:
        model = Paciente
        fields = '__all__'
