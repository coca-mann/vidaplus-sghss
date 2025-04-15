from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.pessoa.views.core import AdministradorViewSet
from backend.pessoa.views.paciente import PacienteViewSet
from backend.pessoa.views.saude import (
    AgendaProfissionalSaudeViewSet,
    EspecialidadeViewSet,
    ProfissionalSaudeViewSet
)
from backend.pessoa.views.djangouser import (
    UserRegistrationViewSet,
    UserProfileViewSet
)


router = DefaultRouter()
router.register('administrador', AdministradorViewSet)
router.register('paciente', PacienteViewSet)
router.register('agendaprofsaude', AgendaProfissionalSaudeViewSet)
router.register('especialidadeprofsaude', EspecialidadeViewSet)
router.register('profissionalsaude', ProfissionalSaudeViewSet)
router.register('auth/register', UserRegistrationViewSet)
router.register('auth/profile', UserProfileViewSet, basename='userprofile')

urlpatterns = [
    path('', include(router.urls)),
]
