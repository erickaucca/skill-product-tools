# Destino Confluence

Leia este arquivo só quando o destino for Confluence.

## Raiz e IDs

A **raiz** vem da conversa: link de uma página/folder, ou nome + espaço. Do link extraia o site (`<site>.atlassian.net`) e o ID (`/pages/<id>/` ou `/folder/<id>`). Se o usuário não informou raiz, use a configuração do plugin (bloco `[product-tools] Configuração do PO:` no contexto, ou variáveis `CLAUDE_PLUGIN_OPTION_*`) **e diga qual raiz está usando**; sem nenhuma, pergunte.

| Campo de configuração | Uso |
|---|---|
| `confluence_site` | site do Confluence |
| `doc_space_key` | espaço de documentação |
| `doc_root_folder_id` | folder/página raiz sob a qual fica `plataforma / domínio / funcionalidade` |

IDs técnicos são **resolvidos**, nunca pedidos ao PO:
- **Cloud ID**: do link; senão `getAccessibleAtlassianResources` pelo URL de `confluence_site` (um só recurso: use-o; vários: pergunte o site pelo nome)
- **ID do espaço**: do link; senão `getConfluenceSpaces` pela chave. Só é necessário para criar páginas
- **ID da raiz**: do link; senão `searchConfluenceUsingCql` (`space = "<chave>" AND title = "<nome>"`)

`confluence_spaces` vale só para leitura no `/refine`; nunca publique nesses espaços por causa dele. Tickets (US e Bug) ficam no **Azure DevOps**.

## Localizar a combinação (descendo a hierarquia)

Nunca busque a funcionalidade por título solto no espaço. Desça a partir da raiz, um nível por vez:

1. **Plataforma**: filhos diretos da raiz (`searchConfluenceUsingCql`: `parent = <rootId>`; se não retornar, `getConfluencePageDescendants` na raiz). Nome igual à plataforma, ignorando maiúsculas e acentos
2. **Domínio**: filhos do nível anterior, mesmo critério
3. **Funcionalidade**: filhos do nível anterior, mesmo critério

Pare no primeiro nível que não existir: ele e os seguintes são os que faltam criar. Se o nível existir, guarde o `id` para ser o `parentId` do seguinte. Um nível existente pode ser **Folder nativo ou página**; use-o como está.

Se a página da funcionalidade existe, leia-a com `getConfluencePage`. A página filha de histórico aparece entre os filhos dela (`parent = <id da funcionalidade>`, título começando com `Histórico de mudanças`); só leia o conteúdo dela se for somar uma entrada.

## Gravação

**Combinação existente** → `updateConfluencePage` na página da funcionalidade com o corpo completo consolidado (sem seção de histórico). Depois, some a entrada no **topo** da página de histórico com `updateConfluencePage` (leia a página com `getConfluencePage`, insira a entrada nova logo após a descrição e envie o corpo completo, preservando as entradas antigas). Se a filha de histórico não existir, crie-a (`createConfluencePage`, `parentId` = id da funcionalidade). Não altere as páginas de plataforma e domínio.

**Combinação inexistente** → crie só os níveis que faltam, na ordem, cada um com `parentId` do nível acima (`createConfluencePage`):
- **Plataforma e domínio**: páginas de navegação, com uma frase de descrição e, se quiser, a macro nativa de lista de páginas filhas. Nunca regra de negócio. A automação **não cria Folders nativos**, então os níveis novos são páginas
- **Funcionalidade**: página com o documento completo
- **Histórico**: página filha da funcionalidade (`parentId` = id da funcionalidade recém-criada), com a descrição e a entrada `criação inicial`, criada logo depois da funcionalidade

**Títulos** são únicos no espaço inteiro. Use o nome puro do nível (`NSRE`, `Resseguro`, `Relatório`). A página de histórico usa `Histórico de mudanças — <Funcionalidade>` desde o início, pois o título puro repetiria entre funcionalidades. Se o nome já existir em outro caminho do espaço, o Confluence recusa: pergunte antes de criar e, se aprovado, desambigue com prefixo do nível acima (ex: `NSRE — Resseguro`, `NSRE — Resseguro — Relatório`), avisando o usuário.

Formato: Gherkin em bloco de código, um cenário por bloco, nunca corridos em parágrafo. Dado sensível (ex: percentual de retenção de tratado): pergunte se precisa de Page Restrictions; restrição no nível pai propaga para as filhas.
