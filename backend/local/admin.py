from django.contrib import admin
from .models import Local

@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = (
        'idLocal',
        'tipoLocal',
        'nome',
        'cnpj',
        'endereco',
    )
    search_fields = (
        'nome',
        'cnpj',
    )
    list_filter = (
        'tipoLocal',
    )