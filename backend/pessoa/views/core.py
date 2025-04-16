from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from backend.pessoa.models.core import Administrador
from backend.pessoa.serializers.core import AdministradorSerializer


class AdministradorViewSet(ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer
    permission_classes = [IsAuthenticated]
