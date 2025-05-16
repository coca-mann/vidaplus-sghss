from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from backend.pessoa.models.core import Administrador
from backend.pessoa.serializers.core import AdministradorSerializer

@extend_schema_view(
    list=extend_schema(
        summary="Listar administradores",
        description="Retorna uma lista paginada de todos os administradores cadastrados no sistema.",
        tags=["Administradores"],
    ),
    retrieve=extend_schema(
        summary="Detalhar administrador",
        description="Retorna os detalhes de um administrador específico pelo seu ID.",
        tags=["Administradores"],
    ),
    create=extend_schema(
        summary="Criar administrador",
        description="Permite criar um novo administrador.",
        tags=["Administradores"],
    ),
    update=extend_schema(
        summary="Atualizar administrador",
        description="Atualiza todos os dados de um administrador existente.",
        tags=["Administradores"],
    ),
    partial_update=extend_schema(
        summary="Atualizar parcialmente administrador",
        description="Atualiza parcialmente os dados de um administrador existente.",
        tags=["Administradores"],
    ),
    destroy=extend_schema(
        summary="Remover administrador",
        description="Remove um administrador do sistema.",
        tags=["Administradores"],
    ),
)
class AdministradorViewSet(ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer
    permission_classes = [IsAuthenticated]
