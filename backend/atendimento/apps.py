from django.apps import AppConfig


class AtendimentoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.atendimento'
    verbose_name = 'Atendimento'

    def ready(self):
        import backend.atendimento.models
