from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from backend.local.models import Local
from backend.local.serializers import LocalSerializer
from backend.local.permissions import IsAdminOrReadOnly

@extend_schema_view(
    list=extend_schema(
        summary="Listar locais",
        description="Retorna uma lista paginada de todos os locais cadastrados no sistema.",
        tags=["Locais"],
    ),
    retrieve=extend_schema(
        summary="Detalhar local",
        description="Retorna os detalhes de um local específico pelo seu ID.",
        tags=["Locais"],
    ),
)
class LocalViewSet(ModelViewSet):
    queryset = Local.objects.all()
    serializer_class = LocalSerializer
    permission_classes = [IsAdminOrReadOnly]
