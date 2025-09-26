import yfinance as yf
import pandas as pd

def get_data(tickers, start_date, end_date=None, save=False):

    "Generates pd.DataFrame with Close Adj from tickers"

    assert len(tickers) > 1, "We need at least two tickers to evaluate the efficient strategy"

    print(f"Collecting data for tickers {tickers}...")
    df = yf.download(tickers, start=start_date, end=end_date, progress=True, auto_adjust=False)["Adj Close"]

    file_name = "../files/"

    for i in range(0, len(tickers)):
        t = tickers[i]
        file_name += t

        if i == len(tickers) - 1:
            file_name += ".csv"
            break


        file_name += "_"
        

    if save:
        df.to_csv(file_name, index=False)

    print("Data collected")

    return df