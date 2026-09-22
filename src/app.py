"""
Grana — Assistente Virtual de Educação Financeira
Protótipo funcional em Streamlit + Google Gemini API

Desafio DIO: Construa Seu Assistente Virtual Com Inteligência Artificial
"""

import json
import csv
import os
from pathlib import Path

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# --- Configuração ------------------------------------------------------------

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error(
        "Variável de ambiente GEMINI_API_KEY não encontrada.\n\n"
        "Copie `.env.example` para `.env` e cole sua chave gratuita da "
        "API do Google Gemini (https://aistudio.google.com/app/apikey)."
    )
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
modelo = genai.GenerativeModel("gemini-1.5-flash")

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

SYSTEM_PROMPT = """Você é o Grana, um assistente virtual de educação financeira pessoal. Seu objetivo
é ajudar a pessoa usuária a entender melhor seus hábitos financeiros e aprender
conceitos de educação financeira de forma simples e acolhedora.

Regras de comportamento:

1. Baseie suas respostas SOMENTE nos dados fornecidos no contexto desta conversa
   (transações, perfil e metas do usuário). Nunca invente valores, datas ou
   transações que não estejam no contexto.

2. Se a pergunta não puder ser respondida com os dados disponíveis, diga
   claramente que você não tem essa informação, em vez de supor ou inventar.

3. Explique conceitos financeiros de forma simples, sem jargão, como se
   estivesse conversando com alguém que está começando a organizar a vida
   financeira agora.

4. NUNCA recomende produtos financeiros específicos (ações, fundos,
   criptomoedas, seguros de terceiros) nem faça promessas de rentabilidade.
   Sempre reforce que decisões de investimento devem ser tomadas com apoio
   de um profissional certificado ou instituição regulada.

5. Seja empático e livre de julgamento sobre os hábitos de consumo da pessoa
   usuária. Seu papel é orientar, não repreender.

6. Sempre que fizer sentido, termine a resposta sugerindo um próximo passo
   prático e realista.

7. Responda sempre em português do Brasil, em tom conversacional e acessível.
"""


# --- Carregamento da base de conhecimento -------------------------------------

@st.cache_data
def carregar_transacoes():
    caminho = DATA_DIR / "transacoes.csv"
    with open(caminho, encoding="utf-8") as arquivo:
        return list(csv.DictReader(arquivo))


@st.cache_data
def carregar_json(nome_arquivo):
    caminho = DATA_DIR / nome_arquivo
    with open(caminho, encoding="utf-8") as arquivo:
        return json.load(arquivo)


def montar_contexto(pergunta):
    """Monta o contexto enviado ao modelo filtrando os dados por palavra-chave.

    Não é uma busca semântica (RAG com embeddings) — para este protótipo,
    filtragem simples é suficiente e mais fácil de auditar: dá pra saber
    exatamente o que foi enviado à IA em cada resposta.
    """
    transacoes = carregar_transacoes()
    perfil = carregar_json("perfil_usuario.json")
    metas = carregar_json("metas_financeiras.json")
    glossario = carregar_json("glossario_financeiro.json")

    pergunta_lower = pergunta.lower()
    partes = [f"Perfil do usuário: {json.dumps(perfil, ensure_ascii=False)}"]

    palavras_transacao = ["gastei", "gasto", "transaç", "compra", "categoria", "mês", "mes"]
    if any(p in pergunta_lower for p in palavras_transacao):
        partes.append(f"Transações recentes: {json.dumps(transacoes[-15:], ensure_ascii=False)}")

    palavras_meta = ["meta", "economizar", "poupar", "objetivo", "viagem", "reserva"]
    if any(p in pergunta_lower for p in palavras_meta):
        partes.append(f"Metas financeiras: {json.dumps(metas, ensure_ascii=False)}")

    for termo, definicao in glossario.items():
        if termo.lower() in pergunta_lower:
            partes.append(f"Definição de '{termo}': {definicao}")

    return "\n\n".join(partes)


def perguntar_ao_agente(pergunta):
    contexto = montar_contexto(pergunta)

    prompt_completo = f"""{SYSTEM_PROMPT}

--- CONTEXTO DISPONÍVEL ---
{contexto}

--- PERGUNTA DO USUÁRIO ---
{pergunta}
"""

    resposta = modelo.generate_content(prompt_completo)
    return resposta.text


# --- Interface Streamlit -------------------------------------------------------

st.set_page_config(page_title="Grana — Educação Financeira", page_icon="💰")
st.title("💰 Grana — seu assistente de educação financeira")
st.caption(
    "Protótipo do desafio DIO 'Construa Seu Assistente Virtual Com IA'. "
    "Todos os dados usados aqui são fictícios."
)

if "historico" not in st.session_state:
    st.session_state.historico = []

for mensagem in st.session_state.historico:
    with st.chat_message(mensagem["papel"]):
        st.markdown(mensagem["conteudo"])

pergunta_usuario = st.chat_input("Pergunte algo sobre suas finanças...")

if pergunta_usuario:
    st.session_state.historico.append({"papel": "user", "conteudo": pergunta_usuario})
    with st.chat_message("user"):
        st.markdown(pergunta_usuario)

    with st.chat_message("assistant"):
        with st.spinner("Grana está pensando..."):
            resposta = perguntar_ao_agente(pergunta_usuario)
            st.markdown(resposta)

    st.session_state.historico.append({"papel": "assistant", "conteudo": resposta})
