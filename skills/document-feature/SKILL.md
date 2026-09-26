---
name: document-feature
description: "Cria ou atualiza páginas de funcionalidade, regra de negócio e histórico de mudanças no Confluence (espaço nsseg) da Nstech, sempre seguindo o template fixo definido nesta skill. Use sempre que o usuário pedir para documentar uma funcionalidade, um serviço, uma regra de negócio (cotação, emissão, sinistro, resseguro, cosseguro, averbação, faturamento), ou criar/atualizar o changelog de uma página no Confluence após a entrega de uma US, mesmo que a palavra 'skill' ou 'template' não apareça explicitamente. Invocável via /document-feature."
---

# Confluence — Documentação de Regras e Funcionalidades (nsseg)

Skill fonte canônica dos templates de documentação de regras de negócio e funcionalidades da Nstech no Confluence. Toda mudança de estrutura começa aqui — o Content Template do Confluence (Space Settings → Content Templates) é só um espelho estático desta skill e deve ser atualizado manualmente depois, nunca o contrário.

## Contexto fixo do espaço

- Site: `nstech-empresa.atlassian.net` — Cloud ID: `443ab39d-4972-4aec-a2bf-2244c082ad0a`
- Espaço `nsseg`: id `14549010`
- Folder `Tecnologia`: id `14352407`
- Folder `Serviços e sistemas` (dentro de Tecnologia): id `14319631`
- Dentro de `Serviços e sistemas`, cada **domínio** (Averbação, Faturamento, Resseguro, Sinistro, Cotação, Emissão, Cosseguro...) é um **Folder** nativo do Confluence (container puro), não uma página. Se o domínio ainda não existir como Folder, ele precisa ser criado manualmente no Confluence (ferramentas de automação atuais só criam Páginas, não Folders nativos) — avise o usuário em vez de tentar criar via API.
- Tickets (US e Bug) ficam no **Azure DevOps**, não no Jira, mesmo estando no mesmo tenant Atlassian que o Confluence.
- O destino da documentação é **sempre** o espaço `nsseg`, mesmo que o PO tenha configurado outros espaços no plugin (`confluence_spaces`). Essa configuração vale só para a *leitura* da base de conhecimento no `/refine`; só publique em outro espaço se o PO pedir explicitamente nesta conversa.

## Relação com as outras ferramentas do product-tools

- `refine` / `format-user-story` → geram a US **antes** do desenvolvimento. Esta skill documenta a regra **depois** que ela é verdade (US aprovada/entregue).
- Se a conversa já tiver um documento do `/refine` ou uma US do `format-user-story`, use-o como insumo do intake: descrição, regras citadas na seção "📚 Base de Conhecimento", critérios de aceite (viram cenários Dado/Quando/Então) e exemplos. Mesmo assim, confirme com o PO o que já está em produção — US é intenção, a página documenta o que é verdade hoje.
- `format-bug` → bugs **nunca** geram atualização de página nem de histórico (ver seção 3).

## Quando usar

- Pedido para criar/documentar uma página de funcionalidade ou serviço
- Pedido para criar/atualizar uma regra de negócio (macro, cross-sistema)
- Pedido para registrar uma mudança no histórico de uma funcionalidade após uma US ser entregue
- Pedido para "equalizar"/padronizar páginas existentes no espaço nsseg com o template

## Os três tipos de página (nunca misturar)

### 1. Página de funcionalidade (uma por serviço/funcionalidade, dentro do domínio)

Estrutura fixa, nesta ordem — não pular seção; se faltar dado, perguntar, nunca inventar:

1. **Título e descrição curta** — o que a funcionalidade faz
2. **Regras de negócio aplicadas** — lista de **links** para páginas de regra (tipo 2 abaixo). Nunca reescrever o conteúdo da regra aqui
3. **Regras específicas desta funcionalidade** — texto direto inline, sem link, sem Page Properties, sem dono/status (é só uma restrição local, não uma regra de negócio — ver teste abaixo)
4. **Comportamento esperado** — cenários em **Dado / Quando / Então** (Gherkin), um por bloco, cada um testável e mapeável quase 1:1 para lógica de código
5. **Exemplos** — tabela simples entrada → resultado esperado, para apoiar QA na massa de teste
6. **Link para "Histórico de mudanças"** no rodapé — sempre como página **filha** separada, nunca como bloco na mesma página

Princípio: a página documenta **o que é verdade hoje**. Não é um mural de tudo que já mudou — isso é papel do histórico (tipo 3).

### 2. Página de regra de negócio (macro / cross-sistema)

Só cria página própria se passar no teste: *outra funcionalidade, em outro sistema ou domínio, precisaria consultar essa regra também?* Se não, é regra específica (fica inline na página de funcionalidade, tipo 1 seção 3).

Bloco de propriedades estruturadas (Page Properties) no topo:

| Campo | Descrição |
|---|---|
| ID da regra | identificador único e estável, ex: `resseguro.sinistro.limite-franquia-auto` |
| Domínio | ex: Resseguro, Averbação, Faturamento |
| Escopo | Geral / Módulo específico |
| Módulo(s) aplicável(is) | pode listar vários |
| Regra geral relacionada | link, se especializa uma regra mais ampla |
| Status | Rascunho / Em revisão / Aprovada / Em produção / Descontinuada |
| Responsável | nome ou time |
| Sistema(s) impactado(s) | ex: i4Pro Sinistro |

Seções de conteúdo:
- **Descrição** — o que a regra determina, em prosa curta
- **Lógica da regra** — formato estruturado fixo, sempre a mesma sintaxe (ex: `SE valor_sinistro > franquia_minima ENTÃO aciona_ressegurador = true`), para leitura confiável por humano e por eventual interpretador automatizado
- **Comentários** — usar o recurso nativo de comentários do Confluence, não uma seção manual

Histórico/versionamento da regra em si = histórico de revisões nativo do Confluence. Não duplicar manualmente.

### 3. Página "Histórico de mudanças" (filha de cada página de funcionalidade)

Formato de changelog — mesmo princípio do `log.md` usado em OKF:

| Data | US | Título | O que mudou na regra |
|---|---|---|---|
| 12/09/2026 | US-0002 | Melhoria no cálculo de massa de teste | Passou a considerar apólices com endosso ativo |

Regras de inclusão:
- Só entram **User Stories que alteram uma regra de negócio ou comportamento documentado**
- **Bugs nunca entram** — correção de defeito não é mudança de regra, é a implementação sendo ajustada para bater com a regra que já existia
- Campo "US" sempre linka direto para o work item no **Azure DevOps**
- Atualização desta página nunca é automática — só depois que a US for aprovada/entregue, e só quando o usuário pedir explicitamente

## Intake obrigatório (perguntar antes de montar conteúdo)

Faça no máximo 3-4 perguntas por rodada. Nunca inventar regra de negócio, cenário Gherkin ou exemplo que o usuário não forneceu — proponha um rascunho calibrado ao domínio para validação, mas sinalize claramente o que é sugestão.

Para página de funcionalidade:
- [ ] Domínio (Averbação, Faturamento, Resseguro, etc.) e se o Folder do domínio já existe no espaço
- [ ] Nome da funcionalidade/serviço (o título tem que ser único no espaço inteiro — nunca só "Solicitações" ou "Histórico" sem prefixo)
- [ ] Descrição curta do que a funcionalidade faz
- [ ] Quais regras de negócio (tipo 2) já existem e se aplicam aqui — se uma regra citada ainda não tem página, perguntar se deve ser criada agora ou só referenciada como pendente
- [ ] Regras específicas locais (se houver)
- [ ] Cenários Dado/Quando/Então — peça ao usuário em texto livre, ou ofereça um rascunho baseado na descrição para validação
- [ ] Exemplos de entrada → resultado esperado
- [ ] Se algum dado sensível (ex: percentual de retenção de tratado) exige Page Restriction específica

Para página de regra de negócio, colete todos os campos da tabela de Page Properties antes de criar.

## Fluxo de trabalho — publicação no Confluence

1. Carregue as ferramentas do Atlassian Rovo se ainda não estiverem carregadas (`ToolSearch` por "Confluence")
2. Confirme o domínio (Folder) de destino — localize com `searchConfluenceUsingCql` (ex: `space = "nsseg" AND title ~ "<nome do domínio>"`); nunca peça o ID técnico ao usuário, resolva por busca. Se o Folder não existir, avise que precisa ser criado manualmente antes (automação não cria Folders nativos)
3. Antes de criar uma página nova num domínio que já tem outras páginas de funcionalidade, busque uma existente (`searchConfluenceUsingCql` + `getConfluencePage`) e use como referência de fidelidade ao template — a estrutura deve ficar consistente entre funcionalidades do mesmo domínio
4. Crie a página de funcionalidade com `createConfluencePage` (`contentFormat: "html"`), `parentId` do Folder do domínio
5. Logo em seguida, crie a página filha "Histórico de mudanças — <nome da funcionalidade>" com `parentId` da página de funcionalidade recém-criada, já com a tabela de changelog (vazia ou com a primeira linha, se houver)
6. No rodapé da página de funcionalidade, garanta o link para a página de Histórico criada
7. Devolva o link de cada página criada (`_links.webui` + base URL do site) e um resumo de 1-2 linhas — não repita o conteúdo inteiro no chat

Para página de regra de negócio, mesmo fluxo, mas o `parentId` é o Folder do domínio diretamente (ou a página de regras gerais do domínio, se o usuário preferir agrupar) e o Page Properties block vai no topo via macro nativa do Confluence.

Conversão de blocos comuns para HTML+ do Confluence:
- Tabelas normais → `<table>`
- Page Properties → macro nativa de Page Properties (não uma tabela solta)
- Cenários Gherkin → bloco de código ou lista, um cenário por bloco, nunca todos corridos em um parágrafo só

## Segurança e permissões

- Preferir **Page Restrictions** por página/pasta a criar espaços separados — mantém navegação e busca unificadas
- Regra com dado sensível (ex: percentual de retenção de tratado específico) deve ter visualização/edição restrita a grupo específico (ex: "Resseguro-Financeiro") — perguntar ao usuário se aplica
- Restrição aplicada na pasta de domínio propaga para as páginas filhas — não precisa repetir por página

## Página de índice / Sumário

Papel puramente navegacional — nunca conter regra de negócio escrita diretamente nela. Usa a macro **Page Properties Report** do Confluence para agregar automaticamente regras gerais do domínio e regras específicas por módulo via filtro de labels (não só hierarquia de pastas) — uma regra pode aparecer em mais de um agrupamento sem duplicar a página, só adicionando o label correspondente.

## Princípios gerais

- Esta skill é a fonte canônica da estrutura (originada em PRODUTO_DEFINICOES.md, seção 8). Se o usuário pedir para mudar a estrutura de algum template, a mudança é feita aqui primeiro, e só depois replicada manualmente no Content Template do Confluence (Space Settings → Content Templates) — lembre o usuário desse segundo passo manual, esta skill não consegue criar Content Templates via API
- Nunca inventar ID de regra, baseline, dono, status ou cenário — sempre perguntar ou marcar como "a definir"
- Regra específica de funcionalidade nunca vira página própria, nunca ganha Page Properties — só texto inline (teste da seção 2 decide isso)
- Bug nunca entra no histórico de mudanças — só US que altera regra/comportamento documentado
- Não repita o conteúdo completo da página no chat depois de criar — resuma e aponte para o link
- Ao equalizar uma página existente para seguir o template, compare seção a seção com uma página de referência do mesmo domínio antes de perguntar o que falta