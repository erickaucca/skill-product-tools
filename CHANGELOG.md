# Changelog

## 0.5.0

### Corrigido
- Agentes: `tools` com valores válidos (`WebSearch`, `Read`), `model` definido e descrições com "quando usar".
- Agentes não usam mais caminho relativo `../refine/...`; o orquestrador informa o caminho do formato de críticas (`${CLAUDE_SKILL_DIR}`).
- Hook de SessionStart: valores vêm de `CLAUDE_PLUGIN_OPTION_*` primeiro, argumentos entre aspas duplas, saída sanitizada, `timeout`.
- Skills `format-*`: saída portável (Cowork com `present_files` ou diretório de trabalho no Claude Code).

### Segurança
- `refine` e `document-feature` com `disable-model-invocation`; `document-feature` exige prévia e confirmação antes de publicar.
- Conteúdo do Confluence/web tratado como dado, não instrução.

### Alterado
- Pipeline por *delta*: cada agente devolve só a sua seção; o orquestrador anexa (menos tokens, sem reescrita de seções).
- Novo agente `base-conhecimento` (Etapa 0, somente leitura) mantém as páginas do Confluence fora do contexto principal.
- Descrições de `format-user-story` e `format-bug` restritas a contexto de produto/backlog (não disparam em sessões de código).
- `userConfig` com `type`/`title`/`required`; manifesto com `homepage`, `repository`, `keywords`; marketplace com `category`/`tags`.

### Adicionado
- `scripts/validate.py` + workflow de CI, `evals/` por skill, `CLAUDE.md`, `CHANGELOG.md`.
