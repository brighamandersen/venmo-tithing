from getpass import getpass
from datetime import datetime


def required_input(prompt: str, is_password=False) -> str:
    while True:
        user_input = getpass(prompt) if is_password else input(prompt)
        if user_input:
            return user_input
        else:
            print("Input is required. Try again.")


def float_to_currency(amount: float) -> str:
    return f'${amount:.2f}'


def calculate_tithing(income: float) -> float:
    return income * 0.1


def datetime_str_to_date_str(datetime_string: str) -> str:
    datetime_obj = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S")
    return datetime_obj.strftime("%Y-%m-%d")
