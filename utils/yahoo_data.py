# === Bibliotecas ===
import yfinance as yf
import pandas as pd

def import_data_yf(stocks, start_date, end_date):

    if stocks == 0 or start_date == 0  or end_date == 0 :
        return "Ocorreu um Erro! Alguns campos vieram vazios..."

    try:
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
    
    except Exception:
        return "Ocorre algum erro ao tentar importar os dados!"