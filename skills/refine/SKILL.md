---
name: refine
description: >
  Orquestra o pipeline completo de refinamento de produto: pesquisa de mercado,
  engenharia, qualidade e escrita final da User Story. Use quando o PO/PM pedir
  para refinar, analisar ou preparar uma necessidade de produto para o backlog.
  Invocável explicitamente via /refine.
---

# Skill — Refine (Orquestrador do Pipeline)

Você orquestra as quatro etapas do refinamento de produto, chamando um agente/skill
por vez, sempre nesta ordem:

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

Nunca peça informações adicionais (ID, título, campos extras) antes de iniciar.
Título é gerado automaticamente a partir da descrição; ID fica como placeholder
(`US-XXX`) até a etapa final.

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
original + pesquisa de mercado + notas de engenharia + plano de testes sugerido)
como insumo. Ela é responsável por gerar o arquivo `.md` final no padrão DoR e
apresentá-lo via `present_files` — você não precisa reimplementar esse
formato aqui.

## O que esta skill não faz

- Não consulta base de conhecimento de produto (MCP) — essa etapa não existe
  ainda neste MVP.
- Não busca arquivos de contexto do projeto (regras de negócio, glossário) —
  todo contexto vem da conversa com o PO.
