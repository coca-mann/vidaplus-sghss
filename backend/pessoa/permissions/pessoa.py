from rest_framework.permissions import BasePermission
from backend.pessoa.models.core import Administrador


class IsAdministradorWithPermission(BasePermission):


    def has_permission(self, request, view):
        admin = Administrador.objects.filter(idPessoa__usuario=request.user).first()

        if admin and admin.cargo in ['DIRGERAL', 'GESTOR', 'LIDER']:
            return True

        if not request.user.is_authenticated:
            return False
        
        if request.user.is_staff:
            return True

        return Administrador.objects.filter(idPessoa__usuario=request.user).exists()
