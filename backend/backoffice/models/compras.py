from django.db import models
from backend.local.models import Local
from .estoque import Suprimento


STATUS_PEDIDO = [
    ('ABER', 'Aberto'),
    ('ENVI', 'Enviado'),
    ('RECE', 'Recebido'),
    ('CANC', 'Cancelado'),
]


class Fornecedor(models.Model):
    idFornecedor = models.AutoField(
        primary_key=True,
        verbose_name='ID Fornecedor'
    )
    nomeFantasia = models.CharField(
        max_length=255,
        blank=False,
        verbose_name='Nome Fantasia'
    )
    razaoSocial = models.CharField(
        max_length=255,
        blank=False,
        verbose_name='Razão Social'
    )
    cpfCnpj = models.CharField(
        max_length=14,
        blank=False,
        verbose_name='CPF/CNPJ'
    )
    telefone = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        verbose_name='Telefone/Celular'
    )
    email = models.EmailField(
        blank=False,
        verbose_name='E-mail'
    )
    endereço = models.TextField(
        blank=False,
        verbose_name='Endereço'
    )


    class Meta:
        db_table = 'backoffice_compras_fornecedor'


class PedidoCompra(models.Model):
    idPedido = models.AutoField(
        primary_key=True,
        verbose_name='ID Pedido'
    )
    idFornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.PROTECT,
        verbose_name='Fornecedor',
        db_column='idFornecedor'
    )
    idLocal = models.ForeignKey(
        Local,
        on_delete=models.PROTECT,
        verbose_name='Local',
        db_column='idLocal'
    )
    dataHoraPedido = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data e Hora do Pedido'
    )
    dataEntregaPrevista = models.DateField(
        blank=True,
        null=True,
        verbose_name='Data prevista de entrega'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_PEDIDO,
        blank=False,
        verbose_name='Status'
    )
    valorTotal = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        blank=False,
        verbose_name='Valor Total'
    )
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observações'
    )


    class Meta:
        db_table = 'backoffice_compras_pedidocompra'


class ItemPedidoCompra(models.Model):
    idItemPedido = models.AutoField(
        primary_key=True,
        verbose_name='ID Item do Pedido'
    )
    idPedido = models.ForeignKey(
        PedidoCompra,
        on_delete=models.PROTECT,
        verbose_name='Pedido',
        db_column='idPedido'
    )
    idSuprimento = models.ForeignKey(
        Suprimento,
        on_delete=models.PROTECT,
        verbose_name='Suprimento',
        db_column='idSuprimento'
    )
    valorUnitario = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        blank=False,
        verbose_name='Valor Unitário'
    )
    quantidade = models.IntegerField(
        blank=False,
        verbose_name='Quantidade'
    )


    class Meta:
        db_table = 'backoffice_compras_itempedidocompra'