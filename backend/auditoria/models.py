from auditlog.registry import auditlog
from django.db import models
from django.contrib.auth.models import User


STATUS_CONSENTIMENTO = [
    ('CONC', 'Concedido'),
    ('REVO', 'Revogado'),
]


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


auditlog.register(ConsentimentoLGPD)
