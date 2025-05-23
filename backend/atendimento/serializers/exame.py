from rest_framework import serializers
from backend.atendimento.models.exame import Exame
from backend.pessoa.serializers.paciente import PacienteSerializer
from backend.pessoa.serializers.saude import ProfissionalSaudeSerializer
from backend.local.serializers import LocalSerializer


class ExameSerializer(serializers.ModelSerializer):
    local_details = LocalSerializer(source='idLocal', read_only=True)
    paciente_details = PacienteSerializer(source='idPaciente', read_only=True)
    profissional_solicitante_details = ProfissionalSaudeSerializer(source='idProfissional', read_only=True)
    http_methods_name = ['get']

    class Meta:
        model = Exame
        fields = '__all__'


class AddExameRequestSerializer(serializers.Serializer):
    tipoExame = serializers.CharField(
        required=True, 
        help_text="Tipo de exame a ser solicitado (obrigatório)"
    )
    detalhes = serializers.CharField(
        required=False, 
        default='', 
        help_text="Detalhes adicionais sobre a solicitação do exame"
    )
    