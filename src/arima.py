import itertools
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error, mean_absolute_error

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
