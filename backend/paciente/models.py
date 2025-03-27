from django.db import models
from backend.local.models import Local
from backend.pessoa.models import Pessoa


class Paciente(models.Model):
    idPaciente = models.AutoField(
        primary_key=True,
        verbose_name='ID Paciente'
    )
    idPessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.PROTECT,
        verbose_name='Pessoa',
        db_column='idPessoa'
    )
    idLocal = models.ForeignKey(
        Local,
        on_delete=models.PROTECT,
        verbose_name='Local',
        db_column='idLocal'
    )
    nomeContato = models.CharField(
        max_length=255,
        blank=False,
        verbose_name='Nome de outro Contato do Paciente'
    )
    telefoneContato = models.CharField(
        max_length=11,
        blank=False,
        verbose_name='Telefone de outro Contato do Paciente'
    )
    fichaMedica = models.JSONField(
        null=True,
        blank=True,
        verbose_name='Ficha médica'
    )
    convenio = models.JSONField(
        null=True,
        blank=True,
        verbose_name='Ficha médica'
    )

    def __str__(self):
        return f"{self.idPessoa.nome}"
    
    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'