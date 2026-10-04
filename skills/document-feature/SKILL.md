---
name: document-feature
description: "Lê o material do chat (documento gerado na conversa, US do Azure DevOps, texto colado), analisa com cuidado e consolida TODAS as regras de negócio de uma funcionalidade num documento .md em formato Gherkin, incrementando o que já existe no destino (página do Confluence ou Notion) e atualizando-o. Exige no cabeçalho plataforma, domínio e funcionalidade; se faltar qualquer um, pergunta antes de qualquer análise. Se o material ou o destino referenciar outra funcionalidade, pergunta antes de alterar qualquer coisa. Use sempre que o usuário pedir para documentar uma funcionalidade ou regra de negócio, atualizar a documentação após uma US, ou consolidar regras em Gherkin, mesmo que a palavra 'skill' ou 'Gherkin' não apareça. Invocável via /document-feature."
---

# Documentação de Regras de Negócio em Gherkin

Esta skill transforma material solto (conversa, US do Azure DevOps, texto) em **um documento `.md` único e sempre atualizado** com todas as regras de negócio de uma funcionalidade, escritas em Gherkin, e sincroniza esse documento com um destino (Confluence ou Notion).

Princípio central: **cumulativo e não destrutivo**. Cada execução lê tudo o que já existe, soma o que é novo e devolve a versão completa. Nunca gera um documento "só com a novidade" e nunca apaga regra existente sem confirmação.

## Ordem obrigatória das etapas

Não pule nem reordene. Cada portão (🚦) bloqueia a etapa seguinte.

1. 🚦 **Portão 1 — Cabeçalho e destino** (antes de qualquer análise)
2. **Coleta do material** (chat, Azure, texto)
3. **Leitura do destino atual**
4. 🚦 **Portão 2 — Referências a outras funcionalidades** (antes de qualquer mudança)
5. **Análise e consolidação das regras**
6. 🚦 **Portão 3 — Revisão do diff pelo PO** (antes de escrever no destino)
7. **Geração do `.md` e atualização do destino**

---

## 🚦 Portão 1 — Cabeçalho e destino

Todo documento tem obrigatoriamente este cabeçalho:

```
plataforma: NSRE
domínio: resseguro
funcionalidade: relatorio
```

| Campo | O que é | Exemplo |
|---|---|---|
| `plataforma` | produto/plataforma dona da funcionalidade | `NSRE` |
| `domínio` | área de negócio | `resseguro`, `cosseguro`, `sinistro`, `cotação`, `emissão`, `averbação`, `faturamento` |
| `funcionalidade` | funcionalidade/serviço documentado | `relatorio` |

Além do cabeçalho, é obrigatório saber o **destino**: a página do Confluence ou do Notion que será atualizada (link, ou título + espaço/pasta).

**Como verificar:** procure os quatro itens na instrução do usuário e no contexto da conversa (formato `plataforma: ...`, ou dito em texto livre). Um item só conta como informado se o usuário o disse explicitamente. **Nunca deduza** plataforma, domínio ou funcionalidade a partir do conteúdo do material.

**Se faltar qualquer um, pare.** Não leia material, não analise, não busque no destino. Faça uma única pergunta listando só o que falta, por exemplo:

> Antes de começar, preciso de: **plataforma**, **domínio** e **destino** (link da página no Confluence ou Notion). Já tenho: funcionalidade = relatorio.

Se o destino ainda não existir e o usuário quiser criá-lo, confirme isso, plataforma/domínio/funcionalidade continuam obrigatórios.

Se o destino for Confluence, resolva site, espaço e folder conforme "Configuração do Confluence" abaixo, sem pedir IDs técnicos ao usuário.

## Coleta do material

Fontes aceitas, em qualquer combinação:

- **Material gerado no chat**: documentos do `/refine`, saída do `/format-user-story`, rascunhos e respostas anteriores desta conversa
- **US do Azure DevOps**: link ou ID do work item. Se não houver ferramenta para ler o Azure DevOps nesta sessão, peça ao usuário para colar título, descrição, regras e critérios de aceite. Nunca invente o conteúdo de uma US a partir do número
- **Texto colado no chat**: tratado como fonte primária, igual às demais

Leia **todo** o material antes de concluir qualquer coisa: descrição, regras explícitas, critérios de aceite, exemplos, exceções, mensagens de erro, campos, limites, perfis de acesso. Registre de qual fonte veio cada regra (ex: `US-1234`, `chat`, `texto colado`).

Bugs (`/format-bug`) não são fonte de regra nova: correção de defeito é a implementação voltando a bater com a regra que já existia. Se o usuário trouxer um bug, pergunte se ele revela uma regra que nunca foi documentada; só então use.

## Leitura do destino atual

Antes de analisar, leia o conteúdo completo do destino:

- **Confluence**: `getConfluencePage` (e `getConfluencePageDescendants` se houver filhas como o histórico)
- **Notion**: `notion-fetch` na página
- Carregue as ferramentas necessárias com `ToolSearch` se ainda não estiverem disponíveis

Se o destino já tem regras, elas são a **base** da consolidação. Preserve IDs, redação e ordem das regras existentes. Se o destino está vazio ou é novo, a base é vazia. Diga ao usuário qual dos dois casos é.

## 🚦 Portão 2 — Referências a outras funcionalidades

Depois de ler material **e** destino, varra os dois em busca de qualquer referência a outra funcionalidade, serviço, tela, relatório, módulo, domínio ou regra geral. Sinais comuns:

- links ou menções a outras páginas ("conforme a regra de cotação", "ver Cosseguro")
- regras que dependem do resultado ou do estado de outra funcionalidade
- campos, status ou eventos que pertencem a outro serviço
- uma US que altera comportamento de funcionalidade vizinha
- uma regra do destino que remete a página de outro domínio

**Se encontrar qualquer uma, pare e pergunte antes de alterar qualquer coisa.** Liste cada referência com a fonte e peça uma decisão por item, por exemplo:

> Encontrei referências a outras funcionalidades:
> 1. US-1234 cita "limite de retenção do tratado" (funcionalidade `tratado`). Quero apenas **referenciar**, documentar a regra aqui como regra local, ou **incluir também** na página de `tratado`?
> 2. A página atual linka "Cálculo de prêmio". Mantenho o link como está?

Opções-padrão a oferecer por referência: (a) só referenciar com link, mantendo a regra na outra funcionalidade; (b) trazer a regra para esta funcionalidade como regra local; (c) atualizar também a outra funcionalidade (exige outro destino e novo Portão 1 para ela); (d) ignorar.

Nunca edite a outra funcionalidade por conta própria. Se não houver nenhuma referência, diga em uma linha que verificou e não encontrou, e siga.

## Análise e consolidação das regras

Com as decisões dos portões, monte a lista completa de regras:

1. Extraia cada regra de negócio do material novo, uma por vez, na menor unidade testável
2. Compare cada uma com as regras do destino e classifique:
   - **Nova**: não existe no destino → adicionar
   - **Igual**: já existe com o mesmo sentido → manter, só somar a nova fonte
   - **Complementa**: acrescenta condição, exceção ou exemplo a uma regra existente → alterar a regra existente
   - **Conflita**: contradiz uma regra existente → **não resolva sozinho**; apresente as duas versões com as fontes e pergunte qual vale
3. Regras do destino que o material novo não menciona **continuam** no documento. Só remova ou marque como descontinuada uma regra se o usuário pedir ou confirmar
4. Lacunas (valor, limite, perfil, mensagem, comportamento em erro não informados) viram **perguntas ao usuário** ou itens marcados `A DEFINIR`. Nunca preencha com suposição. Um rascunho sugerido é permitido apenas se marcado como `SUGESTÃO, validar`

Faça no máximo 3-4 perguntas por rodada, priorizando conflitos e lacunas que mudam o comportamento.

## 🚦 Portão 3 — Revisão antes de escrever

Antes de gravar no destino, mostre ao usuário um resumo curto do que vai mudar, e **não** o documento inteiro:

- quantas regras novas, alteradas, mantidas e com `A DEFINIR`
- a lista de regras novas e alteradas (ID + título + uma linha)
- decisões tomadas nos portões anteriores

Peça confirmação. Só grave no destino depois do "ok". O arquivo `.md` local pode ser gerado antes da confirmação, para o usuário revisar.

## Formato do documento `.md`

Nome do arquivo: `<plataforma>-<dominio>-<funcionalidade>.md` em minúsculas, sem acentos, ex: `nsre-resseguro-relatorio.md`. Salve no diretório de trabalho (ou no scratchpad se a sessão indicar um) e informe o caminho.

Estrutura fixa, nesta ordem:

````markdown
plataforma: NSRE
domínio: resseguro
funcionalidade: relatorio

# <Plataforma> — <Domínio> — <Funcionalidade>

**Última atualização:** DD/MM/AAAA
**Fontes:** US-1234, US-1301, chat

## Descrição
Uma ou duas frases sobre o que a funcionalidade faz.

## Regras de negócio

### RN-01 — <título curto da regra>
**Fonte:** US-1234
**Status:** Em produção | Em desenvolvimento | Rascunho | Descontinuada

```gherkin
Funcionalidade: <funcionalidade>

  Cenário: <nome do cenário>
    Dado que <contexto>
    E <outra condição>
    Quando <ação ou evento>
    Então <resultado esperado>
    E <outro resultado>
```

### RN-02 — ...

## Referências a outras funcionalidades
- <funcionalidade> — <link> — <tipo: referência | regra local trazida | atualizada junto>

## Pontos em aberto
- A DEFINIR: <lacuna>, <quem decide>

## Histórico de mudanças
| Data | Fonte | Regras | O que mudou |
|---|---|---|---|
| DD/MM/AAAA | US-1234 | RN-03 (nova), RN-01 (alterada) | resumo curto |
````

Regras de escrita:

- **Cabeçalho** (`plataforma`, `domínio`, `funcionalidade`) é sempre as três primeiras linhas, idêntico em toda versão do documento
- Gherkin em **português** (`Funcionalidade`, `Cenário`, `Esquema do Cenário`, `Dado`, `Quando`, `Então`, `E`, `Mas`), mesmo estilo em todas as regras
- Uma regra de negócio = um bloco `RN-xx` com um ou mais cenários. Regra com várias condições ou exceções ganha vários cenários (caminho feliz, exceções, limites, erros), nunca um cenário gigante
- Use `Esquema do Cenário` + `Exemplos` quando a mesma regra varia por valores (faixas, percentuais, perfis)
- Cada passo descreve **comportamento observável e testável**, sem detalhe de implementação (nada de nome de tabela, endpoint ou classe, a não ser que a US o imponha)
- **IDs `RN-xx` são estáveis**: nunca renumere, reaproveite ou reordene IDs existentes. Regras novas recebem o próximo número livre. Regra descontinuada mantém o ID com status `Descontinuada`
- Cada regra registra a **fonte**. Ao incrementar uma regra existente, some a nova fonte (`US-1234, US-1301`)
- `Status` reflete o que o usuário informou. Na dúvida entre "em produção" e "em desenvolvimento", pergunte. US é intenção, o documento deve dizer o que é verdade
- **Histórico de mudanças**: uma linha por execução com mudanças. A linha de uma execução só entra depois do "ok" do Portão 3. Bugs nunca entram

## Atualização do destino

Após o "ok" do Portão 3, atualize o destino com a versão completa do documento. Nunca sobrescreva o destino com conteúdo parcial.

**Confluence**
1. Resolva site, Cloud ID e espaço (ver abaixo)
2. Página existente: `updateConfluencePage` com `contentFormat: "markdown"` ou `"html"` conforme o conteúdo, enviando o corpo completo consolidado
3. Página nova: localize o Folder do domínio dentro do folder raiz com `searchConfluenceUsingCql` e crie com `createConfluencePage`, `parentId` do Folder. Se o Folder do domínio não existir, avise que precisa ser criado manualmente (a automação só cria páginas)
4. Cenários Gherkin vão em bloco de código, um por bloco, nunca corridos em parágrafo
5. Título único no espaço inteiro, com prefixo da plataforma e funcionalidade (ex: "NSRE — Resseguro — Relatório"), nunca só "Relatório"

**Notion**
1. `notion-fetch` na página de destino para conferir que é a correta
2. Página existente: `notion-update-page` com o conteúdo completo consolidado
3. Página nova: `notion-create-pages` sob a página/banco que o usuário indicou
4. Use blocos de código com linguagem `gherkin` para os cenários

**Depois de gravar**
- Devolva o link do destino e o caminho do `.md`, com resumo de 1-2 linhas (quantas regras novas, alteradas, em aberto). Não repita o documento no chat
- Se algum dado for sensível (ex: percentual de retenção de tratado), pergunte se a página precisa de restrição de acesso (Page Restrictions no Confluence, permissões no Notion)

## Configuração do Confluence

Site, espaço e folder **não ficam fixos nesta skill**. Vêm da configuração do plugin, injetada no início da sessão em bloco iniciado por `[product-tools] Configuração do PO:` (valor "(não configurado)" = em branco).

| Campo | Uso | Exemplo |
|---|---|---|
| `confluence_site` | site do Confluence | `nstech-empresa.atlassian.net` |
| `doc_space_key` | espaço de destino da documentação | `nsseg` |
| `doc_root_folder_id` | folder que contém os folders de domínio | `14319631` |

Ordem de resolução: (1) informado pelo PO nesta conversa → (2) bloco de configuração no contexto → (3) variáveis `CLAUDE_PLUGIN_OPTION_CONFLUENCE_SITE`, `CLAUDE_PLUGIN_OPTION_DOC_SPACE_KEY`, `CLAUDE_PLUGIN_OPTION_DOC_ROOT_FOLDER_ID` (se tiver terminal) → (4) perguntar. Nunca use valores de exemplo como se fossem configuração.

IDs técnicos são **resolvidos**, nunca pedidos ao PO:
- **Cloud ID**: `getAccessibleAtlassianResources`, pelo URL de `confluence_site`. Sem site configurado e com um só recurso, use-o; com vários, pergunte o site pelo nome
- **ID do espaço**: `getConfluenceSpaces` pela chave `doc_space_key`. Se a chave não estiver configurada e o usuário informou uma página existente por link, use o espaço do link. Caso contrário, pergunte onde publicar
- **Folder raiz**: `doc_root_folder_id`; se vazio, pergunte o **nome** do folder e localize por `searchConfluenceUsingCql` (`space = "<doc_space_key>" AND type = folder AND title = "<nome>"`)

Tickets (US e Bug) ficam no **Azure DevOps**, não no Jira, mesmo com o Confluence no mesmo tenant Atlassian. O campo `confluence_spaces` vale só para leitura no `/refine`; nunca publique nesses espaços por causa dele.

## Relação com as outras ferramentas do product-tools

- `refine` / `format-user-story` geram a US **antes** do desenvolvimento. Seus documentos são fonte válida aqui, mas confirme com o PO o que já está em produção
- `format-bug`: ver "Coleta do material"

## Princípios

- Nada de análise sem cabeçalho completo e destino. Nada de alteração sem resolver as referências a outras funcionalidades
- Sempre ler tudo (material + destino) antes de concluir; sempre devolver o documento completo e atualizado
- Nunca inventar regra, valor, ID, dono, status ou cenário. Perguntar ou marcar `A DEFINIR`
- Nunca apagar nem renumerar regra existente sem confirmação
- Conflito entre fontes é decisão do usuário, não da skill
- Nunca editar outra funcionalidade sem o usuário pedir e sem passar pelo Portão 1 para ela
