from django.utils import timezone
from rest_framework import serializers
from backend.backoffice.models.gestaohospitalar import (
    Ala,
    Leito,
    LogOcupacaoLeito
)
from backend.pessoa.models.paciente import Paciente
from backend.pessoa.models.saude import ProfissionalSaude
from backend.local.models import Local


class AlaSerializer(serializers.ModelSerializer):


    class Meta:
        model = Ala
        fields = '__all__'


class LeitoSerializer(serializers.ModelSerializer):
    paciente = serializers.SerializerMethodField()


    class Meta:
        model = Leito
        fields = ['idLeito', 'idLocal', 'idAla', 'numeroLeito', 'status', 'paciente', 'idPaciente']

    def get_paciente(self, obj):
        if not hasattr(obj, 'idPaciente') or obj.idPaciente is None:
            return None
        
        detalhes_paciente = self.context.get('mostrar_detalhes_paciente', False)

        if detalhes_paciente:
            return {
                'idPaciente': obj.idPaciente.idPaciente,
                'nome': obj.idPaciente.nome,
                'cpf': obj.idPaciente.cpf,
                'dataNascimento': obj.idPaciente.dataNascimento,
            }
        else:
            return {
                'idPaciente': obj.idPaciente.idPaciente,
                'nome': obj.idPaciente.nome
            }


class LogOcupacaoLeitoSerializer(serializers.ModelSerializer):


    class Meta:
        model = LogOcupacaoLeito
        fields = '__all__'


class InternarPacienteSerializer(serializers.Serializer):
    idPaciente = serializers.IntegerField()
    idLocal = serializers.IntegerField()
    idProfissionalInternacao = serializers.IntegerField()
    dataHoraEntrada = serializers.DateTimeField(default=timezone.now)
    dataHoraSaida = serializers.DateTimeField(required=False, allow_null=True)
    motivoInternacao = serializers.CharField()
    observacao = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        
        try:
            paciente = Paciente.objects.get(pk=data['idPaciente'])
        except Paciente.DoesNotExist:
            raise serializers.ValidationError('Paciente não encontrado')
        
        try:
            local = Local.objects.get(pk=data['idLocal'])
        except Local.DoesNotExist:
            raise serializers.ValidationError('Local não encontrado')
        
        try:
            profissional = ProfissionalSaude.objects.get(pk=data['idProfissionaInternacao'])
        except ProfissionalSaude.DoesNotExist:
            raise serializers.ValidationError('Profissional de saúde não encontrado.')
        
        return data
