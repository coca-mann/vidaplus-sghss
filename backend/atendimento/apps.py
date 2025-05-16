from django.apps import AppConfig


class AtendimentoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.atendimento'
    verbose_name = 'Atendimento'

    def ready(self):
        try:
            import backend.atendimento.models.consulta
            import backend.atendimento.models.exame
            import backend.atendimento.models.consulta_exame
        except ImportError as e:
            print(f"Erro ao importar modelos: {e}")
