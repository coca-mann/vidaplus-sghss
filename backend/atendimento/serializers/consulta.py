from rest_framework import serializers
from backend.atendimento.models.consulta import Consulta
from backend.local.serializers import LocalSerializer
from backend.pessoa.serializers.paciente import PacienteSerializer
from backend.pessoa.serializers.saude import ProfissionalSaudeSerializer
from backend.atendimento.serializers.prontuario import ProntuarioSerializer


class ConsultaSerializer(serializers.ModelSerializer):
    local_details = LocalSerializer(source='idLocal', read_only=True)
    paciente_details = PacienteSerializer(source='idPaciente', read_only=True)
    profissional_details = ProfissionalSaudeSerializer(source='idProfissional', read_only=True)
    prontuario_details = ProntuarioSerializer(source='idProntuario', read_only=True)
    

    class Meta:
        model = Consulta
        fields = '__all__'
        extra_kwargs = {
            'medicamentoPrescrito': {'required': False},
            'examesSolicitados': {'required': False},
        }

    def validate(self, data):
        profissional = data.get('idProfissional')
        if profissional:

            pode_criar_consulta = False
            for especialidade in profissional.especialidades.all():
                if especialidade.realiza_consulta:
                    pode_criar_consulta = True
                    break
                    
            if not pode_criar_consulta:
                raise serializers.ValidationError(
                    "O profissional selecionado não tem permissão para realizar consultas."
                )
        
        return data
