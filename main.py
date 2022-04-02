# Obtain tickers in the S&P500.

import requests
import pandas as pd
import yfinance as yf
from bs4 import BeautifulSoup


def get_sp500_instruments():
    res = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = BeautifulSoup(res.content, "lxml")
    table = soup.find_all("table")[0]
    df = pd.read_html(str(table))
    return list(df[0]["Symbol"])


tickers = get_sp500_instruments()
print(tickers)

def get_sp500_df():
    symbols = get_sp500_instruments()
    ohlcvs = {}
    for symbol in symbols:
        symbol_df = yf.Ticker(symbol).history(period="10y")
        ohlcvs[symbol] = symbol_df[["Open", "High", "Low", "Close", "Volume"]].rename(
            columns={
                "Open": "open",
                "High": "close",
                "Low": "low",
                "Close": "close",
                "Volume": "volume"
            }
        )
        #print(symbol_df)


get_sp500_df()