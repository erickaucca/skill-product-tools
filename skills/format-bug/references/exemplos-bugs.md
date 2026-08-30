# Exemplos de Bugs — Referência NSTECH

Use estes exemplos como padrão de qualidade ao formatar novos bugs.

---

## Exemplo 1 — Bug em fluxo de pagamento

**[BUG-091] Checkout — valor da parcela exibido como R$ 0,00 ao usar cartão Elo em 12x**

### Descrição
Clientes que tentam parcelar compras acima de R$ 300,00 em 12x utilizando cartão Elo visualizam R$ 0,00 como valor da parcela e ficam impedidos de finalizar a compra. O bug afeta diretamente a conversão de vendas no ambiente de produção.

### Contexto
- **Módulo**: Checkout > Pagamento > Parcelamento
- **Fluxo de reprodução**:
  1. Autenticar como cliente com compra acima de R$ 300,00 no carrinho
  2. Acessar a tela de checkout
  3. Selecionar "Cartão de Crédito" como meio de pagamento
  4. Informar dados de um cartão Elo válido
  5. Selecionar a opção "12x" no seletor de parcelamento

### Cenário Atual
O campo de valor da parcela exibe "R$ 0,00" e o botão "Confirmar pedido" permanece desabilitado (cinza), impedindo a finalização da compra.

### Cenário Desejado
O sistema deve calcular e exibir o valor correto da parcela (ex: para R$ 500,00 em 12x com 2,99% a.m. → R$ 49,48/parcela) e habilitar o botão "Confirmar pedido".

### Usuário
- **Perfil**: Cliente autenticado
- **Conta de teste**: cliente-teste@nstech.com.br (HML) — senha: Teste@2024

### Ambiente
| Campo | Valor |
|-------|-------|
| **Ambiente** | PRD e HML |
| **Versão** | v2.14.3 |
| **Navegador** | Chrome 124, Firefox 125, Safari 17 |
| **Data** | 03/05/2026 às 09h15 |

### Evidências
- [x] Print da tela com R$ 0,00 (anexo: `print-bug-091.png`)
- [x] Log de erro no console: `TypeError: Cannot read property 'installmentValue' of null at checkout.js:342`
- [x] ID de transação com falha: TXN-20260503-00847

### Critérios de Aceite
- [ ] CA01 — O valor da parcela é calculado e exibido corretamente para cartão Elo em todas as faixas de parcelamento (2x a 12x)
- [ ] CA02 — O botão "Confirmar pedido" é habilitado quando todos os dados do cartão são válidos e a parcela selecionada é exibida corretamente
- [ ] CA03 — O comportamento correto é mantido para as demais bandeiras (Visa, Mastercard, Amex)
- [ ] CA04 — Nenhum erro é registrado no console ao selecionar parcelamento com cartão Elo

### Plano de Testes

```gherkin
Cenário: Parcelamento em 12x com cartão Elo exibe valor correto após correção
  Dado que o cliente tem uma compra de R$ 500,00 no carrinho
  E está autenticado com cartão Elo válido
  Quando seleciona a opção de 12x no checkout
  Então o sistema exibe o valor correto da parcela (R$ 49,48)
  E exibe o total com juros (R$ 593,76)
  E o botão "Confirmar pedido" está habilitado

Cenário: Regressão — parcelamento com Visa continua funcionando
  Dado que o cliente tem uma compra de R$ 300,00 no carrinho
  E está autenticado com cartão Visa válido
  Quando seleciona a opção de 6x no checkout
  Então o sistema exibe o valor correto da parcela
  E o botão "Confirmar pedido" está habilitado

Cenário: Limite mínimo de parcelamento preservado para Elo
  Dado que o cliente tem uma compra de R$ 40,00 no carrinho
  E está autenticado com cartão Elo válido
  Quando acessa a tela de pagamento
  Então o sistema não exibe opções de parcelamento
  E exibe apenas pagamento à vista
```

### Classificação
| Campo | Valor |
|-------|-------|
| **Severidade** | 🔴 Crítico |
| **Prioridade** | 🔴 Urgente |
| **Tipo** | Funcional |
| **Frequência** | Sempre |

---

## Exemplo 2 — Bug visual com impacto em usabilidade

**[BUG-104] Painel Admin — coluna "Status" truncada em resoluções menores que 1280px**

### Descrição
Na listagem de pedidos do painel administrativo, a coluna "Status" é cortada em monitores com resolução inferior a 1280px de largura, exibindo apenas os primeiros 3 caracteres do status. O problema afeta atendentes que utilizam notebooks.

### Contexto
- **Módulo**: Painel Admin > Pedidos > Listagem
- **Fluxo de reprodução**:
  1. Autenticar como Atendente ou Administrador
  2. Acessar o menu "Pedidos"
  3. Visualizar a tabela de listagem em um monitor ou janela com menos de 1280px de largura

### Cenário Atual
A coluna "Status" exibe apenas "Pen..." ao invés de "Pendente", "Env..." ao invés de "Enviado", impossibilitando a leitura do status sem expandir a janela.

### Cenário Desejado
A coluna "Status" deve exibir o texto completo ou, em resoluções menores, adicionar tooltip ao passar o mouse sobre o status truncado.

### Usuário
- **Perfil**: Atendente e Administrador
- **Conta de teste**: admin@nstech.com.br (HML)

### Ambiente
| Campo | Valor |
|-------|-------|
| **Ambiente** | PRD e HML |
| **Versão** | v2.14.3 |
| **Resolução afetada** | < 1280px de largura |
| **Navegadores** | Chrome, Firefox, Edge |
| **Data** | 04/05/2026 às 14h00 |

### Evidências
- [x] Print comparativo: 1920px (OK) vs 1024px (truncado) — anexo: `print-bug-104.png`
- [ ] Log de erro: não aplicável (bug visual)

### Critérios de Aceite
- [ ] CA01 — Em resoluções abaixo de 1280px, a coluna "Status" exibe o texto completo sem truncamento
- [ ] CA02 — Caso o texto seja truncado por limitação de layout, um tooltip com o status completo é exibido ao passar o mouse
- [ ] CA03 — O ajuste não quebra o layout da tabela em resoluções maiores (1280px, 1440px, 1920px)

### Plano de Testes

```gherkin
Cenário: Status exibido corretamente em resolução 1024px após correção
  Dado que o atendente está autenticado no painel
  E a janela do navegador está com 1024px de largura
  Quando acessa a listagem de pedidos
  Então todos os status são exibidos sem truncamento
  Ou apresentam tooltip com o texto completo ao passar o mouse

Cenário: Regressão — layout preservado em 1920px
  Dado que o administrador está autenticado no painel
  E a janela está em resolução 1920px
  Quando acessa a listagem de pedidos
  Então a tabela exibe todas as colunas corretamente sem sobreposição
```

### Classificação
| Campo | Valor |
|-------|-------|
| **Severidade** | 🟡 Médio |
| **Prioridade** | 🟡 Normal |
| **Tipo** | Visual |
| **Frequência** | Sempre (em resoluções < 1280px) |
