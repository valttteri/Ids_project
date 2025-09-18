import pandas as pd

def clean_data(path: str, columns: list):
    # Clean the raw data
    try:
        df = pd.read_csv(path, header=1, index_col=0)
    except FileNotFoundError:
        print("Found no raw data from that year")
        return

    print("Cleaning data...")
    year = df.iloc[0]["VUOSI"]

    # Drop unnecessary columns
    df = df.drop(df.columns[0], axis=1)
    df = df.drop(columns=columns)

    # Replace NaN values with -1
    df = df.fillna(-1)

    df.to_csv(f"../parsed_data_{year}.csv")

    print("Data cleaning finished")
