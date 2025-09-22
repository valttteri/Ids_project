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



def line_diagram_monthly_nousijat(year: int):
    rows = get_data(2022)
    if rows is None:
        return

    header, data = rows[0], rows[1:]
    months, counts = get_counts_per_month(header, data)

    rows2 = get_data(2023)
    if rows2 is None:
        return

    header, data = rows2[0], rows2[1:]
    months2, counts2 = get_counts_per_month(header, data)

    rows3 = get_data(2024)
    if rows3 is None:
        return

    header, data = rows3[0], rows3[1:]
    months3, counts3 = get_counts_per_month(header, data)

    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    plt.figure(figsize=(10, 6))
    plt.plot(months, counts, label=2022)
    plt.plot(months2, counts2, label=2023)
    plt.plot(months3, counts3, label=2024)
    plt.legend(loc="upper left")
    plt.xticks(range(1, 13), month_names)

    plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
    plt.grid(True, which="major", linestyle="--", linewidth=0.7, alpha=0.7)
    plt.xlabel("Month")
    plt.ylabel("Passengers")

    plt.title("Monthly passengers")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    line_diagram_monthly_nousijat(2022)
