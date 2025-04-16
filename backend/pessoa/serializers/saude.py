from rest_framework import serializers
from backend.pessoa.models.saude import (
    AgendaProfissionalSaude,
    Especialidade,
    ProfissionalSaude
)

'''
AGENDA
- Profissionais saude adicionam horários disponíveis e indisponíveis DONE
- Pacientes apenas consultam horários, não podem criar horários DONE
- Pacientes buscam profissionais pelo nome via parametro DONE
'''
class AgendaProfissionalSaudeSerializer(serializers.ModelSerializer):


    class Meta:
        model = AgendaProfissionalSaude
        fields = '__all__'

'''
ESPECIALIDADES
- Somente usuários Admin podem criar, editar, excluir especialidades DONE
'''
class EspecialidadeSerializer(serializers.ModelSerializer):


    class Meta:
        model = Especialidade
        fields = '__all__'

'''
PROFISSIONAL SAUDE
- Atualizar lista de especialidades, sem apagar os demais dados do profissional DONE
'''
class ProfissionalSaudeSerializer(serializers.ModelSerializer):
    especialidades = EspecialidadeSerializer(many=True, read_only=True)

    class Meta:
        model = ProfissionalSaude
        fields = '__all__'
