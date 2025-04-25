from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from backend.backoffice.models.gestaohospitalar import (
    Ala,
    Leito,
    LogOcupacaoLeito
)
from backend.pessoa.models.core import Administrador
from backend.pessoa.models.saude import ProfissionalSaude
from backend.pessoa.models.paciente import Paciente


class AlaPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        is_administrador = Administrador.objects.filter(idUsuario=user).exists()

        is_profissional = ProfissionalSaude.objects.filter(idUsuario=user).exists()

        if is_administrador:
            return True
        
        if is_profissional:
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        user = request.user

        is_administrador = Administrador.objects.filter(idUsuario=user).exists()

        is_profissional = ProfissionalSaude.objects.filter(idUsuario=user).exists()

        if is_administrador:
            return True
        
        if is_profissional and request.method in ['GET', 'HEAD', 'OPTIONS']:

            leitos_ocupados = Leito.objects.filter(
                idAla=obj.idAla,
                ocupado=True
            ).exists()

            return leitos_ocupados
        
        return False


class LeitoPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        is_administrador = Administrador.objects.filter(idUsuario=user).exists()

        is_profissional = ProfissionalSaude.objects.filter(idUsuario=user).exists()

        if is_administrador:
            return True
        
        if is_profissional:
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        user = request.user

        is_administrador = Administrador.objects.filter(idUsuario=user).exists()

        is_profissional = ProfissionalSaude.objects.filter(idUsuario=user).exists()

        is_paciente = Paciente.objects.filter(idUsuario=user).exists()

        if is_administrador:
            return True
        
        if is_profissional and request.method in ['GET', 'HEAD', 'OPTIONS']:

            return True
        
        if is_paciente and request.method in ['GET', 'HEAD', 'OPTIONS']:
            leitos_ocupados_pelo_paciente = LogOcupacaoLeito.objects.filter(idPaciente=is_paciente).exists()

            return leitos_ocupados_pelo_paciente
        
        return False


class IsAdminOrManager(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        ADMIN_TYPES = ['DIRFINAN', 'DIRGERAL', 'DIRADMIN', 'GESTOR']

        if request.user.is_superuser:
            return True
        
        try:
            administrador = Administrador.objects.get(idUsuario=request.user)
            return administrador.cargo in ADMIN_TYPES
        except Administrador.DoesNotExist:
            return False
