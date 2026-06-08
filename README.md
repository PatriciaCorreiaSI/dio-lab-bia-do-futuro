# 🪙 finkAIron — Agente Financeiro Inteligente

Chatbot de educação financeira e investimentos construído com **Streamlit** (interface)
e a **API do Google Gemini** como modelo de linguagem (LLM).

O agente responde dúvidas do usuário usando, como contexto, o perfil do cliente,
suas transações, o histórico de atendimentos e os produtos financeiros disponíveis.

---

## 🤔 Por que Gemini, e não Ollama local?

O desafio original da **DIO** sugere usar o **Ollama** para rodar o modelo localmente.
Optei por uma abordagem **na nuvem com o Google Gemini** por três motivos principais:

- **☁️ Sem peso na máquina local:** rodar um LLM com Ollama consome bastante CPU,
  memória RAM (e idealmente GPU) do computador. Com o Gemini, todo o processamento
  acontece nos servidores do Google — a máquina do usuário só envia a pergunta e
  recebe a resposta.

- **💪 Mais robustez no modelo:** sem a limitação do hardware local, é possível usar
  modelos significativamente maiores e mais capazes do que os que caberiam de forma
  confortável em uma máquina comum, resultando em respostas de melhor qualidade.

- **🆓 Cota gratuita generosa e acessível:** entre as LLMs em nuvem mais conhecidas, o
  Gemini oferece, em geral, uma das camadas gratuitas mais amplas e fáceis de obter —
  basta uma conta Google e uma chave gerada no AI Studio, sem cartão de crédito. Isso
  torna o projeto reproduzível por qualquer pessoa, sem custo de infraestrutura.

> Em resumo: a nuvem troca a dependência de um hardware potente por uma dependência de
> conexão com a internet — uma troca vantajosa para um projeto de estudo que deve ser
> leve de rodar e fácil de reproduzir.

---

## 🧠 Como o Gemini é usado como LLM

A integração com o Gemini é feita pelo SDK oficial **`google-genai`** e segue 3 etapas no
arquivo [`src/app.py`](src/app.py):

1. **Conexão (cliente):** a chave da API é lida de uma variável de ambiente e usada para
   criar o cliente do Gemini.
   ```python
   client = genai.Client(api_key=os.environ['API_GEMINI_KEY'])
   ```

2. **Configuração do modelo (chat com memória + system prompt):** criamos uma sessão de chat
   já com as instruções de sistema (papel do agente + contexto do cliente). Assim, essas
   instruções são enviadas **uma única vez** e valem para toda a conversa.
   ```python
   chat = client.chats.create(
       model='gemini-2.0-flash-lite',
       config=genai.types.GenerateContentConfig(
           system_instruction=SYSTEM_PROMPT + contexto
       )
   )
   ```

3. **Conversa:** cada pergunta do usuário é enviada com `send_message`, e o modelo responde
   levando em conta o system prompt e o histórico da conversa.
   ```python
   r = chat.send_message(msg)
   return r.text
   ```

> 💡 Modelos alternativos (caso queira trocar): `gemini-2.5-flash`, `gemini-2.0-flash`,
> `gemini-1.5-flash`. Basta alterar o parâmetro `model=` na criação do chat.

---

## 🚀 Como rodar o projeto

### 1. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar a chave da API
- Gere uma chave gratuita no [Google AI Studio](https://aistudio.google.com/apikey).
- Copie o arquivo `.env.example` para um novo arquivo chamado `.env`.
- Cole a sua chave nesse `.env`:
  ```
  API_GEMINI_KEY=sua_chave_aqui
  ```

### 3. Executar o app
```bash
streamlit run src/app.py
```
O app abre no navegador. É só digitar a dúvida sobre finanças/investimentos.

---

## 📁 Estrutura

```
.
├── src/
│   └── app.py                 # Código principal (interface + integração Gemini)
├── data/                      # Dados de contexto do cliente
│   ├── perfil_investidor.json
│   ├── transacoes.csv
│   ├── historico_atendimento.csv
│   └── produtos_financeiros.json
├── .env.example               # Modelo de configuração da chave (copie para .env)
├── requirements.txt           # Dependências do projeto
└── .gitignore                 # Protege o .env e arquivos temporários
```

---

## 🔐 Segurança

A chave da API fica no arquivo `.env`, que é ignorado pelo Git (via `.gitignore`) e
**nunca** é enviado ao repositório. Cada pessoa que rodar o projeto usa a sua própria chave.
