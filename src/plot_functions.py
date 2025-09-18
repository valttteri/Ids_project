import csv
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

def get_data(year: int):
    # Read a csv file and return its contents
    try:
        with open(f"../parsed_data_{year}.csv", newline='', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            rows = list(reader)
    except FileNotFoundError:
        print(f"Found no parsed data from {year}")
        return None
    
    return rows 

def plot_monthly_nousijat(year: int):
    rows = get_data(year)
    if rows is None:
        return

    header, data = rows[0], rows[1:]
    idx_month = header.index("KUUKAUSI")
    idx_passengers = header.index("NOUSIJAT")
    idx_direction = header.index("SUUNTA")

    monthly_counts = defaultdict(int)
    for row in data:
        try:
            month = int(row[idx_month])
            passengers = int(row[idx_passengers])
            direction = row[idx_direction]
        except ValueError:
            continue

        if direction not in ("k1", "k2"):
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

def plot_weekday_nousijat(year: int):
    rows = get_data(year)
    if rows is None:
        return

    header, data = rows[0], rows[1:]
    idx_weekday = header.index("PÄIVÄ")
    idx_passengers = header.index("NOUSIJAT")
    idx_direction = header.index("SUUNTA")

    weekday_counts = defaultdict(int)

    for row in data:
        try:
            weekday = int(row[idx_weekday])
            passengers = int(row[idx_passengers])
            direction = row[idx_direction]
        except ValueError:
            continue

        if direction not in ("k1", "k2"):
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

def plot_hourly_nousijat(year: int):
    rows = get_data(year)
    if rows is None:
        return

    header, data = rows[0], rows[1:]
    idx_hour = header.index("TUNTI")
    idx_passengers = header.index("NOUSIJAT")
    idx_direction = header.index("SUUNTA")

    hourly_counts = defaultdict(int)

    for row in data:
        try:
            hour = int(row[idx_hour])
            passengers = int(row[idx_passengers])
            direction = row[idx_direction]
        except ValueError:
            continue

        if direction not in ("k1", "k2"):
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

def plot_hourly_nousijat_by_direction(year: int):
    rows = get_data(year)
    if rows is None:
        return

    header, data = rows[0], rows[1:]
    idx_hour = header.index("TUNTI")
    idx_direction = header.index("SUUNTA")
    idx_passengers = header.index("NOUSIJAT")

    counts = defaultdict(lambda: defaultdict(int))

    for row in data:
        try:
            hour = int(row[idx_hour])
            direction = row[idx_direction]
            passengers = int(row[idx_passengers])
        except ValueError:
            continue

        if direction not in ("k1", "k2"):
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
