from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from backend.pessoa.permissions.pessoa import IsAdministradorWithPermission
from backend.pessoa.models.core import Administrador, Pessoa
from backend.pessoa.serializers.core import AdministradorSerializer, PessoaSerializer


class AdministradorViewSet(ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer
    permission_classes = [IsAdministradorWithPermission]


class PessoaViewSet(ModelViewSet):
    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer
    permission_classes = [IsAdministradorWithPermission]
