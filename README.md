# product-tools

Plugin de ferramentas de produto para uso no Claude Cowork (funciona também no
Claude Code e no Claude Desktop). Cobre o fluxo de refinamento de necessidades
de produto e a formatação direta de User Stories e Bugs no padrão DoR.

## O que tem dentro

| Item | Tipo | Uso |
|---|---|---|
| `refine` | skill | `/product-tools:refine` — pipeline completo: base de conhecimento (Confluence) → pesquisa de mercado → engenharia → qualidade → escrita da US |
| `format-user-story` | skill | `/product-tools:format-user-story` — formata uma US diretamente, sem passar pelo pipeline |
| `format-bug` | skill | `/product-tools:format-bug` — formata um bug diretamente, no padrão DoR |
| `document-feature` | skill | `/product-tools:document-feature` — cria/atualiza no Confluence (espaço de documentação configurado) páginas de funcionalidade, regra de negócio e histórico de mudanças, no template padrão |
| `pesquisa-mercado`, `engenharia`, `qualidade` | agentes | usados internamente pelo `refine`; não são chamados diretamente pelo time |

Todas as skills também disparam automaticamente pelo contexto da conversa
(ex: descrever uma necessidade sem digitar `/refine` já pode acionar
`format-user-story`), além de poderem ser chamadas de forma explícita pelo
comando.

## Instalação (time de produto, sem CLI)

1. Abrir o Claude, aba **Cowork**
2. Ir no diretório de plugins da organização e instalar `product-tools`
3. Preencher a configuração do plugin (pedida ao ativar):
   - `confluence_spaces` — chave(s) do(s) espaço(s) do Confluence com a base de
     conhecimento do seu módulo, separadas por vírgula (ex: `NSSEG,NSSEGCOT`)
   - `confluence_site` — opcional, ex: `nstech-empresa.atlassian.net`
   - `doc_space_key` — espaço onde o `/document-feature` publica, ex: `nsseg`
   - `doc_root_folder_id` — opcional, ID do folder que agrupa os domínios
     (ex: `14319631`, "Serviços e sistemas"); pegue na URL do folder
4. Conectar o conector **Atlassian** na conta (usado para ler o Confluence)
5. Pronto — os comandos ficam disponíveis em qualquer sessão Cowork, inclusive
   pelo app mobile

## Configuração por PO

Cada PO tem sua própria configuração, guardada localmente na máquina dele. No
início de cada sessão, um hook (`hooks/config-context.sh`) informa ao Claude os
valores configurados: o `/refine` busca a base de conhecimento só nos
`confluence_spaces`, e o `/document-feature` publica só no `doc_space_key`.
Cloud ID e ID do espaço são descobertos automaticamente pelo conector Atlassian. Para usar outro espaço numa execução pontual:

```
/product-tools:refine espaço=NSSEGSIN
O segurado precisa acompanhar o status do sinistro pelo portal
```

Se nada estiver configurado, o `/refine` pergunta o espaço uma única vez antes
de começar.

## Uso

```
/product-tools:refine
Quero que o cliente consiga parcelar o pagamento do checkout em até 12x
```

Se alguma etapa do pipeline apontar críticas, responda no mesmo fio da conversa
— o pipeline retoma da etapa que travou, sem reiniciar do zero.

## Ciclo completo

1. `/product-tools:refine` — lê a base de conhecimento (Confluence), refina e gera a US
2. Time desenvolve e entrega a US (Azure DevOps)
3. `/product-tools:document-feature` — atualiza a página da funcionalidade/regra
   no espaço de documentação e registra a US no histórico de mudanças. A próxima execução do
   `/refine` já encontra a regra atualizada.

## Escopo do MVP (o que ainda não tem)

- O `/refine` só lê o Confluence; escrita é feita apenas pelo `document-feature`,
  sempre no espaço `doc_space_key`
- Sem MCP de ADO: leitura/escrita de cards do Azure DevOps ainda não é feita
  por este plugin
- Sem busca de arquivo de contexto de projeto local — o contexto de negócio vem
  da conversa com o PO/PM e do Confluence

## Estrutura

```
product-tools/
├── .claude-plugin/plugin.json      # userConfig: confluence_site, confluence_spaces, doc_space_key, doc_root_folder_id
├── hooks/
│   ├── hooks.json                 # SessionStart → injeta a configuração do PO
│   └── config-context.sh
├── skills/
│   ├── refine/
│   │   ├── SKILL.md
│   │   └── references/formato-criticas.md
│   ├── document-feature/
│   │   └── SKILL.md
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
