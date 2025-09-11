import pandas as pd

def filter_data(path: str):
    print("Cleaning data...")

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

    print("Data cleaning finished")

    print(df[:5])
