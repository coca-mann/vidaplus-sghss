from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
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


class AgendaProfissionalSaudeViewSet(ModelViewSet):
    queryset = AgendaProfissionalSaude.objects.all()
    serializer_class = AgendaProfissionalSaudeSerializer
    permission_classes = [IsAuthenticated]


class EspecialidadeViewSet(ModelViewSet):
    queryset = Especialidade.objects.all()
    serializer_class = EspecialidadeSerializer
    permission_classes = [IsAuthenticated]


class ProfissionalSaudeViewSet(ModelViewSet):
    serializer_class = ProfissionalSaudeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProfissionalSaude.objects.filter(idUsuario__username=self.request.user)
