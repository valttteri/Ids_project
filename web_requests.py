import pandas as pd
import requests
import psycopg2
import csv

def get_passenger_data(year: int):
    # Fetch the Suomenlinna ferry data from the api and write it to a csv file

    with requests.Session() as s:
        headers = {"Authorization": "LWS d59c041a-2ad1-4beb-b769-b9d7ea3a5628"}
        
        # Get passenger data
        passenger_data = s.get(f"https://louhin.hsl.fi/api/1.0/data/257001?filter[VUOSI]={year}", headers=headers)
        passenger_data = passenger_data.content.decode("latin-1")

        # Parse data
        reader = csv.reader(passenger_data.splitlines(), delimiter=";")

        # Save to csv file
        df = pd.DataFrame(reader)
        df.to_csv(f"raw_data_{year}.csv")

        print(df[:10])

def filter_data(path: str):
    df = pd.read_csv(path, header=1, index_col=0)
    year = df.iloc[0]["VUOSI"]

    df = df.drop(df.columns[0], axis=1)

    df = df.drop(columns=[
        "ID",
        "NELJÄNNES",
        "KUUKAUSI",
        "VIIKKO",
        "PÄIVÄ",
        "KUUKAUSIPÄIVÄ",
        "TUNTI",
        "LOMA",
        "HENKILÖAUTOT",
        "PAKETTIAUTOT",
        "KUORMA-AUTOT",
        "REKAT",
        "MUUT",
        "LISÄLIIKENNE",
        "RANNALLE_NOUSIJAT",
        "RANNALLE_AJONEUVOT",
        "RANNALLE_HENKILÖAUTOT",
        "RANNALLE_PAKETTIAUTOT",
        "RANNALLE_KUORMA-AUTOT",
        "RANNALLE_REKAT",
        "RANNALLE_MUUT",
        "LÄMPÖTILA",
        "SADE",
        "TUULI",
        "LÄMPÖTILA_KUUKAUSI",
        "SADE_KUUKAUSI",
        "User",
        "RANNALLE_PYÖRÄT",
        "LISÄTIETOJA"
    ])

    df = df.fillna(-1)

    df.to_csv(f"parsed_data_{year}.csv")

    print(df[:5])


if __name__ == "__main__":
    #get_passenger_data(2024)
    #filter_data("raw_data_2024.csv")
