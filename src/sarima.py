import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error


def get_data(year):
    """
    Create a dataframe with entries like:

    Month name : Total passengers per month
    """
    path = f"../parsed_data_{year}.csv"


    df = pd.read_csv(path)
    df = df[df["SUUNTA"].isin(["s1", "s2"])][["PÄIVÄMÄÄRÄ", "NOUSIJAT"]]
    df["PÄIVÄMÄÄRÄ"] = pd.to_datetime(df["PÄIVÄMÄÄRÄ"])
    df = df.set_index("PÄIVÄMÄÄRÄ")

    monthly_df = df.resample("ME").sum().reset_index()[:12]

    return monthly_df

def arima_forecast(df):
    # Fit ARIMA model
    
    # ARIMA params: p, d, q
    # p -> Number of lagged observations
    # d -> Order of differencing
    # q -> Order of the moving average

    train_size = int(len(df) * 0.8)
    train, test = df.iloc[:train_size], df.iloc[train_size:]

    model = ARIMA(train["NOUSIJAT"], order=(3,1,3))
    model_fit = model.fit()

    # Forecast
    forecast = model_fit.forecast(steps=len(test))

    print(f"AIC: {model_fit.aic}")
    print(f"BIC: {model_fit.bic}")

    forecast = forecast[:len(test)]
    test_close = test["NOUSIJAT_DIFF"][:len(forecast)]
    # Calculate RMSE
    
    rmse = np.sqrt(mean_squared_error(test_close, forecast))
    print(f"RMSE: {rmse:.4f}")
    
    # Plot the results with specified colors
    
    plt.figure(figsize=(14,7))
    plt.plot(train["PÄIVÄMÄÄRÄ"], train["NOUSIJAT"], label='Train', color='#203147')
    plt.plot(test["PÄIVÄMÄÄRÄ"], test["NOUSIJAT"], label='Test', color='#01ef63')
    plt.plot(test["PÄIVÄMÄÄRÄ"], forecast, label='Forecast', color='orange')
    plt.title('Passenger Forecast')
    plt.xlabel('Date')
    plt.ylabel('Passengers')
    plt.legend()
    plt.show()

def optimal_arima_params(data):
    p = range(0, 4)
    d = range(0, 3)
    q = range(0, 4)
    pdq = list(itertools.product(p, d, q))

    best_aic = np.inf
    best_order = None
    best_model = None

    for order in pdq:
        try:
            model = ARIMA(data, order=order)
            results = model.fit()
            if results.aic < best_aic:
                best_aic = results.aic
                best_order = order
                best_model = results
        except:
            continue

    print(f'Best ARIMA order: {best_order} with AIC: {best_aic}')

def stationary_data_check(df):
    # Check if data is stationary

    result_original = adfuller(df["NOUSIJAT"])
    print(f"ADF Statistic (Original): {result_original[0]:.4f}")
    print(f"p-value (Original): {result_original[1]:.4f}")

    if result_original[1] < 0.05:
        print("Interpretation: The original series is Stationary.\n")
    else:    
        print("Interpretation: The original series is Non-Stationary.\n")

    # Apply first-order differencing
    
    df['NOUSIJAT_DIFF'] = df['NOUSIJAT'].diff()
    
    # Perform the Augmented Dickey-Fuller test on the differenced series
    
    result_diff = adfuller(df["NOUSIJAT_DIFF"].dropna())
    
    print(f"ADF Statistic (Differenced): {result_diff[0]:.4f}")
    print(f"p-value (Differenced): {result_diff[1]:.4f}")
    
    if result_diff[1] < 0.05:       
        print("Interpretation: The differenced series is Stationary.")
    else:   
        print("Interpretation: The differenced series is Non-Stationary.")

def sarima_forecast(df):
    # Forecasting with SARIMA model

    df_now = get_data(2025)

    # Parameters for the forecast
    p, d, q = 3, 1, 3
    P, D, Q, s = 2, 2, 2, 12

    # Fit the model
    model = SARIMAX(df["NOUSIJAT"], order=(p, d, q), seasonal_order=(P, D, Q, s))
    results = model.fit()

    # Forecast periods for monthly data is 12
    forecast_periods = 12
    forecast = results.forecast(steps=forecast_periods)
    
    # Plot the observed data and the forecast
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["NOUSIJAT"], label='Observed')
    plt.plot(forecast.index, forecast, label='Forecast', color='red')
    plt.plot(df_now["PÄIVÄMÄÄRÄ"], df_now["NOUSIJAT"], label='Real 2025', color="green")
    plt.title("Ferry passengers")
    plt.xlabel("Date")
    plt.ylabel("Passengers")

    # Some details for the graph
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.gca().xaxis.set_minor_locator(mdates.MonthLocator(interval=1))  
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y"))   
    plt.xticks(rotation=45) 

    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    dfs = [get_data(year) for year in range(2019, 2025)]
    dfs = pd.concat(dfs)
    dfs["PÄIVÄMÄÄRÄ"] = pd.to_datetime(dfs["PÄIVÄMÄÄRÄ"])
    dfs = dfs.set_index("PÄIVÄMÄÄRÄ")

    sarima_forecast(dfs)


