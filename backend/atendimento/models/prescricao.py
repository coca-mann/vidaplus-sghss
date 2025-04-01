from django.db import models
from backend.local.models import Local
from backend.pessoa.models.paciente import Paciente
from backend.pessoa.models.saude import ProfissionalSaude
from .consulta import Consulta


class Prescricao(models.Model):
    idPrescricao = models.AutoField(
        primary_key=True,
        verbose_name='ID Prescrição'
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
        verbose_name='Profissional',
        db_column='idProfissional'
    )
    idConsulta = models.ForeignKey(
        Consulta,
        on_delete=models.PROTECT,
        verbose_name='Consulta',
        db_column='idConsulta'
    )
    medicamentos = models.JSONField(
        blank=True,
        null=True,
        verbose_name='Medicamentos'
    )
    recomendacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Recomendações'
    )
    dataEmissao = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Emissão'
    )
    validadePrescricao = models.DateField(
        blank=True,
        null=True,
        verbose_name='Validade'
    )
    assinaturaDigital = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name='Assinatura Digital'
    )