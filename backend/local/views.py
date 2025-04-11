from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from backend.local.models import Local
from backend.local.serializers import LocalSerializer
from backend.local.permissions import IsAdminOrReadOnly


class LocalViewSet(ModelViewSet):
    queryset = Local.objects.all()
    serializer_class = LocalSerializer
    permission_classes = [IsAdminOrReadOnly]
