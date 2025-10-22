# Importa Planilha PostgreSQL

Projeto Python para importação e processamento de planilhas Excel/CSV para banco de dados PostgreSQL, incluindo funcionalidades de metadados, raster e manipulação de dados geoespaciais.

## 🚀 Instalação e Configuração com Poetry

### Pré-requisitos
- Python 3.8 ou superior
- Poetry instalado ([como instalar Poetry](https://python-poetry.org/docs/#installation))
- PostgreSQL configurado

### Configuração do Projeto

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd Importa-planilha-postgresql
```

2. **Instale as dependências com Poetry:**
```bash
# Instalar todas as dependências (produção + desenvolvimento)
poetry install

# Ou apenas dependências de produção
poetry install --only main
```

3. **Configure as variáveis de ambiente:**
Crie um arquivo `.env` na raiz do projeto:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=seu_banco_de_dados
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
```

4. **Execute o projeto:**
```bash
# Usando Poetry
poetry run python main.py

# Ou ativando o ambiente virtual
poetry shell
python main.py
```

### Comandos Poetry Úteis

```bash
# Adicionar nova dependência
poetry add nome-do-pacote

# Adicionar dependência de desenvolvimento
poetry add --group dev nome-do-pacote

# Atualizar dependências
poetry update

# Ver dependências instaladas
poetry show

# Executar comandos no ambiente virtual
poetry run python script.py
```

## 📋 Funcionalidades

### 🔧 Módulos Principais

- **`main.py`** - Interface principal para importação de planilhas Excel/CSV
- **`carrega_metadados.py`** - Gerenciamento de metadados de tabelas e colunas
- **`conexao.py`** - Classe para conexão com PostgreSQL
- **`gera_create_inserts.py`** - Geração automática de scripts SQL CREATE e INSERT
- **`executa_arquivo_sql.py`** - Execução de arquivos SQL

### 🗺️ Módulos Geoespaciais

- **`gerar_raster.py`** - Geração de dados raster
- **`importa_raster_separado.py`** - Importação de rasters individuais
- **`importa_raster_unidos.py`** - Importação de rasters consolidados

### 📊 Utilitários de Planilhas

- **`Juntar_planilhas - GT_RH/`** - Ferramentas para manipulação de planilhas de RH
  - `junta_guias_planilha.py` - Junção de guias de planilhas
  - `junta_planilhas.py` - Consolidação de múltiplas planilhas
  - `transpor_planilha_RH_dados_subteraneo.py` - Transposição de dados subterrâneos
  - `transpor_planilha_RH_dados_superficiais.py` - Transposição de dados superficiais

## 🎯 Como Usar

### Importação Básica de Planilhas

1. Execute o arquivo principal:
```bash
poetry run python main.py
```

2. Selecione o arquivo Excel (.xlsx) ou CSV através da interface gráfica

3. O sistema irá:
   - Detectar automaticamente o formato do arquivo
   - Criar uma tabela no PostgreSQL com o nome do arquivo
   - Importar todos os dados da planilha
   - Gerar o script SQL CREATE correspondente

### Gerenciamento de Metadados

```bash
poetry run python carrega_metadados.py
```

Este módulo permite:
- Carregar metadados de tabelas e colunas a partir de planilhas
- Verificar existência de tabelas e colunas no banco
- Atualizar comentários de tabelas e colunas
- Gerar relatórios detalhados das operações

### Geração de Scripts SQL

```bash
poetry run python gera_create_inserts.py
```

Funcionalidades:
- Geração automática de scripts CREATE TABLE
- Criação de scripts INSERT com os dados
- Detecção automática de codificação de arquivos
- Formatação de nomes de arquivos e colunas

## 📦 Dependências

### Principais
- **pandas** - Manipulação de dados
- **numpy** - Computação numérica
- **psycopg2-binary** - Conector PostgreSQL
- **python-dotenv** - Gerenciamento de variáveis de ambiente
- **openpyxl** - Leitura de arquivos Excel
- **chardet** - Detecção de codificação
- **unidecode** - Normalização de caracteres

### Desenvolvimento
- **geopandas** - Processamento de dados geoespaciais

## 🔧 Configuração do Banco

O projeto utiliza PostgreSQL e requer as seguintes configurações no arquivo `.env`:

```env
DB_HOST=localhost          # Host do banco
DB_PORT=5432              # Porta do PostgreSQL
DB_NAME=nome_do_banco     # Nome do banco de dados
DB_USER=usuario           # Usuário do banco
DB_PASSWORD=senha         # Senha do usuário
```

## 📁 Estrutura do Projeto

```
Importa-planilha-postgresql/
├── main.py                           # Interface principal
├── carrega_metadados.py             # Gerenciamento de metadados
├── conexao.py                       # Classe de conexão
├── gera_create_inserts.py           # Geração de scripts SQL
├── executa_arquivo_sql.py           # Execução de SQL
├── gerar_raster.py                  # Geração de raster
├── importa_raster_separado.py       # Importação de raster individual
├── importa_raster_unidos.py         # Importação de raster consolidado
├── Juntar_planilhas - GT_RH/        # Utilitários de planilhas RH
├── sql/                             # Arquivos SQL
├── pyproject.toml                   # Configuração Poetry
├── poetry.lock                      # Lock file Poetry
└── .env                            # Variáveis de ambiente
```

## ⚠️ Importante

- **Mantenha o arquivo `poetry.lock`** versionado para garantir reproduzibilidade
- **Configure corretamente o arquivo `.env`** com suas credenciais do PostgreSQL
- **Use Poetry para gerenciar dependências** - não instale pacotes manualmente
- **Execute sempre dentro do ambiente virtual** do Poetry

## 🐛 Solução de Problemas

### Erro de Conexão com PostgreSQL
- Verifique se o PostgreSQL está rodando
- Confirme as credenciais no arquivo `.env`
- Teste a conexão manualmente

### Problemas com Codificação
- O sistema detecta automaticamente a codificação de arquivos CSV
- Para arquivos com problemas, use `chardet` para identificar a codificação

### Dependências Não Instaladas
```bash
# Reinstalar todas as dependências
poetry install --sync
```

## 📄 Licença

MIT License - veja o arquivo `pyproject.toml` para detalhes.

## 👨‍💻 Autor

Felipe Alves - Desenvolvedor do projeto
