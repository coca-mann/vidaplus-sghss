from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from backend.atendimento.models.exame import Exame
from backend.atendimento.serializers.exame import ExameSerializer


class ExameViewSet(ModelViewSet):
    queryset = Exame.objects.all()
    serializer_class = ExameSerializer
    permission_classes = [IsAuthenticated]