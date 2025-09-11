from web_requests import get_passenger_data
from data_cleaner import filter_data

if __name__ == "__main__":
    get_passenger_data(2024)
    filter_data("raw_data_2024.csv")
