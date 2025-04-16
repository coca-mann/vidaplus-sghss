from auditlog.registry import auditlog
from django.db import models
from backend.local.models import Local
from backend.pessoa.models.paciente import Paciente
from backend.pessoa.models.saude import ProfissionalSaude
from .consulta import Consulta


STATUS_EXAME = [
    ('SOLI', 'Solicitado'),
    ('REAL', 'Realizado'),
    ('CANC', 'Cancelado'),
]


class Exame (models.Model):
    idExame = models.AutoField(
        primary_key=True,
        verbose_name='ID Exame'
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
    idProfissionalSolicitante = models.ForeignKey(
        ProfissionalSaude,
        on_delete=models.PROTECT,
        verbose_name='Profissional Solicitante',
        db_column='idProfissionalSolicitante'
    )
    idConsulta = models.ForeignKey(
        Consulta,
        on_delete=models.PROTECT,
        verbose_name='Consulta',
        db_column='idConsulta'
    )
    tipoExame = models.CharField(
        max_length=255,
        blank=False,
        verbose_name='Tipo de Exame'
    )
    dataSolicitacao = models.DateTimeField(
        blank=False,
        verbose_name='Data e Hora de Solicitação'
    )
    dataRealizacao = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Data e Hora de Realização'
    )
    resultadoExame = models.JSONField(
        blank=True,
        verbose_name='Resultado do Exame'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_EXAME,
        blank=False,
        verbose_name='Status'
    )
    

auditlog.register(Exame)
