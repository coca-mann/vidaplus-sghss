from django.apps import AppConfig


class AuditoriaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.auditoria'
    verbose_name = 'Auditoria'

    def ready(self):
        import backend.auditoria.models
