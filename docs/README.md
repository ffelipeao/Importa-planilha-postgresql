# Importa Planilha PostgreSQL

🚀 **Ferramenta completa para importar planilhas Excel/CSV para PostgreSQL**

Este projeto permite importar dados de planilhas diretamente para o PostgreSQL, gerenciar metadados de tabelas e colunas, e trabalhar com dados geoespaciais de forma simples e eficiente.

## ⚡ Início Rápido

### 1. Instalação
```bash
# Clone o repositório
git clone <url-do-repositorio>
cd Importa-planilha-postgresql

# Instale as dependências
poetry install
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
```bash
# Importar planilha para PostgreSQL
poetry run python main.py

# Gerenciar metadados de tabelas
poetry run python carrega_metadados.py
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

**3. Dados Geoespaciais**
- Importação de dados raster
- Processamento de informações geográficas
- Integração com PostGIS

**4. Utilitários de Planilhas**
- Junção de múltiplas planilhas
- Transposição de dados
- Ferramentas específicas para planilhas de RH

## 🎯 Como Usar

### 📊 Importar Planilha para PostgreSQL

```bash
poetry run python src/main.py
```

**O sistema automaticamente:**
- Detecta o formato do arquivo
- Cria uma tabela no PostgreSQL
- Importa todos os dados
- Gera o script SQL correspondente

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
poetry run python src/carrega_metadados.py
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
poetry run python src/carrega_metadados.py --arquivo metadados.xlsx

# Simular mudanças sem executar
poetry run python src/carrega_metadados.py --dry-run

# Executar sem pedir confirmação
poetry run python src/carrega_metadados.py --arquivo dados.csv --auto-confirm

# Ver todas as opções
poetry run python src/carrega_metadados.py --help
```

### 🛠️ Ferramentas Auxiliares

**Ferramentas de RH e manipulação de planilhas:**
```bash
# Junção de planilhas
poetry run python tools/junta_planilhas.py

# Transposição de dados RH
poetry run python tools/transpor_planilha_RH_dados_superficiais.py
poetry run python tools/transpor_planilha_RH_dados_subteraneo.py

# Junção de guias de planilha
poetry run python tools/junta_guias_planilha.py
```

### 🗺️ Dados Geoespaciais

**Importação de dados raster:**
```bash
# Gerar raster
poetry run python src/gerar_raster.py

# Importar raster separado
poetry run python src/importa_raster_separado.py

# Importar raster unido
poetry run python src/importa_raster_unidos.py
```

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
│   └── importa_raster_unidos.py
├── tools/                  # Ferramentas auxiliares
│   ├── junta_guias_planilha.py
│   ├── junta_planilhas.py
│   ├── transpor_planilha_RH_dados_subteraneo.py
│   └── transpor_planilha_RH_dados_superficiais.py
├── examples/               # Exemplos e templates
│   ├── config_exemplo.env # Template de configuração
│   └── exemplo_uso.md     # Guia de uso
├── docs/                   # Documentação
│   └── README.md          # Documentação completa
├── .env                   # Sua configuração local
├── pyproject.toml         # Configuração Poetry
└── poetry.lock           # Lock file Poetry
```

## 📦 Pré-requisitos

- **Python 3.8+** instalado
- **Poetry** instalado ([como instalar](https://python-poetry.org/docs/#installation))
- **PostgreSQL** configurado e rodando

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
```bash
# Reinstalar todas as dependências
poetry install --sync
```

### ❌ Problemas com Imports
- Execute sempre da pasta `src/` ou use os scripts do Poetry
- Os imports relativos funcionam apenas dentro de `src/`

## 📄 Licença

MIT License - veja o arquivo `pyproject.toml` para detalhes.

## 👨‍💻 Autor

Felipe Alves - Desenvolvedor do projeto
