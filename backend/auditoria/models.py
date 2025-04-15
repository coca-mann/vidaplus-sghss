from django.db import models
from django.contrib.auth.models import User


STATUS_CONSENTIMENTO = [
    ('CONC', 'Concedido'),
    ('REVO', 'Revogado'),
]


class AuditoriaSistema(models.Model):
    idAuditoria = models.AutoField(
        primary_key=True,
        verbose_name='ID Auditoria'
    )
    idUsuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Usuário',
        db_column='idUsuario'
    )
    acaoRealizada = models.CharField(
        max_length=500,
        blank=False,
        verbose_name='Ação realizada'
    )
    dataHora = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data e hora'
    )
    ipOrigem = models.CharField(
        max_length=50,
        blank=False,
        verbose_name='Endereço IP'
    )
    detalhes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Detalhes'
    )


class ConsentimentoLGPD(models.Model):
    idConsentimento = models.AutoField(
        primary_key=True,
        verbose_name='ID Consentimento'
    )
    idUsuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Usuário',
        db_column='idUsuario'
    )
    dataConsentimento = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data e hora'
    )
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descrição'
    )
    statusConsentimento = models.CharField(
        max_length=10,
        choices=STATUS_CONSENTIMENTO,
        verbose_name='Status'
    )
