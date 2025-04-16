from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
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


class AgendaProfissionalSaudeFilter(filters.FilterSet):
    nome_profissionalsaude = filters.CharFilter(field_name='idProfissional__nome', lookup_expr='icontains')
    nome_profissionalsaude_exato = filters.CharFilter(field_name='idProfissional__nome', lookup_expr='iexact')

    class Meta:
        model = AgendaProfissionalSaude
        fields = ['idProfissional', 'nome_profissionalsaude', 'nome_profissionalsaude_exato']


class AgendaProfissionalSaudeViewSet(ModelViewSet):
    queryset = AgendaProfissionalSaude.objects.all()
    serializer_class = AgendaProfissionalSaudeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = AgendaProfissionalSaudeFilter


class EspecialidadeViewSet(ModelViewSet):
    queryset = Especialidade.objects.all()
    serializer_class = EspecialidadeSerializer
    permission_classes = [IsAuthenticated]


class ProfissionalSaudeViewSet(ModelViewSet):
    serializer_class = ProfissionalSaudeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProfissionalSaude.objects.filter(idUsuario__username=self.request.user)
