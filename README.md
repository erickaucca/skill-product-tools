# product-tools

Plugin de ferramentas de produto para uso no Claude Cowork (funciona também no
Claude Code e no Claude Desktop). Cobre o fluxo de refinamento de necessidades
de produto e a formatação direta de User Stories e Bugs no padrão DoR.

## O que tem dentro

| Item | Tipo | Uso |
|---|---|---|
| `refine` | skill | `/product-tools:refine` — pipeline completo: pesquisa de mercado → engenharia → qualidade → escrita da US |
| `format-user-story` | skill | `/product-tools:format-user-story` — formata uma US diretamente, sem passar pelo pipeline |
| `format-bug` | skill | `/product-tools:format-bug` — formata um bug diretamente, no padrão DoR |
| `pesquisa-mercado`, `engenharia`, `qualidade` | agentes | usados internamente pelo `refine`; não são chamados diretamente pelo time |

Todas as skills também disparam automaticamente pelo contexto da conversa
(ex: descrever uma necessidade sem digitar `/refine` já pode acionar
`format-user-story`), além de poderem ser chamadas de forma explícita pelo
comando.

## Instalação (time de produto, sem CLI)

1. Abrir o Claude, aba **Cowork**
2. Ir no diretório de plugins da organização e instalar `product-tools`
3. Pronto — os comandos ficam disponíveis em qualquer sessão Cowork, inclusive
   pelo app mobile

## Uso

```
/product-tools:refine
Quero que o cliente consiga parcelar o pagamento do checkout em até 12x
```

Se alguma etapa do pipeline apontar críticas, responda no mesmo fio da conversa
— o pipeline retoma da etapa que travou, sem reiniciar do zero.

## Escopo do MVP (o que ainda não tem)

- Sem MCP de Produto: a validação contra a base de regras oficiais do produto
  ainda não existe nesta versão — está no roadmap
- Sem MCP de ADO: leitura/escrita de cards do Azure DevOps ainda não é feita
  por este plugin
- Sem busca de arquivo de contexto de projeto — todo contexto de negócio vem
  da própria conversa com o PO/PM

## Estrutura

```
product-tools/
├── .claude-plugin/plugin.json
├── skills/
│   ├── refine/
│   │   ├── SKILL.md
│   │   └── references/formato-criticas.md
│   ├── format-user-story/
│   │   ├── SKILL.md
│   │   └── references/
│   └── format-bug/
│       ├── SKILL.md
│       └── references/
└── agents/
    ├── pesquisa-mercado.md
    ├── engenharia.md
    └── qualidade.md
```
