# === Importação das Bibliotecas ===

import streamlit as st
from financial_agents.src.financial_agents.main import crew_ai_project
from utils.create_dashboard import create_dashboard
from utils.yahoo_data import import_data_yf
import pandas as pd
from datetime import datetime 

b3 = pd.read_csv("data/AcoesIndices_2025-06-11.csv", sep=";")

if "provider" not in st.session_state:
    st.session_state.provider = ""
    st.session_state.api_key = ""
    st.session_state.apiNotConfigured = True

@st.dialog("Escolha seu provedor de LLM")
def llmChoose():
    st.session_state.provider  = st.selectbox("Digite um provedor de LLM: ", options=["OpenAI", "Groq"])

    st.session_state.api_key = st.text_input(f"Digite a chave de API da {st.session_state.provider }", type="password")

    if st.button("Submit"):
        st.session_state.apiNotConfigured = False     
        st.rerun()

# === Interface do Streamlit ===

st.set_page_config(page_title="Crew-AI", layout="wide")
st.title("Análise de Ativos: B3 📈")

st.write("Um conjunto de Inteligencias Artificiais, preocupada em fornecer insights baseado no seu prompt!")

tab1, tab2 = st.tabs(["Resetar Dashboard", "Configurar API KEY"])

with tab1:
    resetar = st.button(key="reset",label="Clique aqui")

with tab2:
    if st.button(key="alterarKey",label="Clique aqui"):
        llmChoose()

if 'dashboard_gerado' not in st.session_state or resetar:
    st.session_state.dashboard_gerado = False
    st.session_state.messages = []
    st.session_state.dataset_cotacao = pd.DataFrame()
    st.session_state.dataset_fund = pd.DataFrame()
    st.session_state.acoes = []
    

if not st.session_state.dashboard_gerado:

    acoes = st.multiselect("Informe os símbolos dos ativos", [acao for acao in b3['Symbols']], max_selections=5)
    start_date = st.date_input("Digite a data de início", value=datetime(2024, 1, 1))
    end_date = st.date_input("Digite a data final", value=datetime.now())
    
    if st.button("Gerar Análise Inicial"):

        if acoes and start_date and end_date:

            if st.session_state.api_key != "" and st.session_state.provider != "":

                with st.spinner("Buscando dados e construindo dashboard...", show_time=True):
                    # Armazena os dados no session_state para não perdê-los
                    st.session_state.dataset_cotacao, st.session_state.dataset_fund = import_data_yf(acoes, start_date, end_date)
                    st.session_state.dataset_cotacao = st.session_state.dataset_cotacao.fillna(0)
                    st.session_state.dataset_fund = st.session_state.dataset_fund.fillna(0)
                    st.session_state.acoes = acoes
                    st.session_state.dashboard_gerado = True
                    
                    st.rerun()
            
            st.warning(f"Por favor, configure sua chave de API.")
        else:
            st.warning("Por favor, preencha todos os campos para gerar a análise.")


if st.session_state.dashboard_gerado:

    st.success(f"Análise gerada para as ações: {', '.join(st.session_state.acoes)}")
    st.success(f"O provedor de LLM utilizado será: {st.session_state.provider}")
    
    conteudo_dashboard = create_dashboard(st.session_state.dataset_cotacao, st.session_state.dataset_fund)

    # Escreve em um arquivo ".txt" o dashboard gerado para entrega-lo em forma de contexto para os agentes.
    with open('financial_agents\knowledge\dashboard_escrito.txt', 'w', encoding='UTF-8' ) as f:
        f.write(conteudo_dashboard)

    st.header("💬 Converse com o Agente")
    st.write("Faça perguntas sobre os dados analisados.")

    # Exibe o histórico do chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    # Captura a nova pergunta do usuário
    if prompt:= st.chat_input("Ex: Qual ativo teve o maior P/L?", disabled=st.session_state.apiNotConfigured):

        # Adiciona a pergunta do usuário ao histórico e exibe na tela
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Chama o agente com a nova pergunta
        with st.spinner("O agente está analisando sua pergunta...", show_time=True):

            with open("financial_agents/knowledge/dashboard_escrito.txt", "r", encoding="UTF-8", ) as arquivo:
                conteudo = arquivo.read()

            resultado = crew_ai_project(prompt, conteudo, st.session_state.provider, st.session_state.api_key) 

            # Adiciona a resposta do agente ao histórico e exibe na tela
            st.session_state.messages.append({"role": "assistant", "content": resultado})

            with st.chat_message("assistant"):
                st.markdown(resultado)