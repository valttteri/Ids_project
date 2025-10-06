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

def plot_weekly_passengers(year):
    rows = get_data(year)

    if rows is None:
        return
    
    header, data = rows[0], rows[1:]
    idx_year = header.index("VUOSI")
    idx_week = header.index("VIIKKO")
    idx_passengers = header.index("NOUSIJAT")
    idx_direction = header.index("SUUNTA")

    weekly_counts = defaultdict(int)

    for row in data:
        try:
            year = int(row[idx_year])
            week = int(row[idx_week])
            passengers = int(row[idx_passengers])
            direction = row[idx_direction]
        except ValueError:
            continue

        if direction not in ("k1", "k2"):
            weekly_counts[week] += passengers


    weeks = sorted(weekly_counts.keys())
    counts = [weekly_counts[w] for w in weeks]

    plt.figure(figsize=(12, 6))
    plt.plot(weeks, counts, marker="o", linewidth=2)
    plt.xticks(range(1, 54))
    plt.xlabel("Week")
    plt.ylabel("Passengers")
    plt.title(f"Years {year} passengers per week")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()

def plot_average_weekly_passengers(years: list, show_individual=True):
    all_weekly_counts = []

    for year in years:
        rows = get_data(year)
        if rows is None:
            continue

        header, data = rows[0], rows[1:]
        idx_week = header.index("VIIKKO")
        idx_passengers = header.index("NOUSIJAT")
        idx_direction = header.index("SUUNTA")

        weekly_counts = defaultdict(int)
        for row in data:
            try:
                week = int(row[idx_week])
                passengers = int(row[idx_passengers])
                direction = row[idx_direction]
            except ValueError:
                continue

            if direction not in ("k1", "k2"):
                weekly_counts[week] += passengers

        all_weekly_counts.append(weekly_counts)

    if not all_weekly_counts:
        print("No data available for the selected years.")
        return

    all_weeks = range(1, 54)
    weekly_sums = defaultdict(list)

    for wc in all_weekly_counts:
        for week in all_weeks:
            weekly_sums[week].append(wc.get(week, 0))

    avg_counts = [np.mean(weekly_sums[w]) for w in all_weeks]

    plt.figure(figsize=(12, 6))

    if show_individual:
        for year, wc in zip(years, all_weekly_counts):
            counts = [wc.get(w, 0) for w in all_weeks]
            plt.plot(all_weeks, counts, linestyle="--", alpha=0.4, label=f"{year}")

    plt.plot(all_weeks, avg_counts, marker="o", linewidth=2, color="black", label="Average")

    plt.xticks(range(1, 54))
    plt.xlabel("Week")
    plt.ylabel("Passengers")
    plt.title(f"Average Weekly Passengers ({min(years)}–{max(years)})")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()
