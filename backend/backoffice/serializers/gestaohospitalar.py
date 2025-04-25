from rest_framework import serializers
from backend.backoffice.models.gestaohospitalar import (
    Ala,
    Leito,
    LogOcupacaoLeito
)


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
