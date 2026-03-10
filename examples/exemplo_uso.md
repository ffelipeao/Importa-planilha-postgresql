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

## 📋 Como Executar

### Importar Planilha
```bash
poetry run python src/main.py
```

### Gerenciar Metadados
```bash
poetry run python src/carrega_metadados.py
```

### Usando Scripts do Poetry
```bash
poetry run importa-planilha
poetry run carrega-metadados
```

## 🔧 Ferramentas Auxiliares

As ferramentas de RH estão agora em `tools/`:

```bash
# Junção de planilhas
poetry run python tools/junta_planilhas.py

# Transposição de dados RH
poetry run python tools/transpor_planilha_RH_dados_superficiais.py
poetry run python tools/transpor_planilha_RH_dados_subteraneo.py

# Junção de guias de planilha
poetry run python tools/junta_guias_planilha.py
```

## 🗺️ Dados Geoespaciais

```bash
# Gerar raster
poetry run python src/gerar_raster.py

# Importar raster separado
poetry run python src/importa_raster_separado.py

# Importar raster unido
poetry run python src/importa_raster_unidos.py
```

## 📊 Template de Metadados

Use o arquivo `examples/config_exemplo.env` como modelo para criar seu `.env`.

## 🎯 Vantagens da Nova Estrutura

- ✅ **Organização clara** - Código principal separado de ferramentas
- ✅ **Fácil navegação** - Estrutura simples e lógica
- ✅ **Exemplos organizados** - Templates e configurações em um local
- ✅ **Manutenção facilitada** - Separação de responsabilidades
- ✅ **Estrutura limpa** - Sem links simbólicos desnecessários
- ✅ **Compatibilidade mantida** - Funciona com Poetry e imports relativos
