from rest_framework import serializers


class MedicamentoSerializer(serializers.Serializer):
    nome = serializers.CharField(
        max_length=255,
        required=True,
        help_text="Nome do medicamento"
    )
    dosagem = serializers.CharField(
        max_length=255,
        required=True,
        help_text="Dosagem do medicamento (ex: '500mg')"
    )
    intervalo = serializers.CharField(
        max_length=255,
        required=True,
        help_text="Intervalo de administração (ex: '8 horas')"
    )


class RemoveMedicamentoSerializer(serializers.Serializer):
    nome = serializers.CharField(
        max_length=255, 
        required=True, 
        help_text="Nome do medicamento a ser removido"
    )
