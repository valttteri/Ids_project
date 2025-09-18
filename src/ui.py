import glob
from web_requests import get_passenger_data
from data_cleaner import clean_data
from plot_functions import (
    plot_monthly_nousijat,
    plot_weekday_nousijat,
    plot_hourly_nousijat,
    plot_hourly_nousijat_by_direction
)

class UserInterface:
    """
    Command line user interface
    """

    def __init__(self, columns):
        self.cols = columns
        self.raw_years = glob.glob("../raw_data_*.csv")
        self.parsed_years = glob.glob("../parsed_data_*.csv")

    def print_raw_years(self):
        # Print a list of years for which raw data is available
        print("\nFound raw data from years")
        for year in self.raw_years:
            print(year[-8:-4])

    def print_parsed_years(self):
        # Print a list of years for which parsed data is available
        print("\nFound parsed data from years")
        for year in self.parsed_years:
            print(year[-8:-4])

    def run(self):
        while True:
            cmd = int(input(
                "\nEnter a command:\n"
                "1 : Fetch data\n"
                "2 : Clean data\n"
                "3 : Plot monthly passengers\n"
                "4 : Plot weekly passengers\n"
                "5 : Plot hourly passengers\n"
                "6 : Plot hourly passengers by direction\n"
                "7 : Quit\n"
            ))

            match cmd:
                case 1:
                    start = int(input("Enter a starting year (20xx): "))
                    end = input("Enter an ending year (20xx) or press enter: ")
                    end = start if len(end) == 0 else int(end)

                    if self.validate_year_input(start, end):
                        for i in range(start, end+1):
                            get_passenger_data(i)
                    self.raw_years = glob.glob("../raw_data_*.csv")

                case 2:
                    self.print_raw_years()
                    year = input("Enter a year: ")
                    clean_data(f"../raw_data_{year}.csv", self.cols)
                    self.parsed_years = glob.glob("../parsed_data_*.csv")


                case 3:
                    self.print_parsed_years()
                    year = int(input("Enter a year: "))
                    plot_monthly_nousijat(year)

                case 4:
                    self.print_parsed_years()
                    year = int(input("Enter a year: "))
                    plot_weekday_nousijat(year)

                case 5:
                    self.print_parsed_years()
                    year = int(input("Enter a year: "))
                    plot_hourly_nousijat(year)

                case 6:
                    self.print_parsed_years()
                    year = int(input("Enter a year: "))
                    plot_hourly_nousijat_by_direction(year)

                case 7:
                    break

    def validate_year_input(self, start: int, end: str):
        # Validate the year input given by user on case 1
        if start > end:
            print("Invalid timeframe")
            return False
        if start not in range(2000, 2026) or end not in range(2000, 2026):
            print("Start and end must be in range 2000-2025")
            return False
        return True 


