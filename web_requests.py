import requests
import csv

def get_passenger_data():

    with requests.Session() as s:
        headers = {"Authorization": "LWS d59c041a-2ad1-4beb-b769-b9d7ea3a5628"}
        
        # Get passenger data
        passenger_data = s.get("https://louhin.hsl.fi/api/1.0/data/257001?filter[VUOSI]=2025", headers=headers)
        passenger_data = passenger_data.content.decode("latin-1")

        # Convert data to an array of arrays
        reader = csv.reader(passenger_data.splitlines(), delimiter=";")
        passenger_data = list(reader)

        print(passenger_data)

if __name__ == "__main__":
    get_passenger_data()
