# === Importação das Bibliotecas ===

import streamlit as st
from agentes import crew_ai_project
from tools import importar_dados_yf, criar_dashboard
import pandas as pd
from datetime import datetime 

b3 = pd.read_csv("data/AcoesIndices_2025-06-11.csv", sep=";")

# === Interface do Streamlit ===

st.set_page_config(page_title="Crew-AI", layout="wide")

st.title("Análise de Ações: B3 📈")

resetar = st.button("Resetar Dashboard")

if 'dashboard_gerado' not in st.session_state or resetar:
    st.session_state.dashboard_gerado = False
    st.session_state.messages = []
    st.session_state.dataset_cotacao = pd.DataFrame()
    st.session_state.dataset_fund = pd.DataFrame()
    st.session_state.acoes = []

if not st.session_state.dashboard_gerado:
    st.write("Um conjunto de Inteligencias Artificiais, preocupada em fornecer insights baseado no seu prompt!")

    acoes = st.multiselect("Informe os símbolos das ações", [acao for acao in b3['Symbols']], max_selections=5)
    start_date = st.date_input("Digite a data de início", value=datetime(2024, 1, 1))
    end_date = st.date_input("Digite a data final", value=datetime.now())
    
    # Botão para gerar o dashboard
    if st.button("Gerar Análise Inicial"):
        if acoes and start_date and end_date:
            with st.spinner("Buscando dados e construindo dashboard...", show_time=True):
                # Armazena os dados no session_state para não perdê-los
                st.session_state.dataset_cotacao, st.session_state.dataset_fund = importar_dados_yf(acoes, start_date, end_date)
                st.session_state.dataset_cotacao = st.session_state.dataset_cotacao.fillna(0)
                st.session_state.dataset_fund = st.session_state.dataset_fund.fillna(0)
                st.session_state.acoes = acoes
                
                # "Liga a chave" para indicar que a geração foi concluída
                st.session_state.dashboard_gerado = True
                
                # Força a reexecução do script para entrar no modo "chat"
                st.rerun()

        else:
            st.warning("Por favor, preencha todos os campos para gerar a análise.")


if st.session_state.dashboard_gerado:
    st.success(f"Análise gerada para as ações: {', '.join(st.session_state.acoes)}")
    
    # Recria o dashboard a partir dos dados salvos no estado da sessão
    criar_dashboard(st.session_state.dataset_cotacao, st.session_state.dataset_fund)

    st.header("💬 Converse com o Agente")
    st.write("Faça perguntas sobre os dados analisados.")

    # Exibe o histórico do chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    # Captura a nova pergunta do usuário
    if prompt := st.chat_input("Ex: Qual ação teve o maior P/L?"):

        # Adiciona a pergunta do usuário ao histórico e exibe na tela
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Chama o agente com a nova pergunta
        with st.spinner("O agente está analisando sua pergunta...", show_time=True):
            # Adapte sua função crew_ai_project para receber os dados também, se necessário
            # Ex: resultado = crew_ai_project(prompt, st.session_state.dataset_cotacao, st.session_state.dataset_fund)
            resultado = crew_ai_project(prompt) 

            # Adiciona a resposta do agente ao histórico e exibe na tela
            st.session_state.messages.append({"role": "assistant", "content": resultado})
            with st.chat_message("assistant"):
                st.markdown(resultado)