# Formato Padrão — Relatório de Críticas

> Arquivo de referência compartilhado pelos agentes do pipeline `refine`
> (`pesquisa-mercado`, `engenharia`, `qualidade`). Caminho sugerido no pacote:
> `product-tools/skills/refine/references/formato-criticas.md`
>
> Qualquer agente do pipeline que precisar retornar `status: contem_criticas`
> deve gerar o corpo do documento **exatamente** neste formato. O orquestrador
> (`refine`) só interpreta o campo `status` no topo — o restante é para leitura
> humana (PO/PM).

---

## Contrato de saída (topo do documento)

Todo agente do pipeline retorna sempre estas duas informações, nesta ordem:

```
status: revisado | contem_criticas
---
[corpo do documento — US/bug final OU relatório de críticas abaixo]
```

---

## Template — Relatório de Críticas

Use este template sempre que `status: contem_criticas`.

```markdown
status: contem_criticas
---

## 🔎 Relatório de Críticas

**Necessidade avaliada:** [título/resumo curto da US ou bug]
**Etapa:** [Pesquisa de Mercado | Engenharia | Qualidade]

---

### 📝 Resumo

[2-3 linhas: o que foi avaliado e o motivo geral de não estar "revisado" ainda]

---

### ⚠️ Pontos de Atenção

| # | Criticidade | Categoria | Descrição | Sugestão / Pergunta ao PO |
|---|---|---|---|---|
| 1 | 🔴 Bloqueante | [ver categorias por etapa abaixo] | [descrição objetiva do problema] | [o que o PO precisa responder ou decidir] |
| 2 | 🟡 Recomendação | [...] | [...] | [...] |

**Legenda de criticidade:**
- 🔴 **Bloqueante** — impede seguir para a próxima etapa do pipeline
- 🟡 **Recomendação** — não impede, mas deveria ser esclarecido antes do desenvolvimento

---

### ✅ O que já está validado

- [x] [item que passou nesta etapa — evita retrabalho de revisão nas próximas rodadas]
- [x] [...]

---

### ➡️ Próximo Passo

[Ex: "Aguardando resposta do PO sobre os pontos 1 e 2 antes de seguir para Qualidade" /
"Recomendações registradas — segue para próxima etapa mediante aceite do PO"]
```

---

## Categorias de crítica por etapa

Cada agente usa apenas as categorias relevantes ao seu escopo — não inventar categorias fora desta lista sem necessidade.

| Etapa | Categorias válidas |
|---|---|
| **Pesquisa de Mercado** | Regra de mercado divergente / Prática de mercado não considerada / Risco regulatório |
| **Engenharia** | Falta de informação / Ambiguidade / Escopo / Risco técnico / Dependência não mapeada |
| **Qualidade** | Critério de aceite não testável / Cenário de teste ausente / Consistência com caso similar já resolvido |

---

## Regra de decisão do pipeline

Por padrão, **qualquer crítica** (mesmo 🟡 Recomendação) interrompe o pipeline e retorna o relatório ao PO — não segue automaticamente para a próxima etapa. O PO decide se resolve o ponto e relança o `/refine`, ou se aceita seguir mesmo com a recomendação em aberto.

---

## Exemplo preenchido (etapa Engenharia)

```markdown
status: contem_criticas
---

## 🔎 Relatório de Críticas

**Necessidade avaliada:** Parcelamento de checkout em até 12x
**Etapa:** Engenharia

---

### 📝 Resumo

A descrição cobre bem o fluxo principal, mas falta definir o comportamento em caso de
falha na parcela intermediária e não há critério de aceite testável para o limite de 12x.

---

### ⚠️ Pontos de Atenção

| # | Criticidade | Categoria | Descrição | Sugestão / Pergunta ao PO |
|---|---|---|---|---|
| 1 | 🔴 Bloqueante | Falta de informação | Não está definido o que acontece se o pagamento de uma parcela falhar após a confirmação do pedido | O pedido deve ser cancelado, ficar pendente, ou seguir e cobrar via régua de cobrança? |
| 2 | 🟡 Recomendação | Escopo | Não menciona se o limite de 12x vale para todas as bandeiras ou só para as citadas | Confirmar se Elo/Visa/Master têm o mesmo limite ou se varia por bandeira |

---

### ✅ O que já está validado

- [x] Ator, ação e benefício estão claros
- [x] Fluxo principal (happy path) bem descrito

---

### ➡️ Próximo Passo

Aguardando resposta do PO sobre os pontos 1 e 2 antes de seguir para Qualidade.
```
