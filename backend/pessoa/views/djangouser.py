from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth.models import User
from backend.pessoa.serializers.djangouser import (
    UserRegistrationSerializer,
    UserProfileViewSet
)


class UserRegistrationViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [IsAdminUser]


class UserProfileViewSet(ModelViewSet):
    serializer_class = UserProfileViewSet
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    

    def get_object(self):
        return self.request.user
