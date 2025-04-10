from rest_framework import serializers
from backend.pessoa.models.saude import (
    AgendaProfissionalSaude,
    Especialidade,
    ProfissionalSaude
)


class AgendaProfissionalSaudeSerializer(serializers.ModelSerializer):


    class Meta:
        model = AgendaProfissionalSaude
        fields = '__all__'


class EspecialidadeSerializer(serializers.ModelSerializer):


    class Meta:
        model = Especialidade
        fields = '__all__'


class ProfissionalSaudeSerializer(serializers.ModelSerializer):


    class Meta:
        model = ProfissionalSaude
        fields = '__all__'
