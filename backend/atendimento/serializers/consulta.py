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
            'medicamentosPrescritos': {'required': False},
            'examesSolicitados': {'required': False},
        }

    def validate_medicamentosPrescritos(self, value):
        if value:
            for medicamento in value:
                if not all(key in medicamento for key in ['nome', 'dosagem', 'intervalo']):
                    raise serializers.ValidationError('Cada medicamento deve conter nome, dosagem e intervalo.')
        return value
