from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from backend.pessoa.models.paciente import Paciente
from backend.pessoa.serializers.paciente import PacienteSerializer

@extend_schema_view(
    list=extend_schema(
        summary="Listar pacientes do usuário autenticado",
        description="Retorna uma lista de pacientes associados ao usuário autenticado.",
        tags=["Pacientes"],
    ),
    retrieve=extend_schema(
        summary="Detalhar paciente",
        description="Retorna os detalhes de um paciente associado ao usuário autenticado.",
        tags=["Pacientes"],
    ),
    create=extend_schema(
        summary="Criar paciente",
        description="Permite cadastrar um novo paciente vinculado ao usuário autenticado.",
        tags=["Pacientes"],
    ),
    update=extend_schema(
        summary="Atualizar paciente",
        description="Atualiza todos os dados de um paciente do usuário autenticado.",
        tags=["Pacientes"],
    ),
    partial_update=extend_schema(
        summary="Atualizar parcialmente paciente",
        description="Atualiza parcialmente os dados de um paciente do usuário autenticado.",
        tags=["Pacientes"],
    ),
    destroy=extend_schema(
        summary="Remover paciente",
        description="Remove um paciente associado ao usuário autenticado.",
        tags=["Pacientes"],
    ),
)
class PacienteViewSet(ModelViewSet):
    serializer_class = PacienteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Paciente.objects.filter(idUsuario=self.request.user)
