from rest_framework import serializers
from backend.pessoa.models.saude import (
    AgendaProfissionalSaude,
    Especialidade,
    ProfissionalSaude
)

'''
AGENDA
- Profissionais saude adicionam horários disponíveis e indisponíveis
- Pacientes apenas consultam horários DISPONÍVEIS, não podem criar horários
- Pacientes buscam profissionais pelo nome via parametro
'''
class AgendaProfissionalSaudeSerializer(serializers.ModelSerializer):


    class Meta:
        model = AgendaProfissionalSaude
        fields = '__all__'

'''
ESPECIALIDADES
- Somente usuários Admin podem criar, editar, excluir especialidades
'''
class EspecialidadeSerializer(serializers.ModelSerializer):


    class Meta:
        model = Especialidade
        fields = '__all__'

'''
PROFISSIONAL SAUDE
- Atualizar lista de especialidades, sem apagar os demais dados do profissional
'''
class ProfissionalSaudeSerializer(serializers.ModelSerializer):
    especialidades = EspecialidadeSerializer(many=True, read_only=True)

    class Meta:
        model = ProfissionalSaude
        fields = '__all__'
