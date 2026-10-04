# Destino Confluence

Leia este arquivo só quando o destino for Confluence.

## Atalho: usuário informou o link da página

Extraia do URL o site (`<site>.atlassian.net`) e o `pageId` (`/pages/<id>/`). Com isso:
- **Cloud ID**: use o próprio site do link. Só chame `getAccessibleAtlassianResources` se `getConfluencePage` não aceitar o site direto
- **Espaço e folder**: dispensados, a página já existe. Não chame `getConfluenceSpaces` nem busque folders

## Página nova (sem link)

Site, espaço e folder **não ficam fixos nesta skill**. Vêm da configuração do plugin, injetada no início da sessão em bloco iniciado por `[product-tools] Configuração do PO:` (valor "(não configurado)" = em branco).

| Campo | Uso | Exemplo |
|---|---|---|
| `confluence_site` | site do Confluence | `nstech-empresa.atlassian.net` |
| `doc_space_key` | espaço de destino da documentação | `nsseg` |
| `doc_root_folder_id` | folder que contém os folders de domínio | `14319631` |

Ordem de resolução: (1) informado pelo PO nesta conversa → (2) bloco de configuração no contexto → (3) variáveis `CLAUDE_PLUGIN_OPTION_CONFLUENCE_SITE`, `CLAUDE_PLUGIN_OPTION_DOC_SPACE_KEY`, `CLAUDE_PLUGIN_OPTION_DOC_ROOT_FOLDER_ID` (se tiver terminal) → (4) perguntar. Nunca use valores de exemplo como configuração.

IDs técnicos são **resolvidos**, nunca pedidos ao PO:
- **Cloud ID**: `getAccessibleAtlassianResources`, pelo URL de `confluence_site`. Sem site configurado e com um só recurso, use-o; com vários, pergunte o site pelo nome
- **ID do espaço**: `getConfluenceSpaces` pela chave `doc_space_key`. Sem chave configurada, pergunte onde publicar
- **Folder do domínio**: dentro do folder raiz (`doc_root_folder_id`; se vazio, pergunte o **nome** do folder e localize com `searchConfluenceUsingCql`: `space = "<doc_space_key>" AND type = folder AND title = "<nome>"`). Depois localize o Folder do domínio com `title ~ "<domínio>"`. Se não existir, avise que precisa ser criado manualmente (a automação só cria páginas)

O destino é **sempre** `doc_space_key`. `confluence_spaces` vale só para leitura no `/refine`; nunca publique nesses espaços por causa dele.

## Leitura

`getConfluencePage` no destino. Chame `getConfluencePageDescendants` só se o usuário disser que existem páginas filhas relevantes (ex: histórico antigo em página separada).

## Gravação

- Existente: `updateConfluencePage` com o corpo completo consolidado
- Nova: `createConfluencePage` com `parentId` do Folder do domínio
- Gherkin em bloco de código, um cenário por bloco, nunca corridos em parágrafo
- Título único no espaço inteiro, com prefixo da plataforma e funcionalidade (ex: "NSRE — Resseguro — Relatório"), nunca só "Relatório"
- Dado sensível (ex: percentual de retenção de tratado): pergunte se precisa de Page Restrictions. Restrição na pasta do domínio propaga para as filhas

Tickets (US e Bug) ficam no **Azure DevOps**, não no Jira, mesmo com o Confluence no mesmo tenant Atlassian.
