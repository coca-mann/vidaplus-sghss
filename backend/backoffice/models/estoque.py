from django.db import models
from backend.local.models import Local


class UnidadeMedida(models.Model):
    idUnidadeMedida = models.AutoField(
        primary_key=True,
        verbose_name='ID Unidade Medida'
    )
    nome = models.CharField(
        max_length=50,
        blank=False,
        verbose_name='Nome'
    )
    abreviacao = models.CharField(
        max_length=5,
        blank=False,
        verbose_name='Abreviado'
    )
    descricao = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name='Descrição'
    )


class Suprimento(models.Model):
    idSuprimento = models.AutoField(
        primary_key=True,
        verbose_name='ID Suprimento'
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
    idUnidadeMedida = models.ForeignKey(
        UnidadeMedida,
        on_delete=models.PROTECT,
        blank=False,
        verbose_name='Unidade de Medida',
        db_column='idUnidadeMedida'
    )
    estoqueMinimo = models.DecimalField(
        blank=False,
        verbose_name='Estoque mínimo (dec)'
    )


class EstoqueSuprimento(models.Model):
    idEstoque = models.AutoField(
        primary_key=True,
        verbose_name='ID Estoque'
    )
    idLocal = models.ForeignKey(
        Local,
        on_delete=models.PROTECT,
        verbose_name='Local',
        db_column='idLocal'
    )
    idSuprimento = models.ForeignKey(
        Suprimento,
        on_delete=models.PROTECT,
        verbose_name='Suprimento',
        db_column='idSuprimento'
    )
    quantidadeAtual = models.DecimalField(
        blank=False,
        verbose_name='Quantidade Atual'
    )