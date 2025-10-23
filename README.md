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

1. **Execute o programa:**
```bash
poetry run python main.py
```

2. **Selecione sua planilha** (Excel .xlsx ou CSV)

3. **O sistema automaticamente:**
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
poetry run python carrega_metadados.py
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
poetry run python carrega_metadados.py --arquivo metadados.xlsx

# Simular mudanças sem executar
poetry run python carrega_metadados.py --dry-run

# Executar sem pedir confirmação
poetry run python carrega_metadados.py --arquivo dados.csv --auto-confirm
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

## 📄 Licença

MIT License - veja o arquivo `pyproject.toml` para detalhes.

## 👨‍💻 Autor

Felipe Alves - Desenvolvedor do projeto
