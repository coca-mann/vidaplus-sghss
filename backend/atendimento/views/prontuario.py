from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from backend.atendimento.models.prontuario import Prontuario
from backend.atendimento.serializers.prontuario import ProntuarioSerializer


class ProntuarioViewSet(ModelViewSet):
    queryset = Prontuario.objects.all()
    serializer_class = ProntuarioSerializer
    permission_classes = [IsAuthenticated]
