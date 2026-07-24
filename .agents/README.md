# Configuração para agentes de IA

Diretório **portável** (Cursor, Codex, Claude Code, Copilot, etc.). Instruções gerais compartilhadas:

**[../AGENTS.md](../AGENTS.md)**

## Layout

| Caminho | Uso |
|---------|-----|
| `rules/project-core.mdc` | Sempre ativa: contexto mínimo + link para `AGENTS.md` |
| `rules/commit-message-suggestion.mdc` | Sempre ativa: sugestão de commit após edições |
| `rules/python.mdc` | Ao trabalhar com `**/*.py` |

Arquivos `.mdc` usam frontmatter (`description`, `globs`, `alwaysApply`) onde a ferramenta suportar.

## Cursor IDE

O Cursor descobre regras de projeto em `.cursor/rules/`. Neste repositório, **`.cursor/rules` é um symlink** para `.agents/rules` (sem duplicar conteúdo). Se o symlink não existir no seu clone, recrie:

```bash
mkdir -p .cursor
ln -snf ../.agents/rules .cursor/rules
```

## Manutenção

- Políticas para **todos** os agentes: edite `AGENTS.md` primeiro.
- Ajustes de escopo/ativação: edite os `.mdc` em `.agents/rules/`.
- Mantenha cada regra curta e com uma responsabilidade clara.
