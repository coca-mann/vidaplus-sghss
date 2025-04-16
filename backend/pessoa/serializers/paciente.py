from rest_framework import serializers
from backend.pessoa.models.paciente import Paciente
from django.contrib.auth.models import User


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
