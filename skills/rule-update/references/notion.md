# Destino Notion

Leia este arquivo só quando o destino for Notion.

A **raiz** é a página (ou banco) indicada pelo usuário. Se não foi informada, pergunte.

## Localizar a combinação (descendo a hierarquia)

Nunca use busca solta pelo título da funcionalidade. Desça a partir da raiz, um nível por vez:

1. `notion-fetch` na raiz e procure entre os filhos a página da **plataforma** (nome igual, ignorando maiúsculas e acentos)
2. `notion-fetch` na plataforma e procure o **domínio**
3. `notion-fetch` no domínio e procure a **funcionalidade**

Pare no primeiro nível que não existir: ele e os seguintes são os que faltam criar. Se a funcionalidade existe, o `notion-fetch` já traz o conteúdo para a consolidação e lista as páginas filhas, entre elas a de histórico (`Histórico de mudanças`); só faça fetch dela para somar uma entrada.

## Gravação

- **Combinação existente** → `notion-update-page` na página da funcionalidade com o conteúdo completo consolidado (sem seção de histórico). Depois, `notion-update-page` com `update_content` na página de histórico: `old_str` = a linha de descrição, `new_str` = a descrição seguida da entrada nova (entrada mais recente no topo), sem tocar nas entradas antigas. Se a filha de histórico não existir, crie-a sob a funcionalidade. Não altere plataforma e domínio
- **Combinação inexistente** → `notion-create-pages` só dos níveis que faltam, na ordem, cada um sob o nível acima. Plataforma e domínio são páginas de navegação com uma frase de descrição, nunca regra de negócio. A funcionalidade recebe o documento completo e, depois dela, a página filha `Histórico de mudanças` com a entrada `criação inicial`
- Título de cada página = nome puro do nível (`NSRE`, `Resseguro`, `Relatório`)
- Cenários em blocos de código com linguagem `gherkin`
- Dado sensível: pergunte se a página precisa de permissões restritas

- Antes de gravar conteúdo, leia `notion://docs/enhanced-markdown-spec` com `notion-fetch` para usar a sintaxe correta
- Prefira `update_content`/`insert_content` (edição mínima) a `replace_content`; use `replace_content` na funcionalidade só para a consolidação completa, preservando páginas filhas (o histórico) com as tags exatas do fetch
