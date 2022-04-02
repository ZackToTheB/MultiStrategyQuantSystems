# Obtain tickers in the S&P500.

import requests
import pandas as pd
import yfinance as yf
from bs4 import BeautifulSoup


def get_sp500_instruments():  # get thr ticker symbols for each company
    res = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = BeautifulSoup(res.content, "lxml")
    table = soup.find_all("table")[0]
    df = pd.read_html(str(table))
    return list(df[0]["Symbol"])


def get_sp500_df():  # Get the data for each stock into a single dataframe
    symbols = get_sp500_instruments()
    symbols = symbols[:30]
    ohlcvs = {}
    loop = 1
    for symbol in symbols:
        symbol_df = yf.Ticker(symbol).history(period="10y")
        ohlcvs[symbol] = symbol_df[["Open", "High", "Low", "Close", "Volume"]].rename(
            columns={
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume"
            }
        )
        # print(loop, symbol, "\n", ohlcvs[symbol])
        loop += 1

    df = pd.DataFrame(index=ohlcvs["GOOGL"].index)
    df.index.name = "date"
    instruments = list(ohlcvs.keys())

    for instrument in instruments:
        instrument_df = ohlcvs[instrument]
        print(instrument, instrument_df)
        input()
        columns = list(map(lambda x: "{} {}".format(instrument, x), instrument_df.columns))  # this transforms open, high... to AAPL open, AAPL high...
        df[columns] = instrument_df

    return df, instruments


df, instruments = get_sp500_df()

df.to_excel("./Data/sp500_data.xlsx")
