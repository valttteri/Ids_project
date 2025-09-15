import requests
import csv
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

API_URL = "https://louhin.hsl.fi/api/1.0/data/257001?filter[VUOSI]=2024"
HEADERS = {"Authorization": "LWS d59c041a-2ad1-4beb-b769-b9d7ea3a5628"}

def get_passenger_data():

    with requests.Session() as s:
        headers = {"Authorization": "LWS d59c041a-2ad1-4beb-b769-b9d7ea3a5628"}
        
        # Get passenger data
        passenger_data = s.get("https://louhin.hsl.fi/api/1.0/data/257001?filter[VUOSI]=2024", headers=headers)
        passenger_data = passenger_data.content.decode("latin-1")

        # Convert data to an array of arrays
        reader = csv.reader(passenger_data.splitlines(), delimiter=";")
        passenger_data = list(reader)

        print(passenger_data[0])

def load_data():
    with requests.Session() as s:
        response = s.get(API_URL, headers=HEADERS)
        response.encoding = "latin-1"
        reader = csv.reader(response.text.splitlines(), delimiter=";")
        rows = list(reader)
    return rows[0], rows[1:]


def plot_monthly_nousijat():
    header, data = load_data()
    idx_year = header.index("VUOSI")
    idx_month = header.index("KUUKAUSI")
    idx_passengers = header.index("NOUSIJAT")
    idx_direction = header.index("SUUNTA")

    monthly_counts = defaultdict(int)
    for row in data:
        try:
            year = int(row[idx_year])
            month = int(row[idx_month])
            passengers = int(row[idx_passengers])
            direction = row[idx_direction]
        except ValueError:
            continue

        if year == 2024 and direction not in ("k1", "k2"):
            monthly_counts[month] += passengers

    months = sorted(monthly_counts.keys())
    counts = [monthly_counts[m] for m in months]

    plt.figure(figsize=(10, 6))
    plt.bar(months, counts)
    plt.xticks(months)
    plt.xlabel("Kuukausi")
    plt.ylabel("Nousijat")
    plt.title(f"Vuoden {year} kuukausittaiset nousijat")
    plt.tight_layout()
    plt.show()

def plot_weekday_nousijat():
    header, data = load_data()
    idx_year = header.index("VUOSI")
    idx_weekday = header.index("PÄIVÄ")
    idx_passengers = header.index("NOUSIJAT")
    idx_direction = header.index("SUUNTA")

    weekday_counts = defaultdict(int)

    for row in data:
        try:
            year = int(row[idx_year])
            weekday = int(row[idx_weekday])
            passengers = int(row[idx_passengers])
            direction = row[idx_direction]
        except ValueError:
            continue

        if year == 2024 and direction not in ("k1", "k2"):
            weekday_counts[weekday] += passengers

    weekdays = range(0, 7)
    counts = [weekday_counts[d] for d in weekdays]
    weekday_labels = ["Ma", "Ti", "Ke", "To", "Pe", "La", "Su"]

    plt.figure(figsize=(10, 6))
    plt.bar(weekday_labels, counts)
    plt.xlabel("Viikonpäivä")
    plt.ylabel("Nousijat")
    plt.title(f"Vuoden {year} nousijat viikonpäivittäin")
    plt.tight_layout()
    plt.show()

def plot_hourly_nousijat():
    header, data = load_data()
    idx_year = header.index("VUOSI")
    idx_hour = header.index("TUNTI")
    idx_passengers = header.index("NOUSIJAT")
    idx_direction = header.index("SUUNTA")

    hourly_counts = defaultdict(int)

    for row in data:
        try:
            year = int(row[idx_year])
            hour = int(row[idx_hour])
            passengers = int(row[idx_passengers])
            direction = row[idx_direction]
        except ValueError:
            continue

        if year == 2024 and direction not in ("k1", "k2"):
            hourly_counts[hour] += passengers

    hours = range(0, 24)
    counts = [hourly_counts[h] for h in hours]

    plt.figure(figsize=(12, 6))
    plt.bar(hours, counts)
    plt.xticks(hours)
    plt.xlabel("Tunti")
    plt.ylabel("Nousijat")
    plt.title(f"Vuoden {year} nousijat tunneittain")
    plt.tight_layout()
    plt.show()

def plot_hourly_nousijat_by_direction():
    header, data = load_data()
    idx_year = header.index("VUOSI")
    idx_hour = header.index("TUNTI")
    idx_direction = header.index("SUUNTA")
    idx_passengers = header.index("NOUSIJAT")

    counts = defaultdict(lambda: defaultdict(int))

    for row in data:
        try:
            year = int(row[idx_year])
            hour = int(row[idx_hour])
            direction = row[idx_direction]
            passengers = int(row[idx_passengers])
        except ValueError:
            continue

        if year == 2024 and direction not in ("k1", "k2"):
            counts[hour][direction] += passengers

    hours = range(0, 24)
    directions = sorted({row[idx_direction] for row in data if row[idx_direction] not in ("k1", "k2")})

    width = 0.8 / len(directions)
    x = np.arange(len(hours))
    plt.figure(figsize=(12, 6))

    for i, direction in enumerate(directions):
        vals = [counts[h][direction] for h in hours]
        plt.bar(x + i*width, vals, width, label=f"Suunta {direction}")

    plt.xticks(x + width*(len(directions)-1)/2, hours)
    plt.xlabel("Tunti")
    plt.ylabel("Nousijat")
    plt.title(f"Vuoden {year} nousijat tunneittain suunnan mukaan")
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    #get_passenger_data()
    #plot_monthly_nousijat()
    #plot_weekday_nousijat()
    #plot_hourly_nousijat()
    plot_hourly_nousijat_by_direction()
