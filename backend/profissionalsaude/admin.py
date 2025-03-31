from django.contrib import admin
from .models import ProfissionalSaude, Especialidade, AgendaProfissionalSaude

@admin.register(ProfissionalSaude)
class ProfissionalSaudeAdmin(admin.ModelAdmin):
    list_display = (
        'idProfissional',
        'get_id_local',
        'get_nome_pessoa',
        'registroProfissional',
        'get_especialidades'
    )
    search_fields = (
        'idPessoa__nome',
        'idEspecialidade__nome'
    )
    list_filter = ('especialidades',)

    def get_id_local(self, obj):
        return obj.idLocal.nome if obj.idLocal else '-'
    get_id_local.short_description = 'Local'

    def get_nome_pessoa(self, obj):
        return obj.idPessoa.nome if obj.idPessoa else '-'
    get_nome_pessoa.short_description = 'Nome'

    def get_especialidades(self, obj):
        return ", ".join([e.nome for e in obj.especialidades.all()])
    get_especialidades.short_description = 'Especialidades'


@admin.register(Especialidade)
class ProfissionalEspecialidade(admin.ModelAdmin):
    list_display = ('idEspecialidade', 'nome', 'descricao')
    search_fields = ('nome',)