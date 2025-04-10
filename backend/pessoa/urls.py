from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.pessoa.views.core import AdministradorViewSet, PessoaViewSet


router = DefaultRouter()
router.register('administrador', AdministradorViewSet)
router.register('pessoa', PessoaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
