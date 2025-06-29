# === Bibliotecas ===

import yfinance as yf
import pandas as pd
import streamlit as st
import plotly.express as px

def importar_dados_yf(stocks, start_date, end_date):
    historical_data = []
    fundamental_data = []
        
    for symbol in stocks:

        symbol = symbol + ".SA"
        ticker = yf.Ticker(symbol)

        # 🔹 Dados históricos
        hist = ticker.history(start=start_date, end=end_date)
        hist = hist.reset_index()
        hist['Symbol'] = symbol
        historical_data.append(hist)

        # 🔹 Dados fundamentalistas (P/L, P/VP, ROE etc.)
        info = ticker.info
        fundamentals = {
            'Symbol': symbol,
            'P/L (TTM)': info.get('trailingPE'),   # P/L
            'P/VP': info.get('priceToBook'),
            'ROE': info.get('returnOnEquity'),
            'Dividend Yield': info.get('dividendYield'),
        }
        fundamental_data.append(fundamentals)

    # Exportar CSVs
    df_prices = pd.concat(historical_data)
    df_prices.to_csv('data/stock-analysis.csv')
    dataset_fundamentals = pd.DataFrame(fundamental_data)
    dataset_fundamentals.to_csv('data/stock-analysis-fundamentals.csv')

    return df_prices, dataset_fundamentals

def criar_dashboard(dataset_cotacao, dataset_fund):

    dashboard_detalhado = open("financial_agents/knowledge/dashboard_escrito.txt", encoding='utf-8', mode="w")

    text = f""
    
    st.title("Dashboard de Análise de Ativos Financeiros")

    tab1, tab2 = st.tabs(["📈 Visão Geral do Ativo", "📊 Análise Comparativa"])

    with tab1:
        # 1. gráfico

        st.subheader("📈 Visão Geral do Ativo")

        fig = px.line(
                dataset_cotacao,
                x='Date',
                y='Close',
                color='Symbol',
                title='Preço de Fechamento por Ação',
                labels={
                    "Date": "Data",
                    "Close": "Preço de Fechamento (R$)",
                    "Symbol Stock": "Símbolo da Ação"
                }
        )

        fig.update_traces(hovertemplate='<b>%{customdata[0]}</b><br>Data: %{x}<br>Fechamento: R$ %{y:.2f}<extra></extra>', customdata=dataset_cotacao[['Symbol']])
        st.plotly_chart(fig)
    
    with tab2:

        st.header("📊 Análise Comparativa")

        # Filtrar o DataFrame com base nas seleções

        # --- 1. Tabela Resumo de Métricas ---
        st.subheader("Resumo do Período")
        
        lista_metricas = []

        text += "\n\n2. Análise Comparativa:\n"

        for acao in dataset_cotacao["Symbol"].unique():
            df_acao = dataset_cotacao[dataset_cotacao['Symbol'] == acao].sort_values(by="Date")
            if not df_acao.empty:
                preco_inicial = df_acao['Close'].iloc[0]
                preco_final = df_acao['Close'].iloc[-1]
                variacao_pct = ((preco_final / preco_inicial) - 1) * 100
                volume_total = df_acao['Volume'].sum()
                
                lista_metricas.append({
                    "Ação": acao,
                    "Preço Inicial (R$)": f"{preco_inicial:.2f}",
                    "Preço Final (R$)": f"{preco_final:.2f}",
                    "Variação (%)": f"{variacao_pct:.2f}%",
                    "Volume Total": f"{volume_total:,}".replace(",", ".")
                })
                text += f"\nAção: [{acao}]\n- Preço Inicial (R$): {preco_inicial:.2f}\n- Preço Final (R$): {preco_final:.2f}\n- Variação (%): {variacao_pct:.2f}\n- Volume Total: {volume_total}\n"
        
        df_metricas = pd.DataFrame(lista_metricas)
        st.dataframe(df_metricas, use_container_width=True)

        # --- 2. Gráfico de Volume ---
        st.subheader("Volume Total Negociado no Período")
        df_volume = dataset_cotacao.groupby('Symbol')['Volume'].sum().reset_index()

        fig_volume = px.bar(
            df_volume,
            x='Symbol',
            y='Volume',
            color='Symbol',
            title='Comparativo de Volume Total',
            labels={"Symbol": "Ação", "Volume": "Volume Total Negociado"}
        )
        st.plotly_chart(fig_volume, use_container_width=True)

        st.header("Dados Fundamentalistas")

        text += "\n\n3. Dados Fundamentalistas:\n"
        
        lista_fund = []
        for acao in dataset_fund["Symbol"].unique():

            df_da_acao = dataset_fund[dataset_fund['Symbol'] == acao]
       
            if not df_da_acao.empty:

                pl = df_da_acao['P/L (TTM)'].iloc[0]
                pvp = df_da_acao['P/VP'].iloc[0]
                roe = df_da_acao['ROE'].iloc[0]
                dividend_yield = df_da_acao['Dividend Yield'].iloc[0]
                
                # 4. Adicione o dicionário com os dados CORRETOS à lista
                lista_fund.append({
                    "Symbol": acao,
                    "P/L": f"{pl:.2f}",
                    "P/VP": f"{pvp:.2f}",
                    "ROE": f"{roe:.2f}",
                    "Dividend Yield": f"{dividend_yield:.2f}",
            })
                text += f"\nAção: [{acao}]\n- P/L: {pl:.2f}\n- P/VP: {pvp:.2f}\n- ROE: {roe:.2f}\n- Dividend Yield: {dividend_yield:.2f}\n"
        df_fund = pd.DataFrame(lista_fund)
        st.dataframe(df_fund, use_container_width=True)

    dashboard_detalhado.write(str(text))
    dashboard_detalhado.close()

    return text