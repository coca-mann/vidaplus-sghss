# backend/pessoa/apps.py

from django.apps import AppConfig

class PessoaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.pessoa'
    verbose_name = 'Pessoa'

    def ready(self):
        from .admin import core_admin, saude_admin, paciente_admin
        if hasattr(core_admin, 'register_custom_user_admin'):
            core_admin.register_custom_user_admin()
