from django.db import models
from backend.local.models import Local
from backend.backoffice.models.compras import Fornecedor


FORMA_PAGAMENTO = [
    ('PIX', 'PIX'),
    ('DINH', 'Dinheiro'),
    ('CARC', 'Cartão de Crédito'),
    ('CARD', 'Cartão de Débito'),
    ('BOLE', 'Boleto'),
    ('TED', 'Transferência Bancária TED'),
]


TIPO_CATEGORIA = [
    ('REC', 'Receita'),
    ('DES', 'Despesa'),
]


class CategoriaFinanceira(models.Model):
    idCategoria = models.AutoField(
        primary_key=True,
        verbose_name='ID Categoria'
    )
    nome = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Nome'
    )
    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CATEGORIA,
        verbose_name='Tipo de Categoria'
    )
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descrição'
    )


    class Meta:
        db_table = 'backoffice_financeiro_categoriafinanceira'


class LancamentoFinanceiro(models.Model):
    idLancamento = models.AutoField(
        primary_key=True,
        verbose_name='ID Lançamento Financeiro'
    )
    idLocal = models.ForeignKey(
        Local,
        on_delete=models.PROTECT,
        verbose_name='Local',
        db_column='idLocal'
    )
    idCategoria = models.ForeignKey(
        CategoriaFinanceira,
        on_delete=models.PROTECT,
        verbose_name='Categoria do Lançamento',
        db_column='idCategoria'
    )
    idFornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.PROTECT,
        verbose_name='Fornecedor',
        db_column='idFornecedor'
    )
    dataLancamento = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data/hora do Lançamento'
    )
    valor = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        blank=False,
        verbose_name='Valor'
    )
    formaPagamento = models.CharField(
        max_length=10,
        choices=FORMA_PAGAMENTO,
        blank=False,
        verbose_name='Forma de Pagamento'
    )


    class Meta:
        db_table = 'backoffice_financeiro_lancamentofinanceiro'
