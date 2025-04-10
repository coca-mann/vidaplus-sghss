from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.atendimento.views.consulta import (
    ConsultaViewSet,
    AtendimentoConsultaViewSet
)
from backend.atendimento.views.exame import ExameViewSet
from backend.atendimento.views.prescricao import PrescricaoViewSet


router = DefaultRouter()
router.register('consultas', ConsultaViewSet)
router.register('atendimentoconsultas', AtendimentoConsultaViewSet)
router.register('exames', ExameViewSet)
router.register('prescricao', PrescricaoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]