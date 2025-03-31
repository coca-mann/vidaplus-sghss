from django.contrib import admin
from ..models.paciente import Paciente

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('idPaciente','get_id_local','get_nome_pessoa', 'get_data_nascimento')
    search_fields = ('idPessoa__nome', 'idPessoa__cpf', 'idLocal__nome')

    def get_id_local(self, obj):
        return obj.idLocal.nome if obj.idLocal else '-'
    get_id_local.short_description = 'Local'

    def get_nome_pessoa(self, obj):
        return obj.idPessoa.nome if obj.idPessoa else '-'
    get_nome_pessoa.short_description = 'Nome Paciente'

    def get_data_nascimento(self, obj):
        return obj.idPessoa.dataNascimento if obj.idPessoa else '-'
    get_data_nascimento.short_description = 'Data Nascimento Paciente'