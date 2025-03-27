from django.db import models
from django.contrib.auth.models import User
from backend.local.models import Local


CARGO = [
    ('DIRGERAL', 'Diretor Geral'),
    ('DIRFINAN', 'Diretor Financeiro'),
    ('DIRADMIN', 'Diretor Administrativo'),
    ('GESTOR', 'Gestor'),
    ('LIDER', 'Lider'),
]

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
    

class Administrador(models.Model):
    idPessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Pessoa'
    )
    idLocal = models.ForeignKey(
        Local,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Local'
    )
    cargo = models.CharField(
        max_length=50,
        choices=CARGO,
        blank=False,
        verbose_name='Cargo'
    )

    def __str__(self):
        return f"{self.idPessoa.nome} {self.cargo} de {self.idLocal.nome}"
    
    
    class Meta:
        verbose_name = 'Administrador'
        verbose_name_plural = 'Administradores'