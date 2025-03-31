from django.contrib import admin
from backend.atendimento.models.consulta import Consulta

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('status',)