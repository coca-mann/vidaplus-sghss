# VidaPlus SGHSS - Backend

Sistema de Gestão Hospitalar e de Serviços de Saúde (SGHSS), desenvolvido para a instituição VidaPlus, que administra clínicas, hospitais, laboratórios e serviços de home care.

Este repositório contém a aplicação **backend**, desenvolvida em Django + Django Rest Framework, com foco em integração entre setores da área da saúde, segurança dos dados e modularização por responsabilidades.

---

## 🚀 Tecnologias Utilizadas

- Python 3.10+
- Django 4.x
- Django Rest Framework (DRF)
- DRF Spectacular (documentação automática da API)
- JWT Authentication (djangorestframework-simplejwt)
- PostgreSQL
- Insomnia/Postman (testes manuais da API)
- draw.io (modelagem UML)

---

## 🏥 Funcionalidades Principais

### 📁 Módulos:

- **Atendimento**: Consulta, Exames, Prontuários, Prescrições
- **Pessoa**: Cadastro de Pacientes, Profissionais de Saúde, Administradores
- **Local**: Cadastro de unidades (clínicas e hospitais)
- **Backoffice**:
  - **Compras**: Fornecedores, Pedidos e Itens de Compra
  - **Estoque**: Controle de suprimentos, movimentação e unidades de medida
  - **Financeiro**: Categorias e lançamentos financeiros
  - **Leitos**: Internações, liberações e logs de ocupação
- **Auditoria**: Registro de logs automáticos e (futuramente) consentimentos LGPD

### 🔐 Segurança:
- Autenticação via JWT (access/refresh tokens)
- Controle de acesso por tipo de usuário (Paciente, Profissional, Administrador)
- Permissões por cargo para acessar ou editar recursos
- Logs automáticos via Django-Audit

### 📄 JSONFields com lógica customizada:
- `examesSolicitados` (Paciente): gera ou atualiza registros de exames
- `medicamentoPrescrito` (Consulta): permite adicionar/remover medicamentos via JSON

---

## ⚙️ Como Executar o Projeto

### 1. Clone o repositório
```bash
git clone https://github.com/coca-mann/vidaplus-sghss.git
cd vidaplus-sghss
```

### 2. Crie e ative um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Aplique as migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crie um superusuário
```bash
python manage.py createsuperuser
```

### 6. Popule o banco de dados com dados fictícios
```bash
python manage.py populate_fake_data
```

### 7. Execute o servidor local
```bash
python manage.py runserver
```

## 🧪 Testes
Atualmente os testes são manuais via Insomnia, com diferentes perfis de usuário para validação de:
- Permissões de acesso
- Rotas protegidas
- Validações de entrada e lógica de negócio

## 🗂️ Estrutura do Projeto

```bash
vidaplus-sghss/
├── atendimento/
├── auditoria/
├── backoffice/
│   ├── compras/
│   ├── estoque/
│   ├── financeiro/
│   └── gestao_hospitalar/
├── local/
├── pessoa/
├── utils/
├── documentation/
├── media/
├── manage.py
├── requirements.txt
└── README.md
```

## 📚 Documentação da API
A documentação da API está disponível no formato Swagger/OpenAPI, gerada automaticamente com DRF Spectacular.

Acesse via navegador: 👉 http://127.0.0.1:8000/api/v1/docs/