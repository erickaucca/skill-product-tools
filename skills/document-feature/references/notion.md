# Destino Notion

Leia este arquivo só quando o destino for Notion.

A **raiz** é a página (ou banco) indicada pelo usuário. Se não foi informada, pergunte.

## Localizar a combinação (descendo a hierarquia)

Nunca use busca solta pelo título da funcionalidade. Desça a partir da raiz, um nível por vez:

1. `notion-fetch` na raiz e procure entre os filhos a página da **plataforma** (nome igual, ignorando maiúsculas e acentos)
2. `notion-fetch` na plataforma e procure o **domínio**
3. `notion-fetch` no domínio e procure a **funcionalidade**

Pare no primeiro nível que não existir: ele e os seguintes são os que faltam criar. Se a funcionalidade existe, o `notion-fetch` já traz o conteúdo para a consolidação.

## Gravação

- **Combinação existente** → `notion-update-page` na página da funcionalidade com o conteúdo completo consolidado. Não altere plataforma e domínio
- **Combinação inexistente** → `notion-create-pages` só dos níveis que faltam, na ordem, cada um sob o nível acima. Plataforma e domínio são páginas de navegação com uma frase de descrição, nunca regra de negócio. A funcionalidade recebe o documento completo
- Título de cada página = nome puro do nível (`NSRE`, `Resseguro`, `Relatório`)
- Cenários em blocos de código com linguagem `gherkin`
- Dado sensível: pergunte se a página precisa de permissões restritas
