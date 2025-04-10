from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.pessoa.views.core import AdministradorViewSet, PessoaViewSet
from backend.pessoa.views.paciente import PacienteViewSet
from backend.pessoa.views.saude import (
    AgendaProfissionalSaudeViewSet,
    EspecialidadeViewSet,
    ProfissionalSaudeViewSet
)


router = DefaultRouter()
router.register('administrador', AdministradorViewSet)
router.register('pessoa', PessoaViewSet)
router.register('paciente', PacienteViewSet)
router.register('agendaprofsaude', AgendaProfissionalSaudeViewSet)
router.register('especialidadeprofsaude', EspecialidadeViewSet)
router.register('profissionalsaude', ProfissionalSaudeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
