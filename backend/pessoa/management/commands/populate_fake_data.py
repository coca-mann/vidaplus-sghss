from django.core.management.base import BaseCommand
from faker import Faker
import random
from datetime import timedelta, date
from django.utils import timezone
from django.utils.timezone import make_aware
from django.contrib.auth.models import User, Group

# Importação dos modelos
from backend.local.models import Local
from backend.pessoa.models.paciente import Paciente
from backend.pessoa.models.core import Administrador, CARGO
from backend.pessoa.models.saude import AgendaProfissionalSaude, Especialidade, ProfissionalSaude, STATUS_DISPONIBILIDADE
from backend.atendimento.models import Consulta, Exame, ConsultaExame
from backend.atendimento.models.consulta import STATUS_ATENDIMENTO, TIPO_ATENDIMENTO
from backend.atendimento.models.exame import STATUS_EXAME
from backend.backoffice.models.compras import Fornecedor, ItemPedidoCompra, PedidoCompra, STATUS_PEDIDO
from backend.backoffice.models.estoque import EstoqueSuprimento, MovimentacaoSuprimento, Suprimento, UnidadeMedida, TIPO_MOVIMENTACAO
from backend.backoffice.models.financeiro import CategoriaFinanceira, LancamentoFinanceiro, FORMA_PAGAMENTO, TIPO_CATEGORIA
from backend.backoffice.models.gestaohospitalar import Ala, Leito, LogOcupacaoLeito, STATUS_LEITO

fake = Faker(locale='pt_BR')

def get_random_choice(choices):
    """Retorna um valor aleatório de uma lista de escolhas"""
    return random.choice([choice[0] for choice in choices])

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados fictícios para testes e avaliação'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando a criação de dados fictícios...'))

        # Criar grupos de usuários
        grupos = {
            'profissionais': Group.objects.get_or_create(name='Profissionais')[0],
            'pacientes': Group.objects.get_or_create(name='Pacientes')[0],
            'administradores': Group.objects.get_or_create(name='Administradores')[0]
        }

        # Criar usuário admin padrão se não existir
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@vidaplus.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('123456')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Superusuário criado: admin / 123456'))
        else:
            self.stdout.write(self.style.WARNING('Superusuário admin já existe'))

        local, _ = Local.objects.get_or_create(nome="Hospital VidaPlus", defaults={
            "endereco": fake.address(),
            "telefone": fake.phone_number()
        })

        especialidades = []
        for nome in ["Cardiologia", "Pediatria", "Ortopedia", "Clínico Geral", "Neurologia", "Dermatologia", "Oftalmologia", "Ginecologia", "Urologia", "Psiquiatria"]:
            esp, _ = Especialidade.objects.get_or_create(nome=nome, realiza_consulta=True)
            especialidades.append(esp)

        profissionais = []
        for _ in range(20):
            # Criar usuário para o profissional
            username = fake.user_name()
            email = fake.unique.email()
            user = User.objects.create_user(
                username=username,
                email=email,
                password='123456',
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            user.groups.add(grupos['profissionais'])

            esp = random.choice(especialidades)
            prof = ProfissionalSaude.objects.create(
                nome=fake.name(),
                cpf=fake.unique.numerify(text="###########"),
                telefone=fake.phone_number(),
                idLocal=local,
                endereco=fake.address(),
                registroProfissional=fake.numerify(text="########"),
                idUsuario=user
            )
            prof.especialidades.add(esp)
            profissionais.append(prof)

        pacientes = []
        for _ in range(50):
            # Criar usuário para o paciente
            username = fake.user_name()
            email = fake.unique.email()
            user = User.objects.create_user(
                username=username,
                email=email,
                password='123456',
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            user.groups.add(grupos['pacientes'])

            paciente = Paciente.objects.create(
                nome=fake.name(),
                cpf=fake.unique.numerify(text="###########"),
                dataNascimento=fake.date_of_birth(minimum_age=20, maximum_age=70),
                telefone=fake.phone_number(),
                email=email,
                idLocal=local,
                endereco=fake.address(),
                nomeContato=fake.name(),
                telefoneContato=fake.phone_number(),
                idUsuario=user
            )
            pacientes.append(paciente)

        consultas = []
        for paciente in pacientes:
            for _ in range(random.randint(2, 4)):
                prof = random.choice(profissionais)
                data_hora = make_aware(fake.date_time_between(start_date='-30d', end_date='+30d'))
                consulta = Consulta.objects.create(
                    idPaciente=paciente,
                    idProfissional=prof,
                    idLocal=local,
                    dataHoraConsulta=data_hora,
                    dataHoraAtendimento=data_hora,
                    status=get_random_choice(STATUS_ATENDIMENTO),
                    tipoAtendimento=get_random_choice(TIPO_ATENDIMENTO),
                    sintomas=fake.text(max_nb_chars=200),
                    diagnostico=fake.text(max_nb_chars=200),
                    medicamentoPrescrito=[
                        {
                            "nome": fake.word(),
                            "dosagem": f"{random.randint(1, 1000)}mg",
                            "intervalo": f"{random.randint(4, 12)} horas"
                        }
                        for _ in range(random.randint(1, 3))
                    ]
                )
                consultas.append(consulta)

        for consulta in consultas:
            for _ in range(random.randint(1, 3)):
                exame = Exame.objects.create(
                    idPaciente=consulta.idPaciente,
                    idProfissionalSolicitante=consulta.idProfissional,
                    idLocal=local,
                    tipoExame=random.choice(["Hemograma Completo", "Glicemia", "Colesterol", "Triglicerídeos", "Eletrocardiograma", "Raio-X", "Ultrassonografia"]),
                    detalhesSolicitacao=fake.text(max_nb_chars=200),
                    status=get_random_choice(STATUS_EXAME)
                )
                ConsultaExame.objects.create(
                    idConsulta=consulta,
                    idExame=exame
                )

        fornecedores = []
        for _ in range(10):
            fornecedor = Fornecedor.objects.create(
                nomeFantasia=fake.company(),
                razaoSocial=fake.company(),
                cpfCnpj=fake.cnpj(),
                telefone=fake.phone_number(),
                email=fake.company_email(),
                endereço=fake.address(),
                ativo=True
            )
            fornecedores.append(fornecedor)

        unidades = []
        for nome, abrev in [("Unidade", "UN"), ("Quilograma", "KG"), ("Litro", "L"), ("Caixa", "CX"), ("Pacote", "PC")]:
            unidade = UnidadeMedida.objects.create(
                nome=nome,
                abreviacao=abrev,
                descricao=f"Unidade de medida: {nome}"
            )
            unidades.append(unidade)

        suprimentos = []
        for _ in range(20):
            suprimento = Suprimento.objects.create(
                nome=fake.word().capitalize(),
                idUnidadeMedida=random.choice(unidades),
                descricao=fake.text(max_nb_chars=200),
                estoqueMinimo=random.randint(10, 100)
            )
            suprimentos.append(suprimento)

        for suprimento in suprimentos:
            estoque = EstoqueSuprimento.objects.create(
                idSuprimento=suprimento,
                idLocal=local,
                quantidadeAtual=random.randint(100, 1000)
            )
            for _ in range(random.randint(2, 5)):
                MovimentacaoSuprimento.objects.create(
                    idSuprimento=suprimento,
                    idLocal=local,
                    tipoMovimentacao=get_random_choice(TIPO_MOVIMENTACAO),
                    quantidade=random.randint(10, 100)
                )

        for _ in range(30):
            fornecedor = random.choice(fornecedores)
            pedido = PedidoCompra.objects.create(
                idFornecedor=fornecedor,
                idLocal=local,
                dataHoraPedido=make_aware(fake.date_time_between(start_date='-30d', end_date='+30d')),
                status=get_random_choice(STATUS_PEDIDO),
                valorTotal=0
            )
            valor_total = 0
            for _ in range(random.randint(2, 5)):
                suprimento = random.choice(suprimentos)
                quantidade = random.randint(1, 50)
                valor_unitario = round(random.uniform(1.0, 100.0), 2)
                ItemPedidoCompra.objects.create(
                    idPedido=pedido,
                    idSuprimento=suprimento,
                    quantidade=quantidade,
                    valorUnitario=valor_unitario
                )
                valor_total += quantidade * valor_unitario
            pedido.valorTotal = round(valor_total, 2)
            pedido.save()

        categorias = []
        for _ in range(10):
            categoria = CategoriaFinanceira.objects.create(
                nome=fake.word().capitalize(),
                tipo=get_random_choice(TIPO_CATEGORIA),
                descricao=fake.text(max_nb_chars=200)
            )
            categorias.append(categoria)

        for _ in range(50):
            LancamentoFinanceiro.objects.create(
                idCategoria=random.choice(categorias),
                idLocal=local,
                idFornecedor=random.choice(fornecedores),
                valor=round(random.uniform(100.0, 10000.0), 2),
                formaPagamento=get_random_choice(FORMA_PAGAMENTO)
            )

        alas = []
        for letra in ['A', 'B', 'C', 'D', 'E']:
            ala = Ala.objects.create(
                nome=f"Ala {letra}",
                idLocal=local,
                descricao=f"Ala de internação {letra}"
            )
            alas.append(ala)

        for ala in alas:
            for _ in range(10):
                leito = Leito.objects.create(
                    idAla=ala,
                    idLocal=local,
                    numeroLeito=fake.numerify(text="###"),
                    status=get_random_choice(STATUS_LEITO)
                )
                if random.choice([True, False]):
                    paciente = random.choice(pacientes)
                    leito.status = "OCUP"
                    leito.save()
                    LogOcupacaoLeito.objects.create(
                        idLocal=local,
                        idPaciente=paciente,
                        idLeito=leito,
                        idProfissionalInternacao=random.choice(profissionais),
                        dataHoraEntrada=make_aware(fake.date_time_between(start_date='-30d', end_date='now')),
                        dataHoraSaida=make_aware(fake.date_time_between(start_date='now', end_date='+30d')),
                        motivoInternacao=fake.text(max_nb_chars=200),
                        motivoLiberacao=fake.text(max_nb_chars=200)
                    )

        # Criar 5 administradores
        for _ in range(5):
            # Criar usuário para o administrador
            username = fake.user_name()
            email = fake.unique.email()
            user = User.objects.create_user(
                username=username,
                email=email,
                password='123456',
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            user.groups.add(grupos['administradores'])

            Administrador.objects.create(
                nome=fake.name(),
                cpf=fake.unique.numerify(text="###########"),
                telefone=fake.phone_number(),
                email=email,
                idLocal=local,
                cargo=get_random_choice(CARGO),
                endereco=fake.address(),
                idUsuario=user
            )

        self.stdout.write(self.style.SUCCESS('Dados fictícios criados com sucesso!'))
        self.stdout.write(self.style.SUCCESS('Senha padrão para outros usuários: 123456'))
