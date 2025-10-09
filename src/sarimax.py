import itertools
import warnings
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error
from scipy.optimize import OptimizeWarning

warnings.filterwarnings("ignore", category=UserWarning, module="statsmodels")
warnings.filterwarnings("ignore", category=OptimizeWarning)

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

def optimize_sarimax(df, actual):
    # Find optimal parameters for the SARIMAX model

    p = d = q = range(0, 4)
    P = D = Q = range(0, 2)
    s = [12]

    # non-seasonal
    pdq = list(itertools.product(p, d, q))

    # seasonal
    seasonal_pdq = list(itertools.product(P, D, Q, s))

    combinations = [(order, seasonal_order)
                    for order in pdq
                    for seasonal_order in seasonal_pdq]
    methods = ["bfgs", "lbfgs", "powell", "cg"]

    param_results = []
    min_error = 10**6    

    for method in methods:
        for i, (order, seasonal_order) in enumerate(combinations):
            model = SARIMAX(df["NOUSIJAT"], order=order, seasonal_order=seasonal_order)

            try:
                results = model.fit(method=method)
            except Exception as e:
                print(f"Fit failed with method {method} and {order}, {seasonal_order}")
                print(f"\nError: {e}")

            fc = results.forecast(steps=12)
            fc = fc.round().astype(int)

            # Mean absolute error of the forecast
            error = mean_absolute_error(actual["NOUSIJAT"], fc)

            # Ratio of the MAE and the actual mean of the data
            ratio = error / actual["NOUSIJAT"].mean()

            if error < min_error:
                param_results.append(
                    {  
                        "method": method,
                        "ord": order,
                        "seasonal_ord": seasonal_order,
                        "error": error,
                        "ratio": ratio
                    }
                )
                min_error = error

            # Print the status of the optimization
            print(f"{i}/{len(combinations)} with {method}: {order}, {seasonal_order} -> {error}")

    return param_results
    


def sarimax_forecast(df):
    # Forecasting with SARIMA model

    df_now = get_data(2025)

    # Parameters for the forecast
    # Optimal method: bfgs
    # Optimal order: (3, 1, 3)
    # Optimal seasonal order: (1, 1, 0, 12)
    p, d, q = 3, 1, 3
    P, D, Q, s = 1, 1, 0, 12

    # Fit the model
    model = SARIMAX(df["NOUSIJAT"], order=(p, d, q), seasonal_order=(P, D, Q, s))
    results = model.fit(method="bfgs")

    # Forecast periods for monthly data is 12
    forecast_periods = 12
    forecast = results.forecast(steps=forecast_periods)
    
    # Plot the observed data and the forecast
    plt.figure(figsize=(12, 5))
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
    # Data for forecasting
    dfs = [get_data(year) for year in range(2019, 2025)]
    dfs = pd.concat(dfs)

    dfs["PÄIVÄMÄÄRÄ"] = pd.to_datetime(dfs["PÄIVÄMÄÄRÄ"])
    dfs = dfs.set_index("PÄIVÄMÄÄRÄ")
    dfs = dfs.asfreq("ME")

    # Data for optimizing parameters
    dfss = [get_data(year) for year in range(2018, 2024)]
    dfss = pd.concat(dfss)
    dfss["PÄIVÄMÄÄRÄ"] = pd.to_datetime(dfss["PÄIVÄMÄÄRÄ"])
    dfss = dfss.set_index("PÄIVÄMÄÄRÄ")
    dfss = dfss.asfreq("ME")
    df24 = get_data(2024)
    
    #print(optimize_sarimax(dfss, df24))
    sarimax_forecast(dfs)



