from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from backend.backoffice.models.gestaohospitalar import (
    Ala,
    Leito,
    LogOcupacaoLeito
)
from backend.backoffice.serializers.gestaohospitalar import (
    AlaSerializer,
    LeitoSerializer,
    LogOcupacaoLeitoSerializer
)
from backend.backoffice.permissions import AlaPermission
from backend.pessoa.models.core import Administrador
from backend.pessoa.models.saude import ProfissionalSaude


'''
ALA
- Somente administradores podem editar alas
- Médicos podem ver alas com leitos ocupados
- Pacientes não podem ver alas
'''
class AlaViewSet(ModelViewSet):
    serializer_class = AlaSerializer
    permission_classes = [IsAuthenticated, AlaPermission]

    def get_queryset(self):
        user = self.request.user

        if Administrador.objects.filter(idUsuario=user).exists():
            return Ala.objects.all()
        
        if ProfissionalSaude.objects.filter(idUsuario=user).exists():
            alas_com_leitos_ocupados = Leito.objects.filter(status='OCUP').values_list('idAla', flat=True).distinct()

            return Ala.objects.filter(idAla__in=alas_com_leitos_ocupados)
        
        return Ala.objects.none()


'''
LEITOS
- Somente administradores podem editar leitos
- Médicos podem ver detalhes dos pacientes nos leitos
'''
class LeitoViewSet(ModelViewSet):
    queryset = Leito.objects.all()
    serializer_class = LeitoSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):

        context = super().get_serializer_context()
        user = self.request.user

        context['mostrar_detalhes_paciente'] = (
            Administrador.objects.filter(idUsuario=user).exists() or
            ProfissionalSaude.objects.filter(idUsuario=user).exists()
        )

        return context


'''
LOG LEITOS
- Médicos podem internar pacientes, e liberar leitos
- Administradores não podem internar nem liberar leitos
- Pacientes podem ver apenas seus próprios leitos ocupado
'''
class LogOcupacaoLeitoViewSet(ModelViewSet):
    queryset = LogOcupacaoLeito.objects.all()
    serializer_class = LogOcupacaoLeitoSerializer
    permission_classes = [IsAuthenticated]
