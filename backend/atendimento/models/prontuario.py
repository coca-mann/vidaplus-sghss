from django.db import models
from backend.local.models import Local
from backend.pessoa.models.paciente import Paciente


class Prontuario(models.Model):
    idProntuario = models.AutoField(
        primary_key=True,
        verbose_name='ID Prontuário'
    )
    idLocal = models.ForeignKey(
        Local,
        on_delete=models.PROTECT,
        verbose_name='Local',
        db_column='idLocal'
    )
    idPaciente = models.ForeignKey(
        Paciente,
        on_delete=models.PROTECT,
        verbose_name='Paciente',
        db_column='idPaciente'
    )
    historicoClinico = models.JSONField(
        null=True,
        blank=True,
        verbose_name='Histórico Clínico'
    )