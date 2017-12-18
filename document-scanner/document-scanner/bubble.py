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


def get_growth(sales):
    sales_16 = sales.ix[sales["YEAR"] == 2016]
    sales_17 = sales.ix[sales["YEAR"] == 2017]

    sales_16 = sales_16.groupby(['HEAD'])["SALE"].sum()
    sales_17 = sales_17.groupby(['HEAD'])["SALE"].sum()

    growth = ((sales_17 - sales_16) / sales_16) * 100
    return growth


def set_growth(sales):
    sales_16 = sales.ix[sales["YEAR"] == 2016]
    sales_17 = sales.ix[sales["YEAR"] == 2017]

    sales_16 = sales_16.groupby(['HEAD'])["SALE"].sum()
    sales_17 = sales_17.groupby(['HEAD'])["SALE"].sum()

    growth = ((sales_17 - sales_16) / sales_16) * 100
    growth.to_csv('growth.csv')


def get_performance(sales, targets):
    sales_17 = sales.ix[sales["YEAR"] == 2017]
    targets_17 = targets.ix[targets["YEAR"] == 2017]

    sales_17 = sales_17.groupby(['HEAD'])["SALE"].sum()
    targets_17 = targets_17.groupby(['HEAD'])["TARGET"].sum()
    performance = (sales_17 / targets_17) * 100

    return performance


def set_performance(sales, targets):
    sales_17 = sales.ix[sales["YEAR"] == 2017]
    targets_17 = targets.ix[targets["YEAR"] == 2017]

    sales_17 = sales_17.groupby(['HEAD'])["SALE"].sum()
    targets_17 = targets_17.groupby(['HEAD'])["TARGET"].sum()
    performance = (sales_17 / targets_17) * 100

    performance.to_csv('performance.csv')


def get_highest_performance(sales, targets):
    sales = sales.ix[sales["YEAR"] == 2017]
    targets = targets.ix[targets["YEAR"] == 2017]
    del sales['YEAR']
    del targets['YEAR']
    targets = targets.set_index(['MONTH', 'HEAD', 'REGION'])
    sales = sales.set_index(['MONTH', 'HEAD', 'REGION'])
    targets = targets.join(sales)
    targets['COUNT'] = targets['SALE'] >= targets['TARGET']
    targets['COUNT'] = targets['COUNT'] * 1

    targets = targets.groupby(['HEAD'])["COUNT"].sum()

    return targets


def set_highest_performance(sales, targets):
    sales = sales.ix[sales["YEAR"] == 2017]
    targets = targets.ix[targets["YEAR"] == 2017]
    del sales['YEAR']
    del targets['YEAR']
    targets = targets.set_index(['MONTH', 'HEAD', 'REGION'])
    sales = sales.set_index(['MONTH', 'HEAD', 'REGION'])
    targets = targets.join(sales)
    targets['COUNT'] = targets['SALE'] >= targets['TARGET']
    targets['COUNT'] *= 1

    targets = targets.groupby(['HEAD'])["COUNT"].sum()

    targets.to_csv('monthly.csv')


def getpcpm(sales):
    sales = sales.ix[sales["YEAR"] == 2017]
    sales['COUNT'] = 1
    sales = sales.groupby(['HEAD'])['COUNT', 'SALE'].sum()
    sales['SALE'] = sales['SALE'] / sales['COUNT']
    del sales['COUNT']
    sales['SALE'] = sales['SALE'].round(0)
    return sales['SALE']


def new_test_run():
    # Read data
    sales_df = get_data("sales")
    targets_df = get_data("targets")

    # filter for months 4,5,6,7,8,9,10
    sales_df = sales_df.ix[sales_df["MONTH"].isin([5, 6, 7, 8, 9, 10])]
    targets_df = targets_df.ix[targets_df["MONTH"].isin([5, 6, 7, 8, 9, 10])]

    set_growth(sales_df)
    set_performance(sales_df, targets_df)
    set_highest_performance(sales_df, targets_df)


def test_run():
    # Read data
    sales_df = get_data("sales")
    targets_df = get_data("targets")
    sales_df = sales_df.ix[sales_df["HEAD"] != "CUTTACK"]
    targets_df = targets_df.ix[targets_df["HEAD"] != "CUTTACK"]

    # filter for months 4,5,6,7,8,9,10
    sales_df = sales_df.ix[sales_df["MONTH"].isin([5, 6, 7, 8, 9, 10])]
    targets_df = targets_df.ix[targets_df["MONTH"].isin([5, 6, 7, 8, 9, 10])]

    growth = get_growth(sales_df)
    performance = get_performance(sales_df, targets_df)
    performance = performance[:-2]

    # monthly = get_highest_performance(sales_df, targets_df)[:-2]
    monthly = getpcpm(sales_df)

    def onpick3(event):
        ind = event.ind
        print ind
        print 'onpick3 scatter:', ind, np.take(growth, ind), np.take(performance, ind)

    sizes = np.array(monthly) ** 0.5
    ax1 = bubbles_mpl.add_subplot(111)
    ax1.set_xlim(-50, 250)
    ax1.spines['bottom'].set_position('zero')
    ax1.spines['left'].set_position('center')
    ax1.scatter(performance, growth, s=sizes, marker='o', c=sizes)
    bubbles_mpl.canvas.mpl_connect('pick_event', onpick3)
    plt.show()


if __name__ == "__main__":
    new_test_run()
