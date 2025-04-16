from auditlog.registry import auditlog
from django.db import models
from backend.local.models import Local
from backend.pessoa.models.paciente import Paciente
from backend.pessoa.models.saude import ProfissionalSaude
from .prontuario import Prontuario


STATUS_ATENDIMENTO = [
    ('AGEN', 'Agendada'),
    ('REAL', 'Realizada'),
    ('CANC', 'Cancelada'),
]


TIPO_ATENDIMENTO = [
    ('PRES', 'Presencial'),
    ('TELE', 'Teleconsulta'),
]


class Consulta(models.Model):
    idConsulta = models.AutoField(
        primary_key=True,
        verbose_name='ID Consulta'
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
    idProfissional = models.ForeignKey(
        ProfissionalSaude,
        on_delete=models.PROTECT,
        verbose_name='Médico',
        db_column='idProfissional'
    )
    idProntuario = models.ForeignKey(
        Prontuario,
        on_delete=models.PROTECT,
        verbose_name='Prontuário',
        db_column='idProntuario',
        null=True,
        blank=True
    )
    dataHoraConsulta = models.DateTimeField(
        blank=False,
        verbose_name='Data e Hora'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_ATENDIMENTO,
        blank=False,
        verbose_name='Status'
    )
    tipoAtendimento = models.CharField(
        max_length=10,
        blank=False,
        choices=TIPO_ATENDIMENTO,
        verbose_name='Tipo de Atendimento'
    )
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observações'
    )
    linkTeleconsulta = models.CharField(
        max_length=500,
        verbose_name='Link Teleconsulta',
        blank=True,
        null=True
    )
    sintomas = models.TextField(
        blank=False,
        verbose_name='Sintomas'
    )
    diagnostico = models.TextField(
        blank=True,
        null=True,
        verbose_name='Diagnóstico'
    )
    medicamentoPrescritos = models.JSONField(
        blank=True,
        null=True,
        verbose_name='Medicamentos Preescritos'
    )
    examesSolicitados = models.JSONField(
        blank=True,
        null=True,
        verbose_name='Exames Solicitados'
    )
    dataHoraAtendimento = models.DateTimeField(
        blank=False,
        verbose_name='Data e Hora do Atendimento'
    )


auditlog.register(Consulta)
