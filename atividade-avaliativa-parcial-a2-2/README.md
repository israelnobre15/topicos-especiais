# Sistema de Gerenciamento de Tarefas

Aplicação web para gerenciamento de tarefas em grupo, no estilo Trello, desenvolvida em **Django 6.1** como atividade avaliativa da disciplina de Tópicos Especiais.

## Funcionalidades

- **Cadastro e autenticação de usuários**: registro com nome, e-mail e senha (com confirmação), login e logout. As senhas são armazenadas com hash de forma segura.
- **Gerenciamento de tarefas**: criação, visualização, edição e exclusão de tarefas com título, descrição e status (pendente, em andamento ou concluída).
- **Atribuição de tarefas**: qualquer usuário registrado pode ser definido como responsável por uma tarefa. O criador e o responsável têm os mesmos poderes — ambos podem editar e excluir a tarefa. Demais usuários autenticados podem apenas visualizá-la.
- **Filtragem por status**: tanto a lista pessoal quanto o dashboard permitem filtrar as tarefas por status.
- **Dashboard do grupo**: painel com contadores por status (total, pendentes, em andamento e concluídas) e a tabela com todas as tarefas de todos os usuários.
- **Lista pessoal**: exibe as tarefas criadas pelo usuário ou a ele atribuídas.

## Requisitos

- Python 3.12 ou superior
- Windows, Linux ou macOS

## Instalação

1. **Clonar o repositório**

   ```bash
   git clone https://github.com/israelnobre15/topicos-especiais.git
   cd topicos-especiais/atividade-avaliativa-parcial-a2-2
   ```

2. **Criar e ativar o ambiente virtual**

   Windows (PowerShell):

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   Linux/macOS:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instalar as dependências**

   ```bash
   pip install -r requirements.txt
   ```

4. **Aplicar as migrações (cria o banco SQLite)**

   ```bash
   cd gerenciamento_tarefas
   python manage.py migrate
   ```

5. **Iniciar o servidor de desenvolvimento**

   ```bash
   python manage.py runserver
   ```

6. **Acessar a aplicação**

   Abra <http://127.0.0.1:8000> no navegador. Você será direcionado à tela de login.

## Uso

1. Na tela inicial, clique em **Cadastrar** e crie uma conta informando nome, e-mail, senha e confirmação de senha. Após o cadastro você já fica autenticado e é levado ao dashboard.
2. No **Dashboard**, use o botão **+ Nova tarefa** para criar tarefas, definindo título, descrição, status e, opcionalmente, um responsável (qualquer usuário cadastrado).
3. Clique no título de uma tarefa para ver os detalhes completos. Se você for o criador ou o responsável, os botões **Editar** e **Excluir** estarão disponíveis — a exclusão pede confirmação.
4. Em **Minhas tarefas**, veja somente o que você criou ou o que foi atribuído a você, usando os filtros *Todas / Pendentes / Em andamento / Concluídas*.
5. Os cartões do dashboard funcionam como atalhos de filtro por status.
6. Use **Sair** para encerrar a sessão.

## Estrutura do projeto

```
gerenciamento_tarefas/
├── gerenciamento_tarefas/     # Configurações do projeto (settings, urls)
├── usuarios/                  # Cadastro, login e logout de usuários
└── tarefas/                   # Tarefas: CRUD, filtros, dashboard e permissões
```