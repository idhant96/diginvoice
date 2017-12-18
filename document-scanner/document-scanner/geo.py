"""Bollinger Bands."""

import os
import pandas as pd
import matplotlib.pyplot as plt


def symbol_to_path(symbol, base_dir=""):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbol):
    """Read data (adjusted close) for given symbols from CSV files."""

    df_temp = pd.read_csv(symbol_to_path(symbol), parse_dates=False, na_values=['nan'])

    return df_temp


def plot_data(df, title="POB"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()


def test_run():
    # Read data
    symbol = "pob"
    df = get_data(symbol)
    df = df.ix[(df["PRICE"] > 0)]
    df = df.ix[df["USER"].isin(["AMIT KUMAR", "Ankit Gupta", "KRISHNA NANDAN JHA"])]
    df = df.ix[df["TYPE"] != "Stockist"]
    order_amount = df.groupby(['DATE', "USER"])["PRICE"].sum()
    df = order_amount.unstack()
    print df.index.values
    df.index = pd.to_datetime(df.index)
    df = df.resample('W').sum()
    plot_data(df)


if __name__ == "__main__":
    test_run()


[["ID", "Growth", "Performance", "ID", "Monthly", "Size"],
["Agra", 14.5237494, 117.8918045, "Agra", 5],
["Aligarh", -85.84238332, 21.57258068, "Aligarh", 0],
["Allahabad", 7.636533384, 105.0981989, "Allahabad", 5],
["Ambala", -6.356473209, 86.6794207, "Ambala", 4],
["Amritsar", -12.6143159, 91.5382637, "Amritsar", 3],
["Azamgarh", -40.95190859, 69.66285237, "Azamgarh", 3],
["BHUBANESWAR", 0, 65.27712635, "BHUBANESWAR", 1],
["Balasore", 0, 76.35647536, "Balasore", 2],
["Basti", 0, 0, "Basti", 0],
["Bareilly", -70.69813343, 50.83481956, "Bareilly", 1],
["Bhagalpur", -22.79568001, 69.23591532, "Bhagalpur", 1],
["Bharatpur", -35.6710102, 432.9946451, "Bharatpur", 0],
["Bhatinda", -11.25284638, 77.78249129, "Bhatinda", 3],
["Burdwan", -86.63863499, 54.03200672, "Burdwan", 1],
["CUTTACK", 1574.398452, 54.18321564, "CUTTACK", 1],
["Dehradun", -39.02493876, 74.9176622, "Dehradun", 3],
["Delhi", -48.04439265, 83.87215365, "Delhi", 1],
["Dhanbad", -45.3930028, 66.06309282, "Dhanbad", 1],
["Dharbanga", -16.407861, 76.5713577, "Dharbanga", 1],
["Dibrugarh", -44.83580018, 54.50700238, "Dibrugarh", 1],
["Faizabad", -7.492927234, 94.97481142, "Faizabad", 3],
["Gauhati", -24.31741539, 72.57607244, "Gauhati", 1],
["Gaya", -36.98079192, 64.82502244, "Gaya", 2],
["Ghaziabad", 66.37405641, 128.3245891, "Ghaziabad", 5],
["Ghazipur / Balia", 25.04488365, 109.0369703, "Ghazipur / Balia", 5],
["Gorakhpur -1", 14.20675599, 73.06871453, "Gorakhpur -1", 2],
["Gorakhpur -2", 44.96814649, 200.3744796, "Gorakhpur -2", 4],
["Gurgaon", -25.58861011, 35.74023321, "Gurgaon", 1],
["Haldwani", -67.78867923, 43.73649022, "Haldwani", 0],
["Hisar", 5.778970234, 76.16229792, "Hisar", 3],
["Jaipur", -24.46976457, 53.66129269, "Jaipur", 0],
["Jalandhar", 3.174720733, 79.8382845, "Jalandhar", 4],
["Jammu", -19.74959877, 45.31095373, "Jammu", 1],
["Jamshedpur", -59.0624973, 45.95024013, "Jamshedpur", 1],
["Jhansi", -39.07910501, 75.71857974, "Jhansi", 1],
["Jhunjhunu", 0, 0, "Jhunjhunu", 0],
["Jodhpur", -25.20347524, 45.36856183, "Jodhpur", 2],
["Kanpur - 1", -82.13802347, 26.9531296, "Kanpur - 1", 0],
["Kanpur - 2", -60.89594535, 55.2010735, "Kanpur - 2", 1],
["Karnal", -21.07828022, 80.1916324, "Karnal", 4],
["Kolkata - 1", -67.47656928, 30.59634953, "Kolkata - 1", 3],
["Kolkata - 2", -82.97518378, 130.240628, "Kolkata - 2", 2],
["Kota", -19.58497342, 20.43812145, "Kota", 0],
["Krishnanagar", -90.90873801, 64.14411396, "Krishnanagar", 1],
["Lucknow - 1", 124.1442721, 214.6489418, "Lucknow - 1", 5],
["Lucknow-2", -90.61068795, 3.906959812, "Lucknow-2", 0],
["Ludhiana", 10.18179654, 106.2579104, "Ludhiana", 4],
["Malda", -84.11441512, 61.98591009, "Malda", 3],
["Mandi", -69.47946112, 29.93531938, "Mandi", 0],
["Meerut", -70.67074817, 43.93161736, "Meerut", 1],
["Midnapore", -84.97286734, 60.81206609, "Midnapore", 2],
["Moradabad", -25.57665335, 79.24341693, "Moradabad", 3],
["Motihari", -9.409644074, 79.24860016, "Motihari", 0],
["Muzaffarnagar", 59.15818449, 149.5634522, "Muzaffarnagar", 6],
["Muzaffarpur", -6.372335128, 87.64934485, "Muzaffarpur", 1],
["Nagaon", -21.96805654, 76.48956435, "Nagaon", 2],
["Patiala", -15.92721567, 70.38842638, "Patiala", 2],
["Patna - 1", 37.51634759, 91.51901253, "Patna - 1", 3],
["Patna - 2", 62.56566276, 148.0449052, "Patna - 2", 3],
["Purnea", 5.756280435, 91.87369246, "Purnea", 1],
["Ranchi - 1", -12.24923254, 70.20043063, "Ranchi - 1", 2],
["Ranchi - 2", -56.74710692, 58.71604389, "Ranchi - 2", 0],
["Rohtak", -26.59434069, 70.85698071, "Rohtak", 1],
["Sikar", -49.78590819, 208.752463, "Sikar", 0],
["Silchar", -43.80379688, 58.7217545, "Silchar", 1],
["Siliguri / Coochbehar", -88.65165662, 48.54445952, "Siliguri / Coochbehar", 1],
["Sri Ganganagar", -8.097209461, 139.6512474, "Sri Ganganagar", 1],
["Srinagar", -0.635360053, 97.88847619, "Srinagar", 3],
["Udaipur", -21.45806924, 53.91085577, "Udaipur", 2],
["Varanasi-1", -1.040633182, 98.19835654, "Varanasi-1", 4],
["Varanasi-2", 28.84566743, 135.1801946, "Varanasi-2", 2]]

      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawSeriesChart);

    function drawSeriesChart() {

      var data = google.visualization.arrayToDataTable([["ID", "Growth", "Performance", "Monthly"],
["Agra", 14.5237494, 117.8918045, 5],
["Aligarh", -85.84238332, 21.57258068, 0],
["Allahabad",  7.636533384,  105.0981989,  5],
["Ambala",  -6.356473209,  86.6794207,  4],
["Amritsar",  -12.6143159,  91.5382637,  3],
["Azamgarh",  -40.95190859,  69.66285237,  3],
["BHUBANESWAR", 0, 65.27712635, 1],
["Balasore", 0, 76.35647536, 2],
["Basti", 0, 0, 0],
["Bareilly", -70.69813343, 50.83481956, 1],
["Bhagalpur", -22.79568001, 69.23591532, 1],
["Bharatpur", -35.6710102, 432.9946451, 0],
["Bhatinda", -11.25284638, 77.78249129, 3],
["Burdwan", -86.63863499, 54.03200672, 1],
["CUTTACK", 1574.398452, 54.18321564, 1],
["Dehradun", -39.02493876, 74.9176622, 3],
["Delhi", -48.04439265, 83.87215365, 1],
["Dhanbad", -45.3930028, 66.06309282, 1],
["Dharbanga", -16.407861, 76.5713577, 1],
["Dibrugarh", -44.83580018, 54.50700238, 1],
["Faizabad", -7.492927234, 94.97481142, 3],
["Gauhati", -24.31741539, 72.57607244, 1],
["Gaya", -36.98079192, 64.82502244, 2],
["Ghaziabad", 66.37405641, 128.3245891, 5],
["Ghazipur / Balia", 25.04488365, 109.0369703, 5],
["Gorakhpur -1", 14.20675599, 73.06871453, 2],
["Gorakhpur -2", 44.96814649, 200.3744796, 4],
["Gurgaon", -25.58861011, 35.74023321, 1],
["Haldwani", -67.78867923, 43.73649022, 0],
["Hisar", 5.778970234, 76.16229792, 3],
["Jaipur", -24.46976457, 53.66129269, 0],
["Jalandhar", 3.174720733, 79.8382845, 4],
["Jammu", -19.74959877, 45.31095373, 1],
["Jamshedpur", -59.0624973, 45.95024013, 1],
["Jhansi", -39.07910501, 75.71857974, 1],
["Jhunjhunu", 0, 0, 0],
["Jodhpur", -25.20347524, 45.36856183, 2],
["Kanpur - 1", -82.13802347, 26.9531296, 0],
["Kanpur - 2", -60.89594535, 55.2010735, 1],
["Karnal", -21.07828022, 80.1916324, 4],
["Kolkata - 1", -67.47656928, 30.59634953, 3],
["Kolkata - 2", -82.97518378, 130.240628, 2],
["Kota", -19.58497342, 20.43812145, 0],
["Krishnanagar", -90.90873801, 64.14411396, 1],
["Lucknow - 1", 124.1442721, 214.6489418, 5],
["Lucknow-2", -90.61068795, 3.906959812, 0],
["Ludhiana", 10.18179654, 106.2579104, 4],
["Malda", -84.11441512, 61.98591009, 3],
["Mandi", -69.47946112, 29.93531938, 0],
["Meerut", -70.67074817, 43.93161736, 1],
["Midnapore", -84.97286734, 60.81206609, 2],
["Moradabad", -25.57665335, 79.24341693, 3],
["Motihari", -9.409644074, 79.24860016, 0],
["Muzaffarnagar", 59.15818449, 149.5634522, 6],
["Muzaffarpur", -6.372335128, 87.64934485, 1],
["Nagaon", -21.96805654, 76.48956435, 2],
["Patiala", -15.92721567, 70.38842638, 2],
["Patna - 1", 37.51634759, 91.51901253, 3],
["Patna - 2", 62.56566276, 148.0449052, 3],
["Purnea", 5.756280435, 91.87369246, 1],
["Ranchi - 1", -12.24923254, 70.20043063, 2],
["Ranchi - 2", -56.74710692, 58.71604389, 0],
["Rohtak", -26.59434069, 70.85698071, 1],
["Sikar", -49.78590819, 208.752463, 0],
["Silchar", -43.80379688, 58.7217545, 1],
["Siliguri / Coochbehar", -88.65165662, 48.54445952, 1],
["Sri Ganganagar", -8.097209461, 139.6512474, 1],
["Srinagar", -0.635360053, 97.88847619, 3],
["Udaipur", -21.45806924, 53.91085577, 2],
["Varanasi-1", -1.040633182, 98.19835654, 4],
["Varanasi-2", 28.84566743, 135.1801946, 2]]);

      var options = {
        title: 'Correlation between life expectancy, fertility rate ' +
               'and population of some world countries (2010)',
        hAxis: {title: 'Life Expectancy'},
        vAxis: {title: 'Fertility Rate'},
        bubble: {textStyle: {fontSize: 11}}
      };

      var chart = new google.visualization.BubbleChart(document.getElementById('series_chart_div'));
      chart.draw(data, options);
    }