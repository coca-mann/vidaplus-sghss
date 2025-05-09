from django.apps import AppConfig

class PessoaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.pessoa'
    verbose_name = 'Pessoa'

    def ready(self):
        import backend.pessoa.models
        import backend.pessoa.signals
