# Importa Planilha PostgreSQL

🚀 **Ferramenta completa para importar planilhas Excel/CSV para PostgreSQL**

Este projeto permite importar dados de planilhas diretamente para o PostgreSQL, gerenciar metadados de tabelas e colunas, e trabalhar com dados geoespaciais de forma simples e eficiente.

## ⚡ Início Rápido

### 1. Instalação

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
```

**Usando pip (sem Poetry):**
```bash
# Menu interativo com todas as opções
python src/main.py

# Executar funcionalidades específicas
python src/carrega_metadados.py
python src/gera_create_inserts.py
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

## 🗂️ Estrutura do Projeto

```
Importa-planilha-postgresql/
├── src/                    # Código fonte principal
│   ├── main.py            # Interface principal
│   ├── carrega_metadados.py # Gerenciamento de metadados
│   ├── conexao.py         # Conexão com banco
│   ├── gera_create_inserts.py
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

**Para usar Poetry (recomendado):**
- **Poetry** instalado ([como instalar](https://python-poetry.org/docs/#installation))

**Para usar pip:**
- **pip** (geralmente vem com Python)
- **Ambiente virtual** (recomendado)

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

## 📄 Licença

MIT License - veja o arquivo `pyproject.toml` para detalhes.

## 👨‍💻 Autor

Felipe Alves - Desenvolvedor do projeto

---

📋 **Para exemplos práticos, veja [examples/exemplo_uso.md](examples/exemplo_uso.md)**  
⚙️ **Para template de configuração, veja [examples/config_exemplo.env](examples/config_exemplo.env)**  
📦 **Para instalação sem Poetry, veja [docs/INSTALACAO_SEM_POETRY.md](docs/INSTALACAO_SEM_POETRY.md)**
