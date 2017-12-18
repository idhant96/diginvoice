"""Bollinger Bands."""

import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly
import numpy as np
import collections

plotly.tools.set_credentials_file(username='jayendragothi', api_key='1WfjekNfgrUCaYungn9A')

bubbles_mpl = plt.figure()


def symbol_to_path(symbol, base_dir=""):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbol):
    """Read data (adjusted close) for given symbols from CSV files."""
    df_temp = pd.read_csv(symbol_to_path(symbol), na_values=['nan'])
    return df_temp


def plot_data(df, title="POB"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()


def get_performance(sales, targets):
    # get 2017 data only
    sales_17 = sales.ix[sales["Year"] == 2017]
    targets_17 = targets.ix[targets["Year"] == 2017]

    # get sales
    sales_17 = sales_17.groupby(['Month', 'Region', 'Head'])["Sale"].sum()
    targets_17 = targets_17.groupby(['Month', 'Region', 'Head'])["Target"].sum()
    performance = (sales_17 / targets_17) * 100

    return performance


def get_call_average(visits_df, att_df):
    # filter this years data
    visits_df = visits_df.ix[visits_df["Year"] == 2017]
    att_df = att_df.ix[att_df["Year"] == 2017]

    # index data
    visits_df = visits_df.groupby(['Month', 'Region', 'Head'])["Visit"].sum()
    att_df = att_df.groupby(['Month', 'Region', 'Head'])["Attendance"].sum()

    # calculate call average
    call_average = visits_df / att_df

    return call_average


def get_pob(pob_df, targets_df):
    # get 2017 data only
    pob_df = pob_df.ix[pob_df["Year"] == 2017]
    targets_df = targets_df.ix[targets_df["Year"] == 2017]

    # get sales
    pob_df = pob_df.groupby(['Month', 'Region', 'Head'])["Pob"].sum()
    targets_df = targets_df.groupby(['Month', 'Region', 'Head'])["Target"].sum()
    pob_percent = (pob_df / targets_df) * 100

    return pob_percent


def new_test_run():
    # read att and visits
    visits_df = get_data("visits")
    att_df = get_data("att")
    pob_df = get_data("orders")
    sales_df = get_data("sales")
    targets_df = get_data("targets")

    # filter for months 4,5,6,7,8,9,10
    visits_df = visits_df.ix[visits_df["Month"].isin([5, 6, 7, 8, 9, 10])]
    att_df = att_df.ix[att_df["Month"].isin([5, 6, 7, 8, 9, 10])]
    pob_df = pob_df.ix[pob_df["Month"].isin([5, 6, 7, 8, 9, 10])]
    sales_df = sales_df.ix[sales_df["Month"].isin([5, 6, 7, 8, 9, 10])]
    targets_df = targets_df.ix[targets_df["Month"].isin([5, 6, 7, 8, 9, 10])]

    # get call average
    call_average = get_call_average(visits_df, att_df)
    call_average = call_average.reset_index()
    call_average['Call Average'] = call_average[0]
    del call_average[0]
    call_average = call_average.set_index(['Month', 'Region', 'Head'])

    # get performance
    performance = get_performance(sales_df, targets_df)
    performance = performance.reset_index()
    performance['Performance'] = performance[0]
    del performance[0]
    performance = performance.set_index(['Month', 'Region', 'Head'])

    # get pob
    pob = get_pob(pob_df, targets_df)
    pob = pob.reset_index()
    pob['Pob'] = pob[0]
    del pob[0]
    pob = pob.set_index(['Month', 'Region', 'Head'])

    # merge all
    output = call_average.join(performance)
    output = output.join(pob)

    # add to csv
    output.to_csv('output/output.csv')

if __name__ == "__main__":
    new_test_run()
