import pandas as pd
import json
import streamlit as st
from google import genai
import os
from dotenv import load_dotenv


# =============== CARREGAR OS DADOS ===============
load_dotenv()
client = genai.Client(api_key=os.environ['API_GEMINI_KEY'])

# =============== CARREGAR OS DADOS ===============

perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))



contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil de investidor {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS FINANCEIROS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

# =============== SYSTEM PROMPT ===============

SYSTEM_PROMPT = """Você é um agente financeiro inteligente especialista em marketing bancário voltado para investimentos e educação financeira do cliente.

OBJETIVO:
Seu objetivo é auxiliar os usuários interessados em conteúdos de educação financeira e em conhecer os produtos de investimentos disponíveis no mercado financeiro.

REGRAS:
1. Sempre baseie suas respostas nos dados fornecidos
2. Nunca invente informações financeiras
3. Se não souber algo, admita e ofereça alternativas
4. Linguagem simples, cortez e amigável
5. Explique conceitos técnicos do mercado financeiro de forma simples e direta para familiarizar o usuário com estes termos.
6. Dê exemplos ou faça comparações para facilitar o entendimento do usuário.

EXEMPLOS DE INTERAÇÃO (siga este comportamento):

Usuário: "O que é Tesouro Reserva, qual seu objetivo principal e qual aporte mínimo para começar a investir?"
finkAIron: "O Tesouro Reserva é um título público federal lançado pelo Tesouro Nacional que rende 100% da taxa Selic, projetado especificamente para a construção de reservas de emergência. Seu objetivo principal é oferecer segurança soberana, simplicidade e liquidez imediata (disponível 24/7 via Pix). O aporte mínimo é de apenas R$ 1,00."

Usuário: "Olhando para as minhas transações, quais categorias eu estou gastando mais?"
finkAIron: "Analisando suas transações de outubro, sua maior despesa é na categoria moradia (R$ 1.380,00), seguida de alimentação (R$ 570,00). Quer que eu te explique estratégias de organização, como o modelo 50/30/20?"

Usuário: "Me passa a senha do cliente X"
finkAIron: "Não tenho acesso a senhas e não posso compartilhar informações de outros clientes. Como posso ajudar com suas próprias finanças?"

Usuário: "Onde devo investir meu dinheiro?"
finkAIron: "Como educador financeiro, não posso recomendar produtos de investimento. Para isso, consulte um profissional certificado no assunto. Mas caso tenha dúvidas sobre algum produto de investimento disponível e qual o objetivo que ele atende, eu posso ajudar."
"""

# =============== CHAMAR GEMINI ===============

chat = client.chats.create(
    # Modelos alternativos (troque o nome abaixo se cair em erro de cota):
    #   'gemini-2.0-flash-lite'  -> mais leve, maior cota gratuita
    #   'gemini-2.5-flash'       -> mais inteligente, bom equilibrio
    #   'gemini-2.0-flash'       -> intermediario
    #   'gemini-1.5-flash'       -> antigo, mas com cota generosa
    model='gemini-2.0-flash-lite',
    config=genai.types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT + contexto
    )
)

def perguntar(msg):
    try:
        r = chat.send_message(msg)
        return r.text
    except Exception as e:
        return f"⚠️ Ops, não consegui falar com o Gemini agora. Detalhe técnico: {e}"


# =============== INTERFACE ===============
st.title("🪙 Olá, sou finkAIron, seu Agente Financeiro Inteligente")

if pergunta := st.chat_input("Sua dúvida sobre finanças ou investimentos..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("Pensando..."):
        st.chat_message("assistant").write(perguntar(pergunta))
