from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from auditlog.models import LogEntry
from backend.auditoria.serializers import LogEntrySerializer


class LogEntryViewSet(ReadOnlyModelViewSet):
    queryset = LogEntry.objects.all().order_by('-timestamp')
    serializer_class = LogEntrySerializer
    permission_classes = [IsAuthenticated]
