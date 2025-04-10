from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.atendimento.views.consulta import (
    ConsultaViewSet,
    AtendimentoConsultaViewSet
)
from backend.atendimento.views.exame import ExameViewSet
from backend.atendimento.views.prescricao import PrescricaoViewSet
from backend.atendimento.views.prontuario import ProntuarioViewSet


router = DefaultRouter()
router.register('consulta', ConsultaViewSet)
router.register('atendimentoconsulta', AtendimentoConsultaViewSet)
router.register('exame', ExameViewSet)
router.register('prescricao', PrescricaoViewSet)
router.register('prontuario', ProntuarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]