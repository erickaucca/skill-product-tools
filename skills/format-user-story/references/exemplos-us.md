# Exemplos de User Stories — Referência

Use estes exemplos como padrão de qualidade ao formatar novas histórias.

---

## Exemplo 1 — Funcionalidade de Checkout

**[US-042] Parcelamento no checkout**

### Descrição
> Como **cliente autenticado**,
> quero **parcelar minha compra em até 12 vezes no cartão de crédito**,
> para **ter mais flexibilidade no pagamento de compras de alto valor**.

### Critérios de Aceite
- [ ] CA01 — O sistema exibe opções de parcelamento apenas para compras acima de R$ 50,00
- [ ] CA02 — Compras até R$ 300,00 permitem parcelamento em até 3x sem juros
- [ ] CA03 — Compras acima de R$ 300,00 permitem parcelamento em até 12x com juros de 2,99% a.m.
- [ ] CA04 — O valor total com juros é exibido antes da confirmação do pedido
- [ ] CA05 — Cartões de débito não exibem opção de parcelamento

### Plano de Testes

```gherkin
Cenário: Cliente parcela compra acima de R$ 300,00
  Dado que o cliente tem uma compra de R$ 500,00 no carrinho
  E está autenticado com cartão de crédito válido
  Quando seleciona a opção de 6x no checkout
  Então o sistema exibe o valor de cada parcela (R$ 88,70)
  E exibe o total com juros (R$ 532,20)
  E permite confirmar o pedido

Cenário: Cliente tenta parcelar compra abaixo do limite mínimo
  Dado que o cliente tem uma compra de R$ 30,00 no carrinho
  Quando acessa a tela de pagamento
  Então o sistema não exibe opções de parcelamento
  E exibe apenas a opção de pagamento à vista

Cenário: Cartão recusado na finalização do parcelamento
  Dado que o cliente selecionou parcelamento em 3x
  Quando confirma o pedido com um cartão sem limite suficiente
  Então o sistema exibe a mensagem "Pagamento recusado. Verifique os dados ou tente outro cartão."
  E não processa o pedido
  E mantém o carrinho intacto
```

---

## Exemplo 2 — Funcionalidade de Notificação

**[US-078] Notificação de status do pedido**

### Descrição
> Como **cliente que realizou uma compra**,
> quero **receber notificações sobre o status do meu pedido**,
> para **acompanhar a entrega sem precisar acessar o site**.

### Critérios de Aceite
- [ ] CA01 — O cliente recebe e-mail ao confirmar o pedido (status: "Pedido recebido")
- [ ] CA02 — O cliente recebe e-mail quando o pedido é enviado (status: "Pedido enviado") com código de rastreio
- [ ] CA03 — O cliente recebe notificação push (se o app estiver instalado) em cada mudança de status
- [ ] CA04 — O cliente pode desativar notificações push nas configurações da conta
- [ ] CA05 — E-mails são enviados em até 5 minutos após a mudança de status

### Plano de Testes

```gherkin
Cenário: Cliente recebe e-mail ao confirmar pedido
  Dado que o cliente finalizou uma compra com sucesso
  Quando o sistema confirma o pagamento
  Então um e-mail com assunto "Pedido #12345 confirmado!" é enviado em até 5 minutos
  E o e-mail contém o resumo dos itens e o valor total

Cenário: Cliente com notificações push desativadas
  Dado que o cliente desativou notificações push nas configurações
  Quando o status do pedido muda para "Enviado"
  Então o sistema envia apenas o e-mail de notificação
  E não tenta enviar push notification

Cenário: Falha no envio de e-mail
  Dado que o servidor de e-mail está indisponível
  Quando o sistema tenta enviar notificação de status
  Então o sistema registra o erro no log
  E tenta reenviar após 10 minutos (máximo 3 tentativas)
```
