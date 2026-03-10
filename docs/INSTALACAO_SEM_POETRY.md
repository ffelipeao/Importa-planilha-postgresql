# Instalação sem Poetry

Este arquivo contém instruções detalhadas para instalar e usar o projeto sem Poetry.

## 📦 Instalação das Dependências

### Opção 1: Ambiente Virtual (Recomendado)

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd Importa-planilha-postgresql

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

### Opção 2: Usando pipx (Alternativa)

```bash
# Instale pipx se não tiver
pip install pipx

# Clone o repositório
git clone <url-do-repositorio>
cd Importa-planilha-postgresql

# Instale as dependências usando pipx
pipx install -r requirements.txt
```

### Opção 3: Instalação Global (Não Recomendado)

```bash
# ⚠️ CUIDADO: Pode quebrar o sistema Python
pip install -r requirements.txt --break-system-packages
```

## 🚀 Execução

Após instalar as dependências:

```bash
# Menu interativo
python src/main.py

# Funcionalidades específicas
python src/carrega_metadados.py
python src/gera_create_inserts.py

# Ferramentas auxiliares
python tools/junta_planilhas.py
python tools/transpor_planilha_RH_dados_superficiais.py
```

## 🔧 Configuração

1. Copie o arquivo de exemplo:
```bash
cp examples/config_exemplo.env .env
```

2. Edite o arquivo `.env` com suas configurações de banco:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=seu_banco_de_dados
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
```

## 📋 Dependências Incluídas

- **pandas** - Manipulação de dados
- **numpy** - Computação numérica
- **psycopg2-binary** - Conexão com PostgreSQL
- **python-dotenv** - Carregamento de variáveis de ambiente
- **unidecode** - Normalização de texto
- **chardet** - Detecção de codificação
- **openpyxl** - Leitura de arquivos Excel
- **geopandas** - Dados geoespaciais (opcional)

## 🐛 Problemas Comuns

### Erro "externally-managed-environment"
- Use ambiente virtual: `python -m venv venv`
- Ou use pipx: `pipx install -r requirements.txt`

### Erro de importação
- Execute sempre da raiz do projeto
- Use `python src/arquivo.py` em vez de `python arquivo.py`

### Dependências faltando
- Reinstale: `pip install -r requirements.txt --force-reinstall`

## 🎯 Comandos Úteis

### Verificar instalação
```bash
# Verificar se as dependências estão instaladas
pip list | grep -E "(pandas|psycopg2|openpyxl)"

# Testar importação
python -c "import pandas, psycopg2, openpyxl; print('✅ Dependências OK')"
```

### Atualizar dependências
```bash
# Atualizar todas as dependências
pip install -r requirements.txt --upgrade

# Atualizar dependência específica
pip install --upgrade pandas
```

### Desinstalar
```bash
# Desinstalar todas as dependências
pip uninstall -r requirements.txt -y

# Desativar ambiente virtual
deactivate
```

## 📖 Exemplos de Uso

### Menu Interativo
```bash
python src/main.py
# Escolha uma opção no menu:
# 1. Gerenciar Metadados de Tabelas
# 2. Gerar Scripts SQL (CREATE + INSERT)
# 3. Dados Geoespaciais
# 4. Ferramentas Auxiliares
# 5. Ajuda
```

### Gerenciar Metadados
```bash
# Com arquivo específico
python src/carrega_metadados.py --arquivo metadados.xlsx

# Modo simulação
python src/carrega_metadados.py --dry-run

# Auto-confirmação
python src/carrega_metadados.py --auto-confirm
```

### Gerar Scripts SQL
```bash
# Executar diretamente
python src/gera_create_inserts.py
# Seleciona arquivos Excel/CSV e gera scripts SQL automaticamente
```

### Ferramentas Auxiliares
```bash
# Junção de planilhas
python tools/junta_planilhas.py

# Transposição de dados RH
python tools/transpor_planilha_RH_dados_superficiais.py
python tools/transpor_planilha_RH_dados_subteraneo.py
```

## 🔗 Links Úteis

- [Documentação Python venv](https://docs.python.org/3/library/venv.html)
- [Guia pipx](https://pipx.pypa.io/)
- [PostgreSQL Downloads](https://www.postgresql.org/download/)
- [Documentação pandas](https://pandas.pydata.org/docs/)
