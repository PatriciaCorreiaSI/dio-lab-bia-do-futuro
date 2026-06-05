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

Inclui dos produtos de investimento de renda fixa: Tesouro Reserva e Tesouro RendA+ que são dois produtos do Tesouro Direto muito vantajosos e não constavam na lista.

---

## Estratégia de Integração

### Como os dados são carregados?

Inserir os dados diretamente no prompt ou carregar os arquivos via código, com uso de python, conforme o script abaixo: 


```python
# Utilizando Python para carregar e ler os arquivos

import pandas as pd
import json

historico_atendimento = pd.read_csv('data/historico_atendimento.csv')
transacoes_cliente = pd.read_csv('data/transacoes.csv')

with open('data/perfil_investidor.json', 'r', encoding='utf-8') as f:
   perfil = json.load(f)

with open('data/produtos_financeiros.json', 'r', encoding='utf-8') as f:
   produtos = json.load(f)

```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

```text
DADOS DO CLIENTE:
PERFIL DO CLIENTE:
TRANSACOES DO CLIENTE:
PRODUTOS DISPONIVEIS NO MERCADO FINANCEIRO:
  PARA QUAL PERFIL ESSE PRODUTO SE APLICA:

```
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
