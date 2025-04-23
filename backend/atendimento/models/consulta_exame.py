from django.db import models
from backend.atendimento.models.consulta import Consulta
from backend.atendimento.models.exame import Exame
from auditlog.registry import auditlog


class ConsultaExame(models.Model):
    idConsulta = models.ForeignKey(
        Consulta,
        on_delete=models.PROTECT,
        verbose_name='ID Consulta',
        db_column='idConsulta',
        related_name='exames_relacionados'
    )
    idExame = models.ForeignKey(
        Exame,
        on_delete=models.PROTECT,
        verbose_name='ID Exame',
        db_column='idExame',
        related_name='consultas_relacionadas'
    )

    def __str__(self):
        return f"Consulta: {self.idConsulta.idConsulta} - Exame: {self.idExame.idExame}"
    
    class Meta:
        db_table = 'atendimento_consulta_exame'

auditlog.register(ConsultaExame)
