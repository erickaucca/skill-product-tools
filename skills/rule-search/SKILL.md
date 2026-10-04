---
name: rule-search
description: "Localiza e exibe no chat, em Markdown, as regras de negócio (Gherkin) de uma funcionalidade documentada no Confluence ou Notion, na estrutura plataforma / domínio / funcionalidade. Somente leitura. Se não encontrar, informa em que nível parou para o usuário ajustar. Use quando o usuário pedir para consultar, buscar, ver ou listar regras de um sistema, funcionalidade ou domínio. Invocável via /rule-search."
---

# Consulta de Regras de Negócio

Localiza a página de regras de uma funcionalidade (criada pelo `/rule-update`) e mostra o conteúdo **no chat, em Markdown**. **Somente leitura**: nunca cria, altera, move nem apaga nada.

## 1. Informações necessárias

| Campo | Exemplo | Obrigatório |
|---|---|---|
| `plataforma` | `NSRE` | sim |
| `domínio` | `resseguro` | sim |
| `funcionalidade` | `relatorio` | sim |
| `raiz` | link ou nome da página/folder raiz, no Confluence ou Notion | sim |
| `filtro` | ID de regra (`RN-03`) ou palavra-chave | não |

Só conta o que o usuário disse explicitamente; nunca deduza plataforma, domínio ou funcionalidade. Se faltar algum obrigatório, **pare e faça uma única pergunta** listando só o que falta, sem buscar nada. Se o usuário informar direto o link da página da funcionalidade, ele dispensa plataforma, domínio, funcionalidade e raiz (leia a página e extraia o cabeçalho dela).

Sem raiz na conversa, use a configuração do plugin (`doc_space_key`, `doc_root_folder_id`, ver `references/confluence.md` de `rule-update`) e **diga qual raiz está usando**; sem nenhuma, pergunte.

## 2. Localização

Desça a hierarquia a partir da raiz, um nível por vez (plataforma → domínio → funcionalidade), comparando nomes sem diferenciar maiúsculas nem acentos. Nunca busque por título solto no espaço inteiro.

- Confluence: siga as seções "Raiz e IDs" e "Localizar a combinação" de `../rule-update/references/confluence.md`
- Notion: siga a seção "Localizar a combinação" de `../rule-update/references/notion.md`
- Leia só essas seções; ignore as de gravação. Carregue as ferramentas com `ToolSearch` se preciso

Se houver mais de uma página candidata no mesmo nível, liste as candidatas e pergunte qual.

## 3. Resposta quando encontrou

Leia a página da funcionalidade e responda **com o conteúdo em Markdown direto no chat** (não dentro de bloco de código, para os blocos `gherkin` renderizarem), nesta ordem:

1. Uma linha: `Encontrado: NSRE / Resseguro / Relatório` + link da página
2. O documento: cabeçalho (`plataforma`, `domínio`, `funcionalidade`), descrição, regras `RN-xx` com seus cenários Gherkin, referências a outras funcionalidades e pontos em aberto, exatamente como estão na página
3. Histórico de mudanças: omita por padrão e diga em uma linha que existe; mostre só se o usuário pedir

Com `filtro`:
- **ID** (`RN-03`): mostre só essa regra, mais a linha do cabeçalho
- **Palavra-chave**: mostre as regras cujo título, fonte ou cenários contenham o termo (ignorando maiúsculas e acentos) e diga quantas de quantas bateram
- Se o filtro não bater em nenhuma regra, use a resposta de "não localizado" (nível: regra)

Não resuma, não reescreva e não corrija as regras: reproduza o que está na página. Se algo parecer inconsistente ou desatualizado, aponte numa linha ao final, sem alterar o texto. Se a página tiver `A DEFINIR`, mantenha.

## 4. Resposta quando **não** localizou

Informe de forma direta que **não foi localizado**, diga em que nível parou e o que existe naquele nível, para o usuário ajustar:

```
Não localizei as regras de NSRE / Resseguro / Relatório.

Encontrado até: raiz › NSRE › Resseguro
Não existe: funcionalidade "Relatório"
Existem em "Resseguro": Cálculo de Prêmio, Sinistro Resseguro

Ajuste o nome da funcionalidade, a raiz ou o domínio e tente de novo.
Para criar a documentação, use /rule-update.
```

- Níveis possíveis de falha: raiz inacessível, plataforma, domínio, funcionalidade, regra (filtro sem resultado)
- Liste os irmãos existentes do nível em que parou (até ~10) para facilitar a correção. Se um nome for parecido com o pedido (ex: `Relatorios`), aponte como possível correspondência, **sem assumir** que é a certa
- Raiz sem acesso ou ferramenta indisponível: diga isso, não "não encontrado"
- Nunca invente regras nem preencha com conhecimento geral quando não localizar

## Princípios

- Somente leitura; nada é criado nem alterado
- Pergunte só o que impede a busca; uma pergunta por vez
- Reproduza fielmente o que está na página
- Não localizado é uma resposta válida: diga onde parou, não adivinhe
