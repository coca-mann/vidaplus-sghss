from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample, OpenApiTypes
from backend.pessoa.models.paciente import Paciente
from django.contrib.auth.models import User


@extend_schema_serializer(
    examples=[
    OpenApiExample(
        'Exemplo de Paciente',
        summary='Exemplo completo de envio de paciente',
        value={
            "nome": "Maria da Silva",
            "cpf": "12345678901",
            "data_nascimento": "1990-01-01",
            "fichaMedica": {
                "alergias": "Penicilina",
                "doencasCronicas": ["Diabetes"],
                "medicamentosUso": ["Metformina"],
                "cirurgiasAnteriores": "Apendicectomia em 2010",
                "historicoFamiliar": "Diabetes, hipertensão",
                "grupoSanguineo": "O+",
                "possuiDeficiencia": False,
                "tipoDeficiencia": "",
                "observacoes": "Paciente saudável"
                },
            "convenio": {
                "operadora": "Unimed",
                "numeroCarteira": "123456"
                }
            },
        request_only=True,
        response_only=False,
        ),
    ]
)
class PacienteSerializer(serializers.ModelSerializer):
    fichaMedica = serializers.JSONField(required=False)
    convenio = serializers.JSONField(required=False)


    def validate_fichaMedica(self, value):
        required_fields = {
            'alergias': '',
            'doencasCronicas': [],
            'medicamentosUso': [],
            'cirurgiasAnteriores': '',
            'historicoFamiliar': '',
            'grupoSanguineo': '',
            'possuiDeficiencia': False,
            'tipoDeficiencia': '',
            'observacoes': '',
        }

        if self.instance and self.instance.fichaMedica:
            atual = self.instance.fichaMedica
        else:
            atual = {}

        dados_enviados = value or {}
        ficha_final = {**atual, **dados_enviados}

        for campo, default in required_fields.items():
            if campo not in ficha_final:
                ficha_final[campo] = default

        return ficha_final


    def create(self, validated_data):
        ficha = validated_data.get('fichaMedica', {})
        validated_data['fichaMedica'] = self.validate_fichaMedica(ficha)
        return super().create(validated_data)


    def update(self, instance, validated_data):
        if 'fichaMedica' in self.initial_data:
            dados_enviados = self.initial_data.get('fichaMedica', {})
            validated_data['fichaMedica'] = self.validate_fichaMedica(dados_enviados)
        return super().update(instance, validated_data)
    
    def validate(self, data):
        cpf = data.get('cpf')
        if User.objects.filter(username=cpf).exists():
            raise serializers.ValidationError('Um usuário com este CPF já existe!')
        return data


    class Meta:
        model = Paciente
        fields = '__all__'
