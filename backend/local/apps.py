from django.apps import AppConfig


class LocalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.local'
    verbose_name = 'Local'

    def ready(self):
        import backend.local.models
