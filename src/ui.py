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
                    year = input("Enter a year: ")
                    get_passenger_data(year)

                case 2:
                    year = input("Enter a year: ")
                    clean_data(f"../raw_data_{year}.csv", self.cols)

                case 3:
                    break



