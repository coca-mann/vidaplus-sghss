from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from backend.pessoa.models.paciente import Paciente


class FichaMedicaSerializer(serializers.Serializer):
    alergias = serializers.CharField(required=False, allow_blank=True)
    doencasCronicas = serializers.ListField(child=serializers.CharField(), required=False)
    medicamentosUso = serializers.ListField(child=serializers.CharField(), required=False)
    cirurgiasAnteriores = serializers.CharField(required=False, allow_blank=True)
    historicoFamiliar = serializers.CharField(required=False, allow_blank=True)
    grupoSanguineo = serializers.CharField(required=False, allow_blank=True)
    possuiDeficiencia = serializers.BooleanField(required=False)
    tipoDeficiencia = serializers.CharField(required=False, allow_blank=True)
    observacoes = serializers.CharField(required=False, allow_blank=True)


class PacienteSerializer(serializers.ModelSerializer):
    fichaMedica = serializers.JSONField(required=False)
    convenio = serializers.JSONField(required=False)


    @extend_schema_field(FichaMedicaSerializer)
    def get_fichaMedica(self, obj):
        return obj.fichaMedica


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['fichaMedica'] = self.get_fichaMedica(instance)
        return rep


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


    class Meta:
        model = Paciente
        fields = '__all__'
