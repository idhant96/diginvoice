"""Bollinger Bands."""

import os
import pandas as pd
import matplotlib.pyplot as plt


def symbol_to_path(symbol, base_dir=""):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame()

    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col=['YEAR', 'MONTH', 'HEAD'],
                              parse_dates=True, usecols=['YEAR', 'MONTH', 'HEAD', 'AMOUNT'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'AMOUNT': symbol})
        if (df.empty):
            df = df_temp
        else:
            df = df.join(df_temp)

    return df


def plot_data(df, title="POB"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()


def test_run():
    # Read data
    symbol = ["target", "sap"]
    df = get_data(symbol)

    df = df.groupby(['YEAR', 'MONTH', 'HEAD'])["sap", "target"].sum()
    df['PERCENTAGE'] = (df["sap"] / df["target"]) * 100
    del df["sap"]
    del df["target"]
    df = df.unstack()

    plot_data(df)


if __name__ == "__main__":
    test_run()
