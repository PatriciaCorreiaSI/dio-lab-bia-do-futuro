# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Para que serve no finkAIron? |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Conhecer melhor o usuario a partir de seu histórico de interações anteriores. |
| `perfil_investidor.json` | JSON | Personalizar as explicações a partir do perfil do usuário. |
| `produtos_financeiros.json` | JSON | Conhecer os produtos de investimento disponíveis adequados ao perfil do cliente para explicar suas vantagens e riscos.|
| `transacoes.csv` | CSV | Analisar padrão de gastos do cliente para personalizar as respostas ao usuário. |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

[Sua descrição aqui]

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

[ex: Os JSON/CSV são carregados no início da sessão e incluídos no contexto do prompt]

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

[Sua descrição aqui]

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Dados do Cliente:
- Nome: João Silva
- Perfil: Moderado
- Saldo disponível: R$ 5.000

Últimas transações:
- 01/11: Supermercado - R$ 450
- 03/11: Streaming - R$ 55
...
```
