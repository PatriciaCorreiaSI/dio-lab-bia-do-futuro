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

Os dados podem ser inseridos diratamente no prompt, garantindo o melhor contexto para o agente. Idealmente estas informações deverão ser carregadas dinamicamente.

```text
DADOS DO CLIENTE (data/perfil_investidor.json):
{
  "nome": "João Silva",
  "idade": 32,
  "profissao": "Analista de Sistemas",
  "renda_mensal": 5000.00,
  "perfil_investidor": "moderado",
  "objetivo_principal": "Construir reserva de emergência",
  "patrimonio_total": 15000.00,
  "reserva_emergencia_atual": 10000.00,
  "aceita_risco": false,
  "metas": [
    {
      "meta": "Completar reserva de emergência",
      "valor_necessario": 15000.00,
      "prazo": "2026-06"
    },
    {
      "meta": "Entrada do apartamento",
      "valor_necessario": 50000.00,
      "prazo": "2027-12"
    }
  ]
}

TRANSACOES DO CLIENTE (data/transacoes.csv):
data,descricao,categoria,valor,tipo
2025-10-01,Salário,receita,5000.00,entrada
2025-10-02,Aluguel,moradia,1200.00,saida
2025-10-03,Supermercado,alimentacao,450.00,saida
2025-10-05,Netflix,lazer,55.90,saida
2025-10-07,Farmácia,saude,89.00,saida
2025-10-10,Restaurante,alimentacao,120.00,saida
2025-10-12,Uber,transporte,45.00,saida
2025-10-15,Conta de Luz,moradia,180.00,saida
2025-10-20,Academia,saude,99.00,saida
2025-10-25,Combustível,transporte,250.00,saida

HISTÓRICO DE ATENDIMENTO AO CLIENTE (data/historico_atendimento.csv):
data,canal,tema,resumo,resolvido
2025-09-15,chat,CDB,Cliente perguntou sobre rentabilidade e prazos,sim
2025-09-22,telefone,Problema no app,Erro ao visualizar extrato foi corrigido,sim
2025-10-01,chat,Tesouro Selic,Cliente pediu explicação sobre o funcionamento do Tesouro Direto,sim
2025-10-12,chat,Metas financeiras,Cliente acompanhou o progresso da reserva de emergência,sim
2025-10-25,email,Atualização cadastral,Cliente atualizou e-mail e telefone,sim

PRODUTOS DISPONIVEIS NO MERCADO FINANCEIRO (data/produtos_financeiros.json):
[
  {
    "nome": "Tesouro Selic",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "100% da Selic",
    "aporte_minimo": 30.00,
    "indicado_para": "Reserva de emergência e iniciantes"
  },
  {
    "nome": "CDB Liquidez Diária",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "102% do CDI",
    "aporte_minimo": 100.00,
    "indicado_para": "Quem busca segurança com rendimento diário"
  },
  {
    "nome": "LCI/LCA",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "95% do CDI",
    "aporte_minimo": 1000.00,
    "indicado_para": "Quem pode esperar 90 dias (isento de IR)"
  },
  {
    "nome": "Fundo Multimercado",
    "categoria": "fundo",
    "risco": "medio",
    "rentabilidade": "CDI + 2%",
    "aporte_minimo": 500.00,
    "indicado_para": "Perfil moderado que busca diversificação"
  },
  {
    "nome": "Fundo de Ações",
    "categoria": "fundo",
    "risco": "alto",
    "rentabilidade": "Variável",
    "aporte_minimo": 100.00,
    "indicado_para": "Perfil arrojado com foco no longo prazo"
  },
  {
    "nome": "Tesouro Reserva",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "100% da taxa Selic com Resgate e Aplicação 24/7",
    "aporte_minimo": 1.00,
    "indicado_para": "Perfil conservador ou iniciante que deseja construir ou manter uma reserva de emergência com liquidez imediata e sem oscilações diárias"
  },
   {
    "nome": "Tesouro RendA+",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "IPCA + taxa de juros real (definida no momento da compra)",
    "aporte_minimo": 30.00,
    "indicado_para": " Investidores focados no longo prazo, especialmente trabalhadores e autônomos que desejam construir uma renda complementar para a aposentadoria com segurança."
  },
]
```
---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
DADOS DO CLIENTE:
- Nome: João Silva
- Perfil: Moderado
- Saldo disponível: R$ 5.000
- Objetivo: Construir reserva de emergência
- Patrimonio total: 15000.00
- Reserva de emergencia: 10000.00

RESUMO DOS GASTOS POR CATEGORIA:
- Moradia: R$ 1.380
- Alimentação: R$ 570
- Transporte: R$ 295
- Saúde: R$ 188
- Lazer: R$ 55,00
- Total de saídas: R$ 2.488.90

PRODUTOS DE INVESTIMENTO DISPONÍVEIS:
- Tesouro Selic (risco: baixo, perfil indicado: reserva de emergência e iniciantes)
- CDB Liquidez Diária (risco: baixo, perfil indicado: quem busca segurança com rendimento diário)
- LCI/LCA (risco: baixo, perfil indicado: quem pode esperar 90 dias (isento de IR)
- Fundo Multimercado (risco: médio, perfil indicado: moderado que busca diversificação)
- Fundo de Ações: (risco: alto, perfil indicado: arrojado com foco no longo prazo)
- Tesouro Reserva (risco: baixo, perfil indicado: reserva de emergência e iniciantes que buscam liquidez imediata sem oscilações diárias)
- Tesouro RendA+ (risco: baixo, perfil indicado: foco no longo prazo, especialmente trabalhadores e autônomos que desejam construir uma renda complementar para a aposentadoria)
...
```
