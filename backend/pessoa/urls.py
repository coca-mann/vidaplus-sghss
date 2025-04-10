from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.pessoa.views.core import AdministradorViewSet, PessoaViewSet
from backend.pessoa.views.paciente import PacienteViewSet


router = DefaultRouter()
router.register('administrador', AdministradorViewSet)
router.register('pessoa', PessoaViewSet)
router.register('paciente', PacienteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
