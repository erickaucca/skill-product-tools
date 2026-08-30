# Regras de Negócio — [Nome do Projeto]

> ⚠️ Este arquivo é um TEMPLATE. Substitua o conteúdo pelas regras reais do seu domínio.
> A skill de User Story usará este arquivo automaticamente para enriquecer os critérios de aceite e cenários de teste.

---

## Como usar este arquivo

Organize as regras por domínio/módulo do sistema. Para cada regra, informe:
- **Identificador** (RN-001, RN-002...)
- **Descrição** da regra
- **Quando se aplica**
- **Exceções**, se houver

---

## Exemplo de estrutura

### Módulo: Pagamentos

**RN-001 — Valor mínimo para parcelamento**
- Compras abaixo de R$ 50,00 não podem ser parceladas
- Aplica-se a todos os meios de pagamento com parcelamento

**RN-002 — Juros por faixa de parcelamento**
- Até 3x: sem juros
- De 4x a 6x: 1,99% a.m.
- De 7x a 12x: 2,99% a.m.

**RN-003 — Meios de pagamento aceitos**
- Cartão de crédito (Visa, Mastercard, Elo, Amex)
- Cartão de débito (apenas à vista)
- PIX (apenas à vista, desconto de 5%)
- Boleto bancário (vencimento em 3 dias úteis)

---

### Módulo: Usuários e Acesso

**RN-010 — Perfis de acesso**
- Cliente: acesso ao catálogo, carrinho e histórico de pedidos próprios
- Administrador: acesso total ao painel
- Atendente: acesso a pedidos e dados de clientes, sem acesso financeiro

**RN-011 — Política de senha**
- Mínimo 8 caracteres
- Ao menos 1 letra maiúscula, 1 número e 1 caractere especial
- Bloqueio após 5 tentativas incorretas (desbloqueio por e-mail)

---

## Adicione suas regras abaixo

### Módulo: [Nome do Módulo]

**RN-XXX — [Nome da Regra]**
- [Descrição]
- [Quando se aplica]
- [Exceções]
