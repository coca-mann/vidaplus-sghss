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
    especialidades = EspecialidadeSerializer(many=True, read_only=True)

    class Meta:
        model = ProfissionalSaude
        fields = '__all__'
