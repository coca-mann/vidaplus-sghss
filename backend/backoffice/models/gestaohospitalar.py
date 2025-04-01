from django.db import models
from backend.local.models import Local
from backend.pessoa.models.paciente import Paciente


STATUS_LEITO = [
    ('DISP', 'Disponível'),
    ('OCUP', 'Ocupado'),
    ('HIGI', 'Higienização'),
    ('MANU', 'Manutenção'),
]


class Ala(models.Model):
    idAla = models.AutoField(
        primary_key=True,
        verbose_name='Ala'
    )
    idLocal = models.ForeignKey(
        Local,
        on_delete=models.PROTECT,
        verbose_name='Local',
        db_column='idLocal'
    )
    nome = models.CharField(
        max_length=50,
        blank=False,
        verbose_name='Nome'
    )
    descricao = models.TextField(
        blank=True,
        null=False,
        verbose_name='Descrição'
    )


    class Meta:
        db_table = 'backoffice_gestaohospitalar_ala'


class Leito(models.Model):
    idLeito = models.AutoField(
        primary_key=True,
        verbose_name='ID Leito'
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
    idAla = models.ForeignKey(
        Ala,
        on_delete=models.PROTECT,
        verbose_name='Ala',
        db_column='idAla'
    )
    numeroLeito = models.CharField(
        max_length=5,
        blank=False,
        verbose_name='Número do Leito'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_LEITO,
        blank=False,
        verbose_name='Status'
    )
    observacao = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observação'
    )


    class Meta:
        db_table = 'backoffice_gestaohospitalar_leito'


class LogOcupacaoLeito(models.Model):
    idLogOcupLeito = models.AutoField(
        primary_key=True,
        verbose_name='ID Log'
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
    idLeito = models.ForeignKey(
        Leito,
        on_delete=models.PROTECT,
        verbose_name='Leito',
        db_column='idLeito'
    )
    dataHoraEntrada = models.DateTimeField(
        blank=False,
        verbose_name='Data/Hora Entrada'
    )
    dataHoraSaida = models.DateTimeField(
        blank=False,
        verbose_name='Data/Hora Saída'
    )
    motivoInternacao = models.TextField(
        blank=False,
        verbose_name='Motivo da Internação'
    )
    observacao = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observação'
    )


    class Meta:
        db_table = 'backoffice_gestaohospitalar_logocupacaoleito'