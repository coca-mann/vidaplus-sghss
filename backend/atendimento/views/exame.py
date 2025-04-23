from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from backend.atendimento.models.exame import Exame
from backend.atendimento.serializers.exame import ExameSerializer
from backend.pessoa.models.saude import ProfissionalSaude
from backend.pessoa.models.paciente import Paciente


@extend_schema_view(
    list=extend_schema(description='Listar exames'),
    retrieve=extend_schema(description='Obter detalhes de um exame'),
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
