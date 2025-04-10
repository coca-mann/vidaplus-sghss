from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.atendimento.views.consulta import (
    ConsultaViewSet,
    AtendimentoConsultaViewSet
)

router = DefaultRouter()
router.register('consultas', ConsultaViewSet)
router.register('atendimentoconsultas', AtendimentoConsultaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]