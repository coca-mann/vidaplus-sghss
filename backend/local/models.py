from auditlog.registry import auditlog
from django.db import models

TIPO_LOCAL = [
    ('HOSPITAL', 'Hospital'),
    ('CLINICA', 'Clínica'),
]


class Local(models.Model):
    idLocal = models.AutoField(
        primary_key=True
    )
    nome = models.CharField(
        max_length=255,
        blank=False,
        verbose_name='Nome'
    )
    cnpj = models.CharField(
        max_length=14,
        blank=False,
        verbose_name='CNPJ'
    )
    endereco = models.CharField(
        max_length=1000,
        blank=False,
        verbose_name='Endereço'
    )
    tipoLocal = models.CharField(
        max_length=50,
        choices=TIPO_LOCAL,
        blank=False,
        verbose_name='Tipo Local'
    )
    telefone = models.CharField(
        max_length=11,
        blank=False,
        verbose_name='Telefone'
    )

    def __str__(self):
        return f"{self.nome} - {self.cnpj}"
    
    class Meta:
        verbose_name = 'Local'
        verbose_name_plural = 'Locais'


auditlog.register(Local)
