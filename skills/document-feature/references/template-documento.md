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

## Histórico de mudanças
| Data | Fonte | Regras | O que mudou |
|---|---|---|---|
| DD/MM/AAAA | US-1234 | RN-03 (nova), RN-01 (alterada) | resumo curto |
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
- **Histórico de mudanças**: uma linha por execução com mudanças, só depois do "ok" do Portão 3. Bugs nunca entram
