import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from collections import defaultdict

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

def get_counts_per_month(header, data):
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

    return months, counts

def get_counts_per_hour(header, data):
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

        if direction not in ("k1", "k2"):
            hourly_counts[hour] += passengers

    hours = range(0, 24)
    counts = [hourly_counts[h] for h in hours]

    return counts
    
def get_counts_per_weekday(header, data):
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

    return counts

def line_diagram_monthly_nousijat():

    rows = get_data(2022)
    if rows is None:
        return

    header, data = rows[0], rows[1:]
    months, counts = get_counts_per_month(header, data)

    rows2 = get_data(2023)
    if rows2 is None:
        return

    header, data = rows2[0], rows2[1:]
    _, counts2 = get_counts_per_month(header, data)

    rows3 = get_data(2024)
    if rows3 is None:
        return

    header, data = rows3[0], rows3[1:]
    _, counts3 = get_counts_per_month(header, data)

    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    plt.figure(figsize=(10, 6))
    plt.plot(months, counts, label=2022)
    plt.plot(months, counts2, label=2023)
    plt.plot(months, counts3, label=2024)
    plt.legend(loc="upper left")
    plt.xticks(range(1, 13), month_names)

    plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
    plt.grid(True, which="major", linestyle="--", linewidth=0.7, alpha=0.7)
    plt.xlabel("Month")
    plt.ylabel("Passengers")

    plt.title("Monthly passengers")
    plt.tight_layout()
    plt.show()

def line_diagram_weekly_nousijat():
    rows = get_data(2022)
    if rows is None:
        return

    header, data = rows[0], rows[1:]
    counts = get_counts_per_weekday(header, data)

    rows2 = get_data(2023)
    if rows2 is None:
        return

    header, data = rows2[0], rows2[1:]
    counts2 = get_counts_per_weekday(header, data)

    rows3 = get_data(2024)
    if rows3 is None:
        return

    header, data = rows3[0], rows3[1:]
    counts3 = get_counts_per_weekday(header, data)

    weekday_labels = ["Mon", "Tues", "Wed", "Thu", "Fri", "Sat", "Sun"]

    plt.figure(figsize=(10, 6))
    plt.plot(weekday_labels, counts, label=2022)
    plt.plot(weekday_labels, counts2, label=2023)
    plt.plot(weekday_labels, counts3, label=2024)
    plt.legend(loc="upper left")

    plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
    plt.grid(True, which="major", linestyle="--", linewidth=0.7, alpha=0.7)
    plt.ylim(190000, 450000)
    plt.xlabel("Day")
    plt.ylabel("Passengers")

    plt.title("Weekly passengers")
    plt.tight_layout()
    plt.show()

def line_diagram_hourly_nousijat():
    rows = get_data(2022)
    if rows is None:
        return

    header, data = rows[0], rows[1:]
    counts = get_counts_per_hour(header, data)

    rows2 = get_data(2023)
    if rows2 is None:
        return

    header, data = rows2[0], rows2[1:]
    counts2 = get_counts_per_hour(header, data)

    rows3 = get_data(2024)
    if rows3 is None:
        return

    header, data = rows3[0], rows3[1:]
    counts3 = get_counts_per_hour(header, data)

    hours = range(0, 24)

    plt.figure(figsize=(10, 6))
    plt.plot(hours, counts, label=2022)
    plt.plot(hours, counts2, label=2023)
    plt.plot(hours, counts3, label=2024)
    plt.legend(loc="upper left")
    plt.xticks(hours)

    plt.grid(True, which="major", linestyle="--", linewidth=0.7, alpha=0.7)
    plt.xlabel("Hour")
    plt.ylabel("Passengers")

    plt.title("Hourly passengers")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    #line_diagram_monthly_nousijat()
    #line_diagram_weekly_nousijat()
    line_diagram_hourly_nousijat()
