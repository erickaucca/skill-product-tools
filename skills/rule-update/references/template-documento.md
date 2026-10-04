# Template do documento `.md` e regras de escrita Gherkin

Leia este arquivo ao gerar o `.md` (etapa 6).

Nome do arquivo: `<plataforma>-<dominio>-<funcionalidade>.md` em minúsculas, sem acentos, ex: `nsre-resseguro-relatorio.md`. Salve no diretório de trabalho (ou no scratchpad, se a sessão indicar um) e informe o caminho.

## Estrutura fixa, nesta ordem

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

````

## Regras de escrita

- **Cabeçalho** (`plataforma`, `domínio`, `funcionalidade`): sempre as três primeiras linhas, idêntico em toda versão
- Gherkin em **português** (`Funcionalidade`, `Cenário`, `Esquema do Cenário`, `Exemplos`, `Dado`, `Quando`, `Então`, `E`, `Mas`), mesmo estilo em todas as regras
- Uma regra de negócio = um bloco `RN-xx` com um ou mais cenários. Regra com várias condições ou exceções ganha vários cenários (caminho feliz, exceções, limites, erros), nunca um cenário gigante
- `Esquema do Cenário` + `Exemplos` quando a mesma regra varia por valores (faixas, percentuais, perfis)
- Cada passo descreve **comportamento observável e testável**, sem detalhe de implementação (tabela, endpoint, classe), a não ser que a US o imponha
- **IDs `RN-xx` são estáveis**: nunca renumere, reaproveite ou reordene. Regra nova recebe o próximo número livre. Regra descontinuada mantém o ID com status `Descontinuada`
- Cada regra registra a **fonte**; ao incrementar uma regra existente, some a nova fonte (`US-1234, US-1301`)
- `Status` reflete o que o usuário informou. Na dúvida entre "em produção" e "em desenvolvimento", pergunte. US é intenção, o documento diz o que é verdade
- A página da funcionalidade **não tem seção de histórico**. Ela mostra só a versão vigente das regras
- **Última atualização** e **Fontes** refletem a versão vigente e são atualizadas a cada execução

## Página de histórico (filha da página da funcionalidade)

Título: `Histórico de mudanças` (no Confluence, se o título já existir em outro caminho do espaço, `Histórico de mudanças — <Funcionalidade>`; ver `references/confluence.md`).

Conteúdo: uma descrição de uma linha e as entradas, **mais recente no topo**, uma por execução com mudanças. Só entra depois do "ok" do Portão 3 e da gravação das regras. Nunca reescreva nem apague entradas antigas, só some novas. Bugs nunca entram.

````markdown
Registro das atualizações das regras de **NSRE / Resseguro / Relatório**. A versão vigente está na página da funcionalidade.

## DD/MM/AAAA — US-1234
**Fonte:** US-1234 (título da US)
**Regras:** RN-03 (nova), RN-01 (alterada), RN-02 (descontinuada)

- **RN-03 — <título>** (nova): resumo de uma linha
- **RN-01 — <título>** (alterada): o que mudou, em uma linha
  - Antes: <condição ou resultado anterior, resumido>
  - Depois: <condição ou resultado novo, resumido>

## DD/MM/AAAA — criação inicial
**Fonte:** US-1100
**Regras:** RN-01 a RN-08 (novas)
````

- Regra **alterada** sempre traz `Antes` e `Depois`, porque a página da funcionalidade só guarda a versão vigente
- Regra nova ou descontinuada: uma linha basta
- Linke a US ao work item do Azure DevOps quando o usuário informar o link
- Primeira execução de uma funcionalidade nova: uma entrada `criação inicial`
