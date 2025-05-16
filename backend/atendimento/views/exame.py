from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from backend.atendimento.models.exame import Exame
from backend.atendimento.serializers.exame import ExameSerializer
from backend.pessoa.models.saude import ProfissionalSaude
from backend.pessoa.models.paciente import Paciente


@extend_schema(
    tags=['Exames'],
    description=(
        "API para consulta de exames. "
        "Profissionais visualizam exames solicitados por eles. "
        "Pacientes visualizam seus próprios exames. "
        "Administradores visualizam todos os exames."
    )
)
@extend_schema_view(
    list=extend_schema(
        summary="Listar exames",
        description="Retorna todos os exames que o usuário autenticado pode visualizar.",
        responses={200: ExameSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Detalhar exame",
        description="Retorna os detalhes de um exame específico.",
        responses={200: ExameSerializer}
    ),
)
class ExameViewSet(ReadOnlyModelViewSet):
    serializer_class = ExameSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Exame.objects.all()
        user = self.request.user

        try:
            profissional = ProfissionalSaude.objects.get(idUsuario=user)
            return queryset.filter(idProfissionalSolicitante=profissional)
        except:
            pass

        try:
            paciente = Paciente.objects.get(idUsuario=user)
            return queryset.filter(idPaciente=paciente)
        except:
            pass

        if user.is_staff:
            return queryset
        
        return Exame.objects.none()
