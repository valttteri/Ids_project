from web_requests import get_passenger_data
from data_cleaner import clean_data

class UserInterface:
    """
    Command line user interface
    """

    def __init__(self, columns):
        self.cols = columns

    def run(self):
        while True:
            cmd = int(input(
                "\nEnter a command:\n1 : Fetch data\n2 : Clean data\n3 : Exit "
            ))

            match cmd:
                case 1:
                    year = input("Enter a year (20xx) or a time frame (20xx-20xx): ")

                    # Time frame
                    if len(year) == 9:
                        start = int(year[:4])
                        end = int(year[5:])
                        
                        if start >= end:
                            print("Invalid timeframe")
                            continue
                        if start not in range(2000, 2026) or end not in range(2000, 2026):
                            print("Start and end must be in range 2000-2025")
                            continue
                        for i in range(start, end+1):
                            get_passenger_data(i)
                    
                    # Single year
                    elif len(year) == 4:
                        if int(year) not in range(2000, 2026):
                            print("Year must be in range 2000-2025")
                            continue
                        get_passenger_data(year)
                    else:
                        print("Invalid input")
                        continue

                case 2:
                    year = input("Enter a year: ")
                    clean_data(f"../raw_data_{year}.csv", self.cols)

                case 3:
                    break



