import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import root_mean_squared_error
from sklearn.linear_model import LinearRegression

from regression_columns import columns

def clean_data(path: str, columns: list):
    # Clean the raw data
    try:
        df = pd.read_csv(path, header=1, index_col=0)
    except FileNotFoundError:
        print("Found no raw data from that year")
        return

    # Drop unnecessary columns
    df = df.drop(df.columns[0], axis=1)
    df = df.drop(columns=columns)

    # Replace NaN values with -1
    df = df.fillna(-1)

    return df

def combine_data_by_date(path):
  df = clean_data(path, columns)

  df["PÄIVÄMÄÄRÄ"] = pd.to_datetime(df["PÄIVÄMÄÄRÄ"])

  """ 
  Gets also cumulative passenger count

  df = df.set_index("timestamp")
  df_daily = df.resample("D").sum().reset_index()
  """

  df_daily = df.groupby(df["PÄIVÄMÄÄRÄ"].dt.date)["NOUSIJAT"].sum().reset_index()
  timeseries = pd.Series(df_daily["NOUSIJAT"].to_list(), index=df_daily["PÄIVÄMÄÄRÄ"])
  timeseries.name = "NOUSIJAT"
  return timeseries

def create_lag_features(series, n_lags=3):
    df = pd.DataFrame(series)
    for lag in range(1, n_lags + 1):
        df[f"lag_{lag}"] = df[series.name].shift(lag)
    df.dropna(inplace=True)
    return df

# Create input X and output y pairs for our regressor model
def create_supervised_dataset(series, n_lags, n_forecasts):
  X, y = [], []
  for i in range(n_lags, len(series) - n_forecasts + 1):
    X.append(series[i - n_lags:i].values)
    y.append(series[i:i + n_forecasts].values)
  return np.array(X), np.array(y)

# Combine data from multiple years into a single pandas series
def combine_years(years: tuple):
  paths = [f"../raw_data_{year}.csv" for year in range(years[0], years[1] + 1)]
  s = [combine_data_by_date(path) for path in paths]
  return pd.concat(s)

ts = combine_years((2016, 2023))
lag_features = create_lag_features(ts, n_lags=5)

# Train / Test split
split = int(len(lag_features) * 0.8)
train, test = lag_features.iloc[:split], lag_features.iloc[split:]

X_train, y_train = train.drop(columns=[ts.name]), train[ts.name]
X_test, y_test = test.drop(columns=[ts.name]), test[ts.name]
print(X_test)

"""X, y = create_supervised_dataset(ts, n_lags=5, n_forecasts=3)

# Train/test split
split = int(len(X) * 0.8)
X_train, X_test, y_train, y_test = X[:split], X[split:], y[:split], y[split:]
"""

model = LinearRegression()
model.fit(X_train, y_train)

future_steps = 50

y_pred = model.predict(X_test)

rmse = root_mean_squared_error(y_test, y_pred)
print('RMSE:', rmse)

events = np.array([np.datetime64('2023-03-25'), 
                   np.datetime64('2023-12-24'), 
                   np.datetime64('2023-06-24'), 
                   np.datetime64('2023-02-21'), 
                   np.datetime64('2023-06-17'), 
                   np.datetime64('2023-04-09'), 
                   np.datetime64('2023-05-01'), 
                   np.datetime64('2023-08-24'), 
                   np.datetime64('2023-08-15'), 
                   np.datetime64('2023-12-31'), 
                   np.datetime64('2023-11-04')])
                  

plt.figure(figsize=(20, 10))
plt.plot(y_test.index, y_test, label="Actual")
plt.plot(y_test.index, y_pred, label="Predicted")
for event in events:
    plt.axvline(event, color='red', linestyle='--', linewidth=2) 
plt.legend()
plt.show()
