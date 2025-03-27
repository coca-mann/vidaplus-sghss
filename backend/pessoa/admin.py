from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import Pessoa, Administrador


class PessoaInline(admin.StackedInline):
    model = Pessoa
    can_delete = False
    verbose_name_plural = 'Pessoa'
    fk_name = 'usuario'
    extra = 0
    max_num = 1


class CustomUserAdmin(DefaultUserAdmin):
    inlines = (PessoaInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)
    

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ('idPessoa', 'cargo', 'idLocal')
    search_fields = ('idPessoa__nome', 'idLocal__nome', 'cargo')
    list_filter = ('cargo',)