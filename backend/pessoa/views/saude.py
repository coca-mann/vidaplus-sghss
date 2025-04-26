from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes
from django_filters import rest_framework as filters
from backend.pessoa.models.saude import (
    AgendaProfissionalSaude,
    Especialidade,
    ProfissionalSaude
)
from backend.pessoa.serializers.saude import (
    AgendaProfissionalSaudeSerializer,
    EspecialidadeSerializer,
    ProfissionalSaudeSerializer
)
from backend.pessoa.permissions.saude import IsAdminOrReadOnly


@extend_schema_view(
    list=extend_schema(
        summary="Listar agendas de profissionais de saúde",
        description=(
            "Retorna uma lista paginada das agendas de profissionais de saúde. "
            "Permite filtrar por ID do profissional, nome parcial ou exato do profissional."
        ),
        tags=["Agenda Profissional Saúde"],
        parameters=[
            OpenApiParameter("idProfissional", OpenApiTypes.INT, OpenApiParameter.QUERY, description="ID do profissional"),
            OpenApiParameter("nome_profissionalsaude", OpenApiTypes.STR, OpenApiParameter.QUERY, description="Busca parcial por nome do profissional"),
            OpenApiParameter("nome_profissionalsaude_exato", OpenApiTypes.STR, OpenApiParameter.QUERY, description="Busca exata (case-insensitive) por nome do profissional"),
        ]
    ),
        retrieve=extend_schema(
        summary="Detalhar agenda de profissional de saúde",
        description="Retorna detalhes de uma agenda específica.",
        tags=["Agenda Profissional Saúde"],
    ),
    create=extend_schema(
        summary="Criar agenda de profissional de saúde",
        description="Cria uma nova agenda para um profissional de saúde.",
        tags=["Agenda Profissional Saúde"],
    ),
    update=extend_schema(
        summary="Atualizar agenda de profissional de saúde",
        description="Atualiza todos os dados de uma agenda existente.",
        tags=["Agenda Profissional Saúde"],
    ),
    partial_update=extend_schema(
        summary="Atualizar parcialmente agenda de profissional de saúde",
        description="Atualiza parcialmente os dados de uma agenda existente.",
        tags=["Agenda Profissional Saúde"],
    ),
    destroy=extend_schema(
        summary="Remover agenda de profissional de saúde",
        description="Remove uma agenda do sistema.",
        tags=["Agenda Profissional Saúde"],
    ),
)
class AgendaProfissionalSaudeViewSet(ModelViewSet):
    queryset = AgendaProfissionalSaude.objects.all()
    serializer_class = AgendaProfissionalSaudeSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(
        summary="Listar especialidades",
        description="Retorna uma lista de todas as especialidades cadastradas.",
        tags=["Especialidades"],
    ),
    retrieve=extend_schema(
        summary="Detalhar especialidade",
        description="Retorna detalhes de uma especialidade pelo ID.",
        tags=["Especialidades"],
    ),
    create=extend_schema(
        summary="Criar especialidade",
        description="Cria uma nova especialidade. Apenas administradores podem criar.",
        tags=["Especialidades"],
    ),
    update=extend_schema(
        summary="Atualizar especialidade",
        description="Atualiza todos os dados de uma especialidade. Apenas administradores podem atualizar.",
        tags=["Especialidades"],
    ),
    partial_update=extend_schema(
        summary="Atualizar parcialmente especialidade",
        description="Atualiza parcialmente os dados de uma especialidade. Apenas administradores podem atualizar.",
        tags=["Especialidades"],
    ),
    destroy=extend_schema(
        summary="Remover especialidade",
        description="Remove uma especialidade. Apenas administradores podem remover.",
        tags=["Especialidades"],
    ),
)
class EspecialidadeViewSet(ModelViewSet):
    queryset = Especialidade.objects.all()
    serializer_class = EspecialidadeSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


@extend_schema_view(
    list=extend_schema(
        summary="Listar profissionais de saúde do usuário autenticado",
        description="Retorna os profissionais de saúde vinculados ao usuário autenticado.",
        tags=["Profissionais de Saúde"],
    ),
    retrieve=extend_schema(
        summary="Detalhar profissional de saúde",
        description="Retorna detalhes de um profissional de saúde do usuário autenticado.",
        tags=["Profissionais de Saúde"],
    ),
    create=extend_schema(
        summary="Criar profissional de saúde",
        description="Cadastra um novo profissional de saúde vinculado ao usuário autenticado.",
        tags=["Profissionais de Saúde"],
    ),
    update=extend_schema(
        summary="Atualizar profissional de saúde",
        description="Atualiza todos os dados de um profissional de saúde do usuário autenticado.",
        tags=["Profissionais de Saúde"],
    ),
    partial_update=extend_schema(
        summary="Atualizar parcialmente profissional de saúde",
        description="Atualiza parcialmente os dados de um profissional de saúde do usuário autenticado.",
        tags=["Profissionais de Saúde"],
    ),
    destroy=extend_schema(
        summary="Remover profissional de saúde",
        description="Remove um profissional de saúde do usuário autenticado.",
        tags=["Profissionais de Saúde"],
    ),
)
class ProfissionalSaudeViewSet(ModelViewSet):
    serializer_class = ProfissionalSaudeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProfissionalSaude.objects.filter(idUsuario__username=self.request.user)
    
    @extend_schema(
        summary="Adicionar especialidades ao profissional de saúde",
        description="Adiciona uma ou mais especialidades ao profissional de saúde informado.",
        tags=["Profissionais de Saúde"],
        request={
            "type": "object",
            "properties": {
                "especialidades": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "Lista de IDs das especialidades a serem adicionadas"
                }
            },
            "required": ["especialidades"],
        },
        responses={200: ProfissionalSaudeSerializer},
    )
    @action(detail=True, methods=['post'])
    def add_especialidades(self, request, pk=None):
        profissional = self.get_object()
        especialidades_ids = request.data.get('especialidades', [])

        especialidades = Especialidade.objects.filter(idEspecialidade__in=especialidades_ids)
        profissional.especialidades.add(*especialidades)

        return Response(ProfissionalSaudeSerializer(profissional).data)
    
    @extend_schema(
        summary="Remover especialidades do profissional de saúde",
        description="Remove uma ou mais especialidades do profissional de saúde informado.",
        tags=["Profissionais de Saúde"],
        request={
            "type": "object",
            "properties": {
                "especialidades": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "Lista de IDs das especialidades a serem removidas"
                }
            },
            "required": ["especialidades"],
        },
        responses={200: ProfissionalSaudeSerializer},
    )
    @action(detail=True, methods=['post'])
    def remove_especialidades(self, request, pk=None):
        profissional = self.get_object()
        especialidades_ids = request.data.get('especialidades', [])

        especialidades = Especialidade.objects.filter(idEspecialidade__in=especialidades_ids)
        profissional.especialidades.remove(*especialidades)

        return Response(ProfissionalSaudeSerializer(profissional).data)
