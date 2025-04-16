from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from backend.pessoa.models.paciente import Paciente
from backend.pessoa.serializers.paciente import PacienteSerializer


class PacienteViewSet(ModelViewSet):
    serializer_class = PacienteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Paciente.objects.filter(idUsuario=self.request.user)
