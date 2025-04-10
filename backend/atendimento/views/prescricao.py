from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from backend.atendimento.models.prescricao import Prescricao
from backend.atendimento.serializers.prescricao import PrescricaoSerializer


class PrescricaoViewSet(ModelViewSet):
    queryset = Prescricao.objects.all()
    serializer_class = PrescricaoSerializer
    permission_classes = [IsAuthenticated]
