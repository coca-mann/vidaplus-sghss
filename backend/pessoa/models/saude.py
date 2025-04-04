from django.db import models
from backend.local.models import Local
from backend.pessoa.models.core import Pessoa


STATUS_DISPONIBILIDADE = [
    ('DISP', 'Disponível'),
    ('INDISP', 'Indisponível'),
    ('RES', 'Reservado'),
]


class Especialidade(models.Model):
    idEspecialidade = models.AutoField(
        primary_key=True,
        verbose_name='ID Especialidade'
    )
    nome = models.CharField(
        max_length=255,
        blank=False,
        verbose_name='Nome'
    )
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descrição'
    )

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Especialidade'
        verbose_name_plural = 'Especialidades'


    class Meta:
        db_table = 'pessoa_profissionalsaude_especialidade'


class ProfissionalSaude(models.Model):
    idProfissional = models.AutoField(
        primary_key=True,
        verbose_name='ID Profissional'
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
    registroProfissional = models.CharField(
        max_length=30,
        blank=False,
        verbose_name='Nº registro profissional'
    )
    especialidades = models.ManyToManyField(
        Especialidade,
        related_name='profissionais',
        verbose_name='Especialidades'
    )

    def __str__(self):
        return f"{self.idPessoa.nome}"
    
    class Meta:
        verbose_name = 'Profissional de Saude'
        verbose_name_plural = 'Profissionais de Saude'


class AgendaProfissionalSaude(models.Model):
    idAgenda = models.AutoField(
        primary_key=True,
        verbose_name='ID Agenda'
    )
    idLocal = models.ForeignKey(
        Local,
        on_delete=models.PROTECT,
        verbose_name='Local'
    )
    idProfissional = models.ForeignKey(
        ProfissionalSaude,
        on_delete=models.PROTECT,
        verbose_name='Profissional de Saude'
    )
    dataHoraInicio = models.DateTimeField(
        blank=False,
        verbose_name='Data e Hora inicial'
    )
    dataHoraFim = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Data e Hora final'
    )
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observações'
    )
    disponibilidade = models.CharField(
        choices=STATUS_DISPONIBILIDADE,
        max_length=20,
        blank=False,
        verbose_name='Disponibilidade'
    )

    def __str__(self):
        return f"{self.idProfissional.idPessoa.nome} - {self.dataHoraInicio}"
    
    class Meta:
        verbose_name = 'Agenda do Profissional'
        verbose_name_plural = 'Agendas dos Profissionais'


    class Meta:
        db_table = 'pessoa_profissionalsaude_agenda'