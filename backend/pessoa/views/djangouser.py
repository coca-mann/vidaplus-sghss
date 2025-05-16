from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.contrib.auth.models import User
from backend.pessoa.serializers.djangouser import (
    UserRegistrationSerializer,
    UserProfileViewSet
)

@extend_schema_view(
    list=extend_schema(
        summary="Listar usuários",
        description="Retorna todos os usuários cadastrados. Apenas administradores podem acessar.",
        tags=["Usuários"],
    ),
    retrieve=extend_schema(
        summary="Detalhar usuário",
        description="Retorna os detalhes de um usuário específico pelo seu ID. Apenas administradores podem acessar.",
        tags=["Usuários"],
    ),
    create=extend_schema(
        summary="Cadastrar usuário",
        description="Permite cadastrar um novo usuário no sistema. Apenas administradores podem acessar.",
        tags=["Usuários"],
    ),
    update=extend_schema(
        summary="Atualizar usuário",
        description="Atualiza todos os dados de um usuário existente. Apenas administradores podem acessar.",
        tags=["Usuários"],
    ),
    partial_update=extend_schema(
        summary="Atualizar parcialmente usuário",
        description="Atualiza parcialmente os dados de um usuário existente. Apenas administradores podem acessar.",
        tags=["Usuários"],
    ),
    destroy=extend_schema(
        summary="Remover usuário",
        description="Remove um usuário do sistema. Apenas administradores podem acessar.",
        tags=["Usuários"],
    ),
)
class UserRegistrationViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [IsAdminUser]

@extend_schema_view(
    list=extend_schema(
        summary="Listar perfil do usuário autenticado",
        description="Retorna os dados do perfil do usuário autenticado.",
        tags=["Perfil do Usuário"],
    ),
    retrieve=extend_schema(
        summary="Detalhar perfil do usuário autenticado",
        description="Retorna os detalhes do perfil do usuário autenticado.",
        tags=["Perfil do Usuário"],
    ),
    update=extend_schema(
        summary="Atualizar perfil do usuário autenticado",
        description="Atualiza todos os dados do perfil do usuário autenticado.",
        tags=["Perfil do Usuário"],
    ),
    partial_update=extend_schema(
        summary="Atualizar parcialmente perfil do usuário autenticado",
        description="Atualiza parcialmente os dados do perfil do usuário autenticado.",
        tags=["Perfil do Usuário"],
    ),
)
class UserProfileViewSet(ModelViewSet):
    serializer_class = UserProfileViewSet
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    

    def get_object(self):
        return self.request.user
