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
| `rule-update` | skill | `/product-tools:rule-update` — lê material do chat, US do Azure e texto colado e consolida as regras de negócio num `.md` em Gherkin, atualizando a página no Confluence ou Notion, na estrutura `plataforma / domínio / funcionalidade` sob uma raiz informada (cria os níveis que faltam, atualiza se existir). Exige os três campos no cabeçalho; o histórico fica numa página filha |
| `rule-search` | skill | `/product-tools:rule-search` — consulta somente leitura: localiza as regras de uma funcionalidade (`plataforma / domínio / funcionalidade` sob uma raiz) e mostra em Markdown no chat; se não achar, diz onde parou para você ajustar |
| `base-conhecimento`, `pesquisa-mercado`, `engenharia`, `qualidade` | agentes | usados internamente pelo `refine`; não são chamados diretamente pelo time |

`refine` e `rule-update` só rodam quando você os chama (`disable-model-invocation`),
porque têm custo alto ou escrevem no Confluence/Notion. `rule-search` é somente leitura. `format-user-story` e
`format-bug` também disparam pelo contexto da conversa (ex: pedir "escreve uma
US para..."), mas não em pedidos de código ou depuração.

## Instalação (time de produto, sem CLI)

1. Abrir o Claude, aba **Cowork**
2. Ir no diretório de plugins da organização e instalar `product-tools`
3. Preencher a configuração do plugin (pedida ao ativar):
   - `confluence_spaces` — chave(s) do(s) espaço(s) do Confluence com a base de
     conhecimento do seu módulo, separadas por vírgula (ex: `NSSEG,NSSEGCOT`)
   - `confluence_site` — opcional, ex: `nstech-empresa.atlassian.net`
   - `doc_space_key` — espaço onde o `/rule-update` publica, ex: `nsseg`
   - `doc_root_folder_id` — opcional, ID do folder ou página raiz sob a qual
     o `/rule-update` cria `plataforma / domínio / funcionalidade` (ex: `14319631`);
     pegue na URL
4. Conectar o conector **Atlassian** na conta (usado para ler e, no
   `/rule-update`, escrever no Confluence). Para destino Notion, conectar o
   conector **Notion**. O plugin não embute um MCP próprio, para não duplicar o
   login do conector que você já usa
5. Pronto — os comandos ficam disponíveis em qualquer sessão Cowork, inclusive
   pelo app mobile

## Receber atualizações

**Claude Code** (instalação por marketplace):

```
/plugin marketplace update erick-product-tools
/plugin update product-tools@erick-product-tools
```

Depois, reinicie a sessão. Para receber sem comando manual, ative o
auto-update em `/plugin` → Marketplaces (em marketplaces de terceiros costuma
vir desligado). A configuração do PO (`userConfig`) é preservada; se uma versão
nova pedir campos novos, só eles são solicitados.

**Cowork** (plugin instalado pelo diretório da organização): a atualização
depende da sincronização do marketplace feita pelo admin do workspace — o
usuário final normalmente não executa comando. Confirme com o admin como e com
que frequência a sincronização ocorre.

Se o repositório for privado, cada usuário precisa de acesso ao GitHub (login
do `git` ou `GITHUB_TOKEN`), senão a atualização falha.

## Configuração por PO

Cada PO tem sua própria configuração, guardada localmente na máquina dele. No
início de cada sessão, um hook (`hooks/config-context.sh`) informa ao Claude os
valores configurados: o `/refine` busca a base de conhecimento só nos
`confluence_spaces`, e o `/rule-update` publica só no `doc_space_key`.
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
3. `/product-tools:rule-update` — atualiza as regras da funcionalidade (Gherkin)
   na hierarquia plataforma / domínio / funcionalidade e registra a US na página filha de histórico (a página da funcionalidade guarda só a versão vigente). A próxima execução do
   `/refine` já encontra a regra atualizada.

## Desenvolvimento

- `python3 scripts/validate.py` — validação estática (manifestos, frontmatter,
  agentes, hooks, referências); roda também no CI (`.github/workflows/validate.yml`)
- `skills/*/evals/` — casos de teste para `skill-creator` (`evals.json`) e de
  gatilho (`trigger-evals.json`)
- Veja `CLAUDE.md` (convenções e checklist de release) e `CHANGELOG.md`

## Escopo do MVP (o que ainda não tem)

- O `/refine` só lê o Confluence; escrita é feita apenas pelo `rule-update`,
  sempre no espaço `doc_space_key`
- Sem MCP de ADO: leitura/escrita de cards do Azure DevOps ainda não é feita
  por este plugin
- Sem busca de arquivo de contexto de projeto local — o contexto de negócio vem
  da conversa com o PO/PM e do Confluence

## Estrutura

```
product-tools/
├── .claude-plugin/
│   ├── plugin.json                # userConfig: confluence_site, confluence_spaces, doc_space_key, doc_root_folder_id
│   └── marketplace.json
├── hooks/
│   ├── hooks.json                 # SessionStart → injeta a configuração do PO
│   └── config-context.sh
├── skills/
│   ├── refine/                    # SKILL.md, references/formato-criticas.md, evals/
│   ├── rule-update/               # SKILL.md, references/ (confluence, notion, template-documento), evals/
│   ├── rule-search/               # SKILL.md, evals/
│   ├── format-user-story/         # SKILL.md, references/, evals/
│   └── format-bug/                # SKILL.md, references/, evals/
├── agents/
│   ├── base-conhecimento.md
│   ├── pesquisa-mercado.md
│   ├── engenharia.md
│   └── qualidade.md
├── scripts/validate.py
├── .github/workflows/validate.yml
├── CHANGELOG.md
└── CLAUDE.md
```
