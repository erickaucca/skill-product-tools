# Changelog

## 0.6.0

### Alterado (quebra de contrato)
- `document-feature` foi substituída por **`rule-update`** (`/product-tools:rule-update`). O comando antigo deixa de existir.
- Novo modelo de documentação: um documento por funcionalidade com **todas as regras de negócio em Gherkin** (`RN-xx` estáveis), consolidado de forma cumulativa a partir de material do chat, US do Azure DevOps e texto colado. Substitui os três tipos de página (funcionalidade, regra com Page Properties, histórico em tabela) e a página de índice.
- Destino em **Confluence ou Notion**, na hierarquia `raiz / plataforma / domínio / funcionalidade`: atualiza se a combinação existir, cria só os níveis que faltam se não existir.
- Histórico fora da página da regra: página filha `Histórico de mudanças`, entradas mais recentes no topo, com `Antes`/`Depois` nas regras alteradas.
- Portões antes de agir: cabeçalho (`plataforma`, `domínio`, `funcionalidade`) e raiz obrigatórios; uma rodada única de perguntas (referências a outras funcionalidades, conflitos, lacunas); confirmação do diff antes de gravar.
- `doc_root_folder_id` agora é a **raiz** sob a qual a hierarquia é criada (antes, o folder que agrupava os domínios). Ajuste o valor se necessário.
- `refine`, `base-conhecimento` e hook de sessão passam a se referir ao `/rule-update` e ao novo padrão de páginas.

### Adicionado
- Skill **`rule-search`** (`/product-tools:rule-search`): consulta somente leitura que localiza as regras de uma funcionalidade e as mostra em Markdown no chat; se não encontra, informa em que nível parou.
- Evals de `rule-update` e `rule-search`.

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
