# Instruções para agentes de IA

Documento **portável**: vale para Cursor, Cloud Agents, Copilot, Claude Code e outros assistentes neste repositório.  
Regras com escopo e frontmatter ficam em [`.agents/rules/`](.agents/rules/) (ver [`.agents/README.md`](.agents/README.md)). No Cursor, `.cursor/rules` aponta para o mesmo conteúdo via symlink.

## Objetivo do projeto

Ferramenta Python para importar planilhas Excel/CSV para PostgreSQL, gerenciar metadados, gerar SQL (CREATE/INSERT), trabalhar com dados geoespaciais e exportar backups (`pg_dump`). Detalhes de uso humano: [README.md](README.md).

## Ambiente e comandos

- **Python**: 3.8+; dependências via **Poetry** (`poetry install`) ou `pip install -r requirements.txt`.
- **Código da aplicação**: pasta `src/` (no `PYTHONPATH` do pytest).
- **Testes**: `poetry run pytest` (config em `pyproject.toml`, testes em `tests/`).
- **CLI principal**: `poetry run importa-planilha` ou `poetry run python src/main.py`.
- **Scripts Poetry** (ver `[tool.poetry.scripts]` em `pyproject.toml`): `carrega-metadados`, `gera-create-inserts`, `exporta-backup-bd`, etc.
- **Banco**: credenciais em `.env` (nunca commitar); classe `ConexaoBanco` em `src/conexao.py`.
- **Backups locais**: pasta `backup_bd_flonaca/` (gitignored).

## Estrutura relevante

| Caminho | Função |
|--------|--------|
| `src/main.py` | Menu interativo |
| `src/main_importacao.py` | Fluxo de importação |
| `src/carrega_metadados.py` | Metadados de tabelas/colunas |
| `src/gera_create_inserts.py` + `src/sql_generator/` | Geração de SQL a partir de planilhas |
| `src/exporta_backup_bd.py` | Backup pg_dump + retenção de dumps |
| `tests/` | Testes pytest (principalmente `sql_generator`) |

## Convenções de código

- **Escopo mínimo**: altere só o necessário para a tarefa; não refatore áreas não relacionadas.
- **Estilo**: siga o padrão dos arquivos ao redor (nomes, imports, docstrings em português quando já usadas no módulo).
- **Imports em `src/`**: módulos no mesmo nível importam sem prefixo `src.` (ex.: `from conexao import ConexaoBanco`), pois o pytest adiciona `src` ao path.
- **Comentários**: só onde a lógica de negócio ou detalhe técnico não for óbvio.
- **Testes**: adicione ou ajuste testes em `tests/` quando a mudança alterar comportamento testável; não crie testes triviais.
- **Documentação**: atualize README ou `docs/` só quando a mudança afetar uso ou instalação; não crie arquivos markdown novos sem pedido explícito.

## Git

- **Não executar `git commit` nem `git push`** a menos que o usuário peça explicitamente.
- Não commitar `.env`, dumps em `backup_bd_flonaca/` nem dados sensíveis.
- Não alterar `git config` do usuário; evitar comandos destrutivos (`reset --hard`, `push --force` em `main`, etc.) sem pedido explícito.

## Comunicação

- Respostas ao usuário em **português do Brasil**, claras e proporcionais à tarefa.
- Ao citar código existente, use o formato do projeto: bloco com `linhaInício:linhaFim:caminho`.

## Sugestão de commit (após editar arquivos)

Ao **concluir uma tarefa que alterou arquivos versionados** (código, config, testes, scripts), encerre a resposta com a seção abaixo.  
**Não** incluir se a resposta foi só explicação, revisão ou pergunta, sem edição de arquivos.

### Formato obrigatório

Título `## Sugestão de commit` e, logo abaixo, um único bloco de código com a mensagem:

````
<tipo>(<escopo>): <resumo em uma linha>

- <bullet 1: o que mudou e por quê>
- <bullet 2>
````

### Regras de redação

- `<tipo>`: `feat`, `fix`, `refactor`, `test`, `docs`, `chore` ou `style`
- `<escopo>`: área afetada (ex.: `backup`, `sql-generator`, `metadados`)
- Resumo: imperativo, sem ponto final, ~72 caracteres no máximo
- Bullets: 2–5 itens; foco no **porquê** e no impacto

### Exemplo

## Sugestão de commit

````
refactor(backup): reter os 5 dumps mais recentes na limpeza

- Substitui remoção por idade por limite de quantidade na pasta
- Preserva os 5 arquivos mais recentes independente da data
- Atualiza mensagens do menu e documentação
````
