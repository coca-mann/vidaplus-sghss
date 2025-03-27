from django.db import models
from django.contrib.auth.models import User


class Pessoa(models.Model):
    idPessoa = models.AutoField(
        primary_key=True
    )
    nome = models.CharField(
        max_length=255,
        blank=False,
        verbose_name='Nome'
    )
    dataNascimento = models.DateField(
        blank=False,
        verbose_name='Data de Nascimento'
    )
    telefone = models.CharField(
        max_length=11,
        blank=False,
        verbose_name='Telefone'
    )
    endereco = models.CharField(
        max_length=1000,
        blank=False,
        verbose_name='Endereço'
    )
    cpf = models.CharField(
        max_length=14,
        blank=False,
        verbose_name='CPF',
        unique=True
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='E-mail'
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Usuário do sistema',
        related_name='pessoas'
    )

    def __str__(self):
        return self.nome