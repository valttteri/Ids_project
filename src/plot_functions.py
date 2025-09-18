import csv
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

def plot_monthly_nousijat(year: int):
    try:
        with open(f"../parsed_data_{year}.csv", newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            rows = list(reader)
    except FileNotFoundError:
        print(f"Found no parsed data from {year}")
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
