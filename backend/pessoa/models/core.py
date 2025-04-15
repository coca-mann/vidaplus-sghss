from django.db import models
from backend.local.models import Local


CARGO = [
    ('DIRGERAL', 'Diretor Geral'),
    ('DIRFINAN', 'Diretor Financeiro'),
    ('DIRADMIN', 'Diretor Administrativo'),
    ('GESTOR', 'Gestor'),
    ('LIDER', 'Lider'),
]
    

class Administrador(models.Model):
    idLocal = models.ForeignKey(
        Local,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Local',
        db_column='idLocal'
    )
    cargo = models.CharField(
        max_length=50,
        choices=CARGO,
        blank=False,
        verbose_name='Cargo'
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

    def __str__(self):
        return f"{self.idPessoa.nome} {self.cargo} de {self.idLocal.nome}"
    
    
    class Meta:
        verbose_name = 'Administrador'
        verbose_name_plural = 'Administradores'
