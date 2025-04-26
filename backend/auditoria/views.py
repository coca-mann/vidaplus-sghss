from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from auditlog.models import LogEntry
from backend.auditoria.serializers import LogEntrySerializer

@extend_schema_view(
    list=extend_schema(
        summary="Listar logs de auditoria",
        description="Retorna uma lista paginada dos registros de auditoria do sistema, ordenados do mais recente para o mais antigo.",
        tags=["Auditoria"],
    ),
    retrieve=extend_schema(
        summary="Detalhar log de auditoria",
        description="Retorna os detalhes de um registro de auditoria específico pelo seu ID.",
        tags=["Auditoria"],
    ),
)
class LogEntryViewSet(ReadOnlyModelViewSet):
    queryset = LogEntry.objects.all().order_by('-timestamp')
    serializer_class = LogEntrySerializer
    permission_classes = [IsAuthenticated]
