---
name: refine
description: >
  Orquestra o pipeline completo de refinamento de produto: pesquisa de mercado,
  engenharia, qualidade e escrita final da User Story, usando como insumo a base
  de conhecimento do PO no Confluence (espaço configurado no plugin). Use quando o PO/PM pedir
  para refinar, analisar ou preparar uma necessidade de produto para o backlog.
  Invocável explicitamente via /refine.
---

# Skill — Refine (Orquestrador do Pipeline)

Você orquestra as etapas do refinamento de produto, chamando um agente/skill
por vez, sempre nesta ordem:

0. Base de conhecimento no Confluence (feita por você mesmo — ver abaixo)
1. `agents/pesquisa-mercado`
2. `agents/engenharia`
3. `agents/qualidade`
4. `skills/format-user-story` (etapa final de escrita — não é um agente, é a skill
   de formatação já existente, reaproveitada aqui)

## Como receber a entrada

O comando aceita dois formatos, ambos válidos:

- `/refine` sozinho — nesse caso, peça ao PO para colar a descrição da necessidade
  na mensagem seguinte, e aguarde.
- `/refine <descrição colada na mesma linha>` — nesse caso, já use o texto recebido
  como entrada e inicie o pipeline imediatamente, sem perguntar nada antes.

Nunca peça informações adicionais (ID, título, campos extras) antes de iniciar —
a única exceção é o espaço do Confluence, quando não estiver configurado (ver Etapa 0).
Título é gerado automaticamente a partir da descrição; ID fica como placeholder
(`US-XXX`) até a etapa final.

## Etapa 0 — Base de conhecimento (Confluence)

Antes da pesquisa de mercado, busque no Confluence o que já existe sobre o tema
da necessidade (regras de negócio, funcionalidades, glossário, decisões).

### Qual espaço usar

Cada PO configura o(s) seu(s) espaço(s) ao ativar o plugin (campo
`confluence_spaces`, e opcionalmente `confluence_site`). No início da sessão o
plugin injeta essa configuração no contexto com uma linha iniciada por
`[product-tools] Configuração do PO:`. Resolva o espaço nesta ordem:

1. Espaço informado explicitamente pelo PO na própria mensagem
   (ex: `/refine espaço=NSSEGSIN ...`) — vale só para esta execução.
2. Espaço(s) da linha `[product-tools] Configuração do PO:` no contexto.
3. Variável de ambiente `CLAUDE_PLUGIN_OPTION_CONFLUENCE_SPACES`, se você tiver
   acesso a um terminal e a linha acima não estiver no contexto.
4. Se nada disso existir: esta é a **única** pergunta permitida antes de iniciar.
   Pergunte uma vez qual espaço do Confluence usar e lembre o PO de preencher a
   configuração do plugin (`confluence_spaces`) para não precisar informar de
   novo. Se o PO responder que não quer usar o Confluence, siga sem esta etapa.

Espaços separados por vírgula devem ser todos pesquisados.

### Como buscar

Use o conector Atlassian (Rovo):

1. Se `confluence_site` estiver configurado, obtenha o `cloudId` desse site via
   `getAccessibleAtlassianResources`; senão, use o único/primeiro site disponível.
2. Extraia de 2 a 5 termos-chave da necessidade (entidades de negócio, processo,
   ex: "cotação", "endosso", "franquia", "resseguro").
3. Busque com `searchConfluenceUsingCql`, restrito aos espaços resolvidos, ex:
   `space in ("NSSEG","NSSEGCOT") AND type = page AND text ~ "cotação endosso"`.
   Refaça com termos alternativos se vier vazio.
4. Leia (`getConfluencePage`) as páginas mais relevantes — no máximo 5.
   Priorize páginas no padrão da skill `document-feature`: páginas de regra de
   negócio (com Page Properties e "Lógica da regra") e páginas de
   funcionalidade (com "Comportamento esperado"). Ignore páginas de
   "Histórico de mudanças", exceto para entender uma mudança recente.

### O que anexar ao documento de trabalho

Crie o documento de trabalho já com esta seção logo após a descrição original:

```markdown
## 📚 Base de Conhecimento (Confluence)

**Espaço(s) consultado(s):** NSSEG, NSSEGCOT

| Página | Link | O que é relevante para esta necessidade |
|---|---|---|
| ... | ... | ... |

**Regras de negócio existentes que se aplicam:** ...
**Possíveis conflitos ou sobreposições com o que já existe:** ...
```

Esta etapa nunca gera `contem_criticas` sozinha: se nada relevante for
encontrado, ou o conector não estiver disponível/autenticado, registre isso na
seção (ex: "Nenhuma página relevante encontrada em NSSEG") e siga para a
pesquisa de mercado. Conflitos com regras existentes devem ser registrados aqui
para que as etapas seguintes (principalmente Engenharia) os avaliem.

## Documento de trabalho

Mantenha um único documento markdown que cresce a cada etapa aprovada. Cada agente
recebe o documento acumulado até ali e devolve o mesmo documento com uma seção nova
anexada ao final (a estrutura de cada seção está definida no próprio agente).

Nunca reescreva ou resuma seções já escritas por etapas anteriores — apenas anexe.

## Regra de execução

Para cada etapa, na ordem:

1. Invoque o agente correspondente, passando o documento de trabalho atual.
2. Leia o campo `status` no topo da resposta.
   - `status: revisado` → avance para a próxima etapa com o documento atualizado.
   - `status: contem_criticas` → **pare imediatamente**. Entregue o relatório de
     críticas ao PO exatamente como recebido do agente. Não avance para as
     próximas etapas. Não gere a US ainda.

## Retomada após crítica

Se a mensagem do PO for uma resposta a um relatório de críticas anterior nesta
mesma conversa (você reconhece isso pelo contexto — o turno anterior seu foi um
relatório de críticas), **não reinicie o pipeline do zero**:

1. Identifique qual etapa gerou a crítica.
2. Incorpore a resposta do PO ao documento de trabalho que já existia até aquela
   etapa (não descarte pesquisa de mercado/engenharia já aprovadas).
3. Invoque novamente **apenas** a etapa que travou, agora com a informação nova.
4. Se ela retornar `revisado`, continue o pipeline normalmente a partir da
   próxima etapa. Se travar de novo, repita o mesmo relatório de críticas.

## Etapa final — escrita

Quando as três primeiras etapas retornarem `revisado`, chame a skill
`format-user-story` passando o documento de trabalho completo (descrição
original + base de conhecimento + pesquisa de mercado + notas de engenharia +
plano de testes sugerido)
como insumo. Ela é responsável por gerar o arquivo `.md` final no padrão DoR e
apresentá-lo via `present_files` — você não precisa reimplementar esse
formato aqui.

Depois de apresentar a US, lembre o PO em uma linha: quando a US for entregue,
`/product-tools:document-feature` atualiza a página da funcionalidade e o
histórico de mudanças no Confluence.

## O que esta skill não faz

- Não escreve nem altera páginas no Confluence — a base de conhecimento é
  somente leitura.
- Não busca arquivos de contexto do projeto locais (regras de negócio,
  glossário) — o contexto vem da conversa com o PO e do Confluence.
