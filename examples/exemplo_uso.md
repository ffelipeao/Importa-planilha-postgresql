# Como usar o projeto reorganizado

## 🚀 Estrutura do Projeto

```
Importa-planilha-postgresql/
├── src/                    # Código fonte principal
├── tools/                  # Ferramentas auxiliares
├── examples/               # Exemplos e templates
├── docs/                   # Documentação
├── .env                   # Sua configuração local
├── pyproject.toml         # Configuração Poetry
└── poetry.lock           # Lock file Poetry
```

## 📋 Menu interativo

Execute na raiz do projeto:

```bash
poetry run python src/main.py
# ou
poetry run importa-planilha
```

### Menu principal

| Opção | Função |
|-------|--------|
| **1** | Gerenciar metadados de tabelas |
| **2** | Gerar scripts SQL (CREATE + INSERT) |
| **3** | Exportar backup do banco de dados |
| **4** | Dados geoespaciais (submenu) |
| **5** | Ferramentas auxiliares (submenu) |
| **6** | Ajuda |
| **0** | Sair |

### Submenu 4 — Dados geoespaciais

| Opção | Função |
|-------|--------|
| **1** | Gerar raster |
| **2** | Importar raster separado |
| **3** | Importar raster unido |
| **0** | Voltar |

### Submenu 5 — Ferramentas auxiliares

| Opção | Função |
|-------|--------|
| **1** | Juntar planilhas |
| **2** | Juntar guias de planilha |
| **3** | Transpor planilha RH — superficiais |
| **4** | Transpor planilha RH — subterrâneos |
| **5** | Executar arquivo SQL |
| **0** | Voltar |

## 📋 Comandos diretos (sem menu)

### Metadados e SQL

```bash
poetry run python src/carrega_metadados.py
poetry run python src/gera_create_inserts.py
poetry run python src/gera_create_inserts.py -c iso-8859-1   # CSV em Latin-1
poetry run python src/gera_create_inserts.py --help
# ou
poetry run carrega-metadados
poetry run gera-create-inserts
```

### Backup do banco

```bash
poetry run python src/exporta_backup_bd.py
# ou
poetry run exporta-backup-bd
```

Dumps em `backup_bd_flonaca/`; arquivos com mais de 15 dias são removidos automaticamente.

## 🔧 Ferramentas auxiliares

As ferramentas de RH estão em `tools/` (também acessíveis pelo menu, opção **5**):

```bash
poetry run python tools/junta_planilhas.py
poetry run python tools/junta_guias_planilha.py
poetry run python tools/transpor_planilha_RH_dados_superficiais.py
poetry run python tools/transpor_planilha_RH_dados_subteraneo.py
poetry run python src/executa_arquivo_sql.py
```

## 🗺️ Dados geoespaciais

Também pelo menu, opção **4**:

```bash
poetry run python src/gerar_raster.py
poetry run python src/importa_raster_separado.py
poetry run python src/importa_raster_unidos.py
```

## 📊 Template de configuração

Use `examples/config_exemplo.env` como modelo para criar o `.env` na raiz do projeto.

## 🎯 Vantagens da estrutura

- ✅ **Organização clara** — código principal separado de ferramentas
- ✅ **Menu único** — todas as funções acessíveis por `src/main.py`
- ✅ **Exemplos organizados** — templates e configurações em `examples/`
- ✅ **Compatibilidade** — Poetry (`poetry run …`) ou `python src/…` com pip
