from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
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
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class ProfissionalSaudeViewSet(ModelViewSet):
    serializer_class = ProfissionalSaudeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProfissionalSaude.objects.filter(idUsuario__username=self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_especialidades(self, request, pk=None):
        profissional = self.get_object()
        especialidades_ids = request.data.get('especialidades', [])

        especialidades = Especialidade.objects.filter(idEspecialidade__in=especialidades_ids)
        profissional.especialidades.add(*especialidades)

        return Response(ProfissionalSaudeSerializer(profissional).data)
    
    @action(detail=True, methods=['post'])
    def remove_especialidades(self, request, pk=None):
        profissional = self.get_object()
        especialidades_ids = request.data.get('especialidades', [])

        especialidades = Especialidade.objects.filter(idEspecialidade__in=especialidades_ids)
        profissional.especialidades.remove(*especialidades)

        return Response(ProfissionalSaudeSerializer(profissional).data)
