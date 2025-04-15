from django.db import models
from backend.local.models import Local


class Paciente(models.Model):
    idPaciente = models.AutoField(
        primary_key=True,
        verbose_name='ID Paciente'
    )
    idLocal = models.ForeignKey(
        Local,
        on_delete=models.PROTECT,
        verbose_name='Local',
        db_column='idLocal'
    )
    nome = models.CharField(
        max_length=255,
        blank=False,
        verbose_name='Nome do Paciente'
    )
    cpf = models.CharField(
        max_length=11,
        blank=False,
        verbose_name='CPF'
    )
    dataNascimento = models.DateField(
        blank=False,
        verbose_name='Data de Nascimento'
    )
    telefone = models.CharField(
        max_length=14,
        blank=False,
        verbose_name='Telefone'
    )
    endereco = models.CharField(
        max_length=500,
        blank=False,
        verbose_name='Endereço'
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='E-mail'
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
        verbose_name='Convênio'
    )

    def __str__(self):
        return f"{self.idPessoa.nome}"
    
    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
