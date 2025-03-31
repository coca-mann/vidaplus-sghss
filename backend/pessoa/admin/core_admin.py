from django.contrib import admin
from ..models.core import Pessoa, Administrador

class PessoaInline(admin.StackedInline):
    model = Pessoa
    can_delete = False
    verbose_name_plural = 'Pessoa'
    fk_name = 'usuario'
    extra = 0
    max_num = 1

# Registre o model Administrador normalmente
@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ('idPessoa', 'cargo', 'idLocal')
    search_fields = ('idPessoa__nome', 'idLocal__nome', 'cargo')
    list_filter = ('cargo',)

# Registre o model Pessoa (se necessário, separadamente)
@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'dataNascimento', 'cpf', 'usuario') # Exemplo de campos
    search_fields = ('nome', 'cpf')

# Função para registrar o UserAdmin customizado após as apps serem carregadas
def register_custom_user_admin():
    from django.contrib.auth.models import User
    from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

    class CustomUserAdmin(DefaultUserAdmin):
        inlines = (PessoaInline, )

        def get_inline_instances(self, request, obj=None):
            if not obj:
                return []
            return super().get_inline_instances(request, obj)

    try:
        admin.site.unregister(User)
    except admin.sites.NotRegistered:
        pass  # Ignora se User não estiver registrado

    admin.site.register(User, CustomUserAdmin)