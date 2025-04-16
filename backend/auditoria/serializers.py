from rest_framework import serializers
from auditlog.models import LogEntry


class LogEntrySerializer(serializers.ModelSerializer):
    model_name = serializers.SerializerMethodField()
    action_label = serializers.SerializerMethodField()

    class Meta:
        model = LogEntry
        fields = '__all__'


    def get_model_name(self, obj):
        return obj.content_type.model_class().__name__
    

    def get_action_label(self, obj):
        return {
            0: 'Criado',
            1: 'Atualizado',
            2: 'Deletado',
        }.get(obj.action, 'Desconhecido')