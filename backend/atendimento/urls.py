from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.atendimento.views.consulta import (ConsultaViewSet)
from backend.atendimento.views.exame import ExameViewSet


router = DefaultRouter()
router.register(r'consulta', ConsultaViewSet, basename='consulta')
router.register('exame', ExameViewSet, basename='exame')

urlpatterns = [
    path('', include(router.urls)),
]
