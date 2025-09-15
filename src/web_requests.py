import pandas as pd
import requests
import csv

def get_passenger_data(year: int):
    # Fetch the Suomenlinna ferry data from the api and write it to a csv file
    print(f"Fetching data from {year}...")

    with requests.Session() as s:
        headers = {"Authorization": "LWS d59c041a-2ad1-4beb-b769-b9d7ea3a5628"}
        
        # Get passenger data
        passenger_data = s.get(f"https://louhin.hsl.fi/api/1.0/data/257001?filter[VUOSI]={year}", headers=headers)
        passenger_data = passenger_data.content.decode("latin-1")

        # Parse data
        reader = csv.reader(passenger_data.splitlines(), delimiter=";")

        # Save to csv file
        df = pd.DataFrame(reader)
        df.to_csv(f"../raw_data_{year}.csv")

        print("Wrote data to csv file")
