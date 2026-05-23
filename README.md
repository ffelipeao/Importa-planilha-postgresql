# Importa Planilha PostgreSQL

🚀 **Ferramenta completa para importar planilhas Excel/CSV para PostgreSQL**

Este projeto permite importar dados de planilhas diretamente para o PostgreSQL, gerenciar metadados de tabelas e colunas, trabalhar com dados geoespaciais e exportar backups do banco (`pg_dump`) de forma simples e eficiente.

## ⚡ Início Rápido

### 1. Instalação

**Poetry não instalado?** Confira com `poetry --version`. Se o comando não existir, instale com o instalador oficial (recomendado):

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

No Windows (PowerShell):

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

Se `py` não estiver disponível, use `python` no lugar. Ao final, siga as instruções exibidas pelo instalador para adicionar o Poetry ao `PATH`, se necessário. Alternativa: `pip install poetry` (menos isolado do sistema Python).

**Opção A: Usando Poetry (Recomendado)**
```bash
# Clone o repositório
git clone <url-do-repositorio>
cd Importa-planilha-postgresql

# Instale as dependências
poetry install
```

**Opção B: Usando pip (sem Poetry)**
```bash
# Clone o repositório
git clone <url-do-repositorio>
cd Importa-planilha-postgresql

# Crie um ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt
```

### 2. Configuração do Banco
Crie um arquivo `.env` na raiz do projeto:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=seu_banco_de_dados
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
```

### 3. Primeira Execução

**Usando Poetry:**
```bash
# Menu interativo com todas as opções
poetry run python src/main.py

# Ou usar scripts específicos do Poetry
poetry run importa-planilha          # Menu interativo
poetry run carrega-metadados         # Gerenciar metadados
poetry run gera-create-inserts       # Gerar scripts SQL
poetry run exporta-backup-bd         # Backup do banco (dump + limpeza de arquivos antigos)
```

**Usando pip (sem Poetry):**
```bash
# Menu interativo com todas as opções
python src/main.py

# Executar funcionalidades específicas
python src/carrega_metadados.py
python src/gera_create_inserts.py
python src/exporta_backup_bd.py
```

## 📋 O que este projeto faz

### 🎯 Funcionalidades Principais

**1. Importação de Planilhas**
- Converte Excel (.xlsx) e CSV para tabelas PostgreSQL
- Criação automática de tabelas
- Detecção automática de tipos de dados
- Interface gráfica para seleção de arquivos

**2. Gerenciamento de Metadados**
- Adiciona comentários descritivos em tabelas e colunas
- Pré-visualiza mudanças antes de executar
- Confirmação interativa para segurança
- Modo simulação para testar sem alterar dados

**3. Geração de Scripts SQL**
- Converte planilhas em scripts CREATE TABLE e INSERT
- Cria arquivos SQL prontos para execução
- Suporte para Excel (.xlsx) e CSV
- Tratamento automático de dados e codificação

**4. Dados Geoespaciais**
- Importação de dados raster
- Processamento de informações geográficas
- Integração com PostGIS

**5. Utilitários de Planilhas**
- Junção de múltiplas planilhas
- Transposição de dados
- Ferramentas específicas para planilhas de RH

**6. Backup do banco de dados**
- Exporta dump em formato customizado (`pg_dump -Fc`) para a pasta `backup_bd_flonaca/`
- Remove automaticamente arquivos de backup locais com mais de 15 dias
- Requer `pg_dump` no `PATH` (cliente PostgreSQL instalado)

## 🗂️ Estrutura do Projeto

```
Importa-planilha-postgresql/
├── src/                    # Código fonte principal
│   ├── main.py            # Interface principal
│   ├── carrega_metadados.py # Gerenciamento de metadados
│   ├── conexao.py         # Conexão com banco
│   ├── gera_create_inserts.py
│   ├── exporta_backup_bd.py  # Backup pg_dump + limpeza de dumps antigos
│   ├── executa_arquivo_sql.py
│   ├── gerar_raster.py
│   ├── importa_raster_separado.py
│   ├── importa_raster_unidos.py
│   └── tipodados.txt      # Tipos de dados PostgreSQL
├── tools/                  # Ferramentas auxiliares
│   ├── __init__.py        # Arquivo de inicialização
│   ├── junta_guias_planilha.py
│   ├── junta_planilhas.py
│   ├── transpor_planilha_RH_dados_subteraneo.py
│   └── transpor_planilha_RH_dados_superficiais.py
├── examples/               # Exemplos e templates
│   ├── config_exemplo.env # Template de configuração
│   └── exemplo_uso.md     # Guia de uso
├── docs/                   # Documentação
│   └── INSTALACAO_SEM_POETRY.md # Guia de instalação sem Poetry
├── sql/                    # Scripts SQL gerados
│   └── *.sql              # Arquivos SQL criados automaticamente
├── .env                   # Sua configuração local
├── .env.example           # Exemplo de configuração
├── .gitignore             # Arquivos ignorados pelo Git
├── requirements.txt       # Dependências para pip
├── requirements-dev.txt   # Dependências de desenvolvimento
├── README.md              # Documentação completa
├── pyproject.toml         # Configuração Poetry
└── poetry.lock           # Lock file Poetry
```

## 🎯 Como Usar

### 🚀 Menu Interativo (Recomendado)

**Para acessar todas as funcionalidades através de um menu interativo:**

**Usando Poetry:**
```bash
poetry run python src/main.py
```

**Usando pip:**
```bash
python src/main.py
```

**O menu oferece as seguintes opções:**
- 📝 Gerenciar Metadados de Tabelas  
- 📄 Gerar Scripts SQL (CREATE + INSERT)
- 🗺️ Dados Geoespaciais
- 🛠️ Ferramentas Auxiliares
- ❓ Ajuda
- 💾 Exportar backup do banco de dados
- 🚪 Sair

### 💾 Exportar backup do banco de dados

**Para gerar um dump local e limpar backups antigos:**

**Método 1: Menu interativo (recomendado)**
```bash
# Usando Poetry
poetry run python src/main.py
# Escolha opção 6 no menu

# Usando pip
python src/main.py
# Escolha opção 6 no menu
```

**Método 2: Execução direta**
```bash
# Usando Poetry
poetry run python src/exporta_backup_bd.py
# ou
poetry run exporta-backup-bd

# Usando pip
python src/exporta_backup_bd.py
```

Os arquivos são gravados em `backup_bd_flonaca/` (nome com data e hora). É necessário ter o cliente PostgreSQL instalado para que o comando `pg_dump` esteja disponível no terminal.

### 📄 Gerar Scripts SQL de Planilhas

**Para converter planilhas em scripts CREATE TABLE e INSERT:**

**Método 1: Menu interativo (recomendado)**
```bash
# Usando Poetry
poetry run python src/main.py
# Escolha opção 2 no menu

# Usando pip
python src/main.py
# Escolha opção 2 no menu
```

**Método 2: Execução direta**
```bash
# Usando Poetry
poetry run python src/gera_create_inserts.py

# Usando pip
python src/gera_create_inserts.py
```

### 📝 Gerenciar Metadados de Tabelas

**Para adicionar comentários descritivos em tabelas e colunas:**

1. **Prepare sua planilha** com as colunas:
   - `schema` - Nome do schema (ex: public)
   - `tabela` - Nome da tabela (ex: usuarios)
   - `comentario_tabela` - Descrição da tabela
   - `coluna` - Nome da coluna (ex: email)
   - `comentario_coluna` - Descrição da coluna

2. **Execute o programa:**
```bash
# Método 1: Menu interativo (recomendado)
# Usando Poetry
poetry run python src/main.py
# Escolha opção 1 no menu

# Usando pip
python src/main.py
# Escolha opção 1 no menu

# Método 2: Execução direta
# Usando Poetry
poetry run python src/carrega_metadados.py

# Usando pip
python src/carrega_metadados.py
```

3. **O sistema mostra uma pré-visualização** das mudanças:
```
================================================================================
PRÉ-VISUALIZAÇÃO DAS MUDANÇAS
================================================================================

📋 TABELAS QUE SERÃO ATUALIZADAS (2):
--------------------------------------------------------------------------------

1. public.usuarios (linha 1)
   ATUAL:
   (sem comentário)
   NOVO:
   'Tabela de usuários do sistema'
----------------------------------------

🤔 Deseja executar essas mudanças?
Digite:
  's' ou 'sim' - Para executar as mudanças
  'n' ou 'não' - Para cancelar
  'dry' - Para simular sem executar
```

### 🔧 Opções Avançadas

**Argumentos de linha de comando:**
```bash
# Especificar arquivo diretamente
# Usando Poetry
poetry run python src/carrega_metadados.py --arquivo metadados.xlsx

# Usando pip
python src/carrega_metadados.py --arquivo metadados.xlsx

# Simular mudanças sem executar
# Usando Poetry
poetry run python src/carrega_metadados.py --dry-run

# Usando pip
python src/carrega_metadados.py --dry-run

# Executar sem pedir confirmação
# Usando Poetry
poetry run python src/carrega_metadados.py --arquivo dados.csv --auto-confirm

# Usando pip
python src/carrega_metadados.py --arquivo dados.csv --auto-confirm

# Ver todas as opções
# Usando Poetry
poetry run python src/carrega_metadados.py --help

# Usando pip
python src/carrega_metadados.py --help
```

### 🛠️ Ferramentas Auxiliares

**Ferramentas de RH e manipulação de planilhas:**
```bash
# Junção de planilhas
# Usando Poetry
poetry run python tools/junta_planilhas.py

# Usando pip
python tools/junta_planilhas.py

# Transposição de dados RH
# Usando Poetry
poetry run python tools/transpor_planilha_RH_dados_superficiais.py
poetry run python tools/transpor_planilha_RH_dados_subteraneo.py

# Usando pip
python tools/transpor_planilha_RH_dados_superficiais.py
python tools/transpor_planilha_RH_dados_subteraneo.py

# Junção de guias de planilha
# Usando Poetry
poetry run python tools/junta_guias_planilha.py

# Usando pip
python tools/junta_guias_planilha.py

# Executar um arquivo SQL no banco configurado no .env
# Usando Poetry
poetry run python src/executa_arquivo_sql.py

# Usando pip
python src/executa_arquivo_sql.py
```

### 🗺️ Dados Geoespaciais

**Importação de dados raster:**
```bash
# Gerar raster
# Usando Poetry
poetry run python src/gerar_raster.py

# Usando pip
python src/gerar_raster.py

# Importar raster separado
# Usando Poetry
poetry run python src/importa_raster_separado.py

# Usando pip
python src/importa_raster_separado.py

# Importar raster unido
# Usando Poetry
poetry run python src/importa_raster_unidos.py

# Usando pip
python src/importa_raster_unidos.py
```

## 📦 Pré-requisitos

**Obrigatórios:**
- **Python 3.8+** instalado
- **PostgreSQL** configurado e rodando

**Para exportar backup pelo script (`exporta_backup_bd.py`):**
- **Cliente PostgreSQL** com `pg_dump` no `PATH` (no macOS com Homebrew: `brew install libpq` e siga a dica do `brew` para o `PATH`, ou use a instalação completa do PostgreSQL)

**Para usar Poetry (recomendado):**
- **Poetry** instalado ([como instalar](https://python-poetry.org/docs/#installation))

**Para usar pip:**
- **pip** (geralmente vem com Python)
- **Ambiente virtual** (recomendado)

## 💻 Guia rápido para macOS (Mac)

Este passo a passo foi pensado para configurar o ambiente em macOS (incluindo Macs com Apple Silicon).

### 1. Ferramentas básicas

- **Instalar Xcode Command Line Tools (compiladores básicos):**
```bash
xcode-select --install
```

- **Instalar o Homebrew (gerenciador de pacotes do macOS):**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Após a instalação, siga as instruções que aparecem no terminal para adicionar o `brew` ao `PATH` (por exemplo, em Macs com chip M1/M2/M3, algo como):
```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### 2. Instalar Python no macOS

Recomenda-se usar o Python do Homebrew:
```bash
brew install python
python3 --version
```

### 3. Criar ambiente virtual (sem Poetry)

Se você preferir usar `pip` em vez de Poetry:
```bash
cd Importa-planilha-postgresql
python3 -m venv .venv
source .venv/bin/activate  # macOS (zsh/bash)

# Instalar dependências
pip install -r requirements.txt
```

### 4. Instalar Poetry no macOS (opção recomendada)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Depois do comando acima, adicione o Poetry ao `PATH` (caso necessário), por exemplo:
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

Então, na pasta do projeto:
```bash
cd Importa-planilha-postgresql
poetry install
poetry run python src/main.py
```

### 5. Instalar PostgreSQL no macOS

Escolha **uma** das opções abaixo:

- **Opção A – Homebrew (terminal):**
```bash
brew install postgresql
brew services start postgresql   # inicia o serviço do banco

# Criar um banco de dados local
createdb meu_banco
psql -d meu_banco
```

- **Opção B – Postgres.app (interface gráfica):**
- Baixe o Postgres.app em `https://postgresapp.com/`
- Arraste para `Aplicativos` e abra o app
- Crie um banco de dados pela interface e use as credenciais fornecidas pelo Postgres.app

### 6. Configurar o arquivo `.env` no macOS

No diretório raiz do projeto, crie (ou edite) o arquivo `.env`:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=meu_banco
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
```

Se estiver usando o Postgres instalado via Homebrew, normalmente o usuário padrão é o seu usuário do macOS (sem senha). Nesse caso, você pode deixar `DB_PASSWORD` vazio ou configurar uma senha via `psql`, conforme sua política de segurança.

### 7. Executar o projeto no macOS

- **Usando Poetry (recomendado):**
```bash
cd Importa-planilha-postgresql
poetry install
poetry run python src/main.py
```

- **Usando pip (sem Poetry):**
```bash
cd Importa-planilha-postgresql
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

## 🐛 Problemas Comuns

### ❌ Erro de Conexão com PostgreSQL
- Verifique se o PostgreSQL está rodando
- Confirme as credenciais no arquivo `.env`
- O sistema mostra informações detalhadas sobre a conexão

### ❌ Problemas com Seleção de Arquivo
- Use `--arquivo` para especificar arquivo diretamente
- Use `--dry-run` para testar sem executar mudanças
- O sistema funciona em ambientes headless (SSH/servidor)

### ❌ Dependências Não Instaladas

**Usando Poetry:**
```bash
# Reinstalar todas as dependências
poetry install --sync
```

**Usando pip:**
```bash
# Reinstalar todas as dependências
pip install -r requirements.txt --force-reinstall

# Ou para desenvolvimento
pip install -r requirements-dev.txt --force-reinstall
```

### ❌ Problemas com Imports
- Execute sempre da pasta `src/` ou use os scripts do Poetry
- Os imports relativos funcionam apenas dentro de `src/`
- Se usar pip, execute `python src/arquivo.py` em vez de `python arquivo.py`

### ❌ Backup: `pg_dump` não encontrado
- Instale o cliente PostgreSQL ou adicione o diretório dos binários (`pg_dump`) ao `PATH`
- Confirme com `which pg_dump` (Linux/macOS) ou `where pg_dump` (Windows)

## 📄 Licença

MIT License - veja o arquivo `pyproject.toml` para detalhes.

## 👨‍💻 Autor

Felipe Alves - Desenvolvedor do projeto

---

📋 **Para exemplos práticos, veja [examples/exemplo_uso.md](examples/exemplo_uso.md)**  
⚙️ **Para template de configuração, veja [examples/config_exemplo.env](examples/config_exemplo.env)**  
📦 **Para instalação sem Poetry, veja [docs/INSTALACAO_SEM_POETRY.md](docs/INSTALACAO_SEM_POETRY.md)**
