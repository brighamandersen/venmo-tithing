import re
from datetime import datetime


def calculate_tithing(income: float) -> float:
    TITHING_PERCENTAGE = 0.1
    return income * TITHING_PERCENTAGE


def currency_str_to_float(currency_str: str) -> float:
    return float(currency_str.replace('$', '').replace(',', '').replace(' ', '').replace('+', ''))


def datetime_to_date(datetime_string: str) -> str:
    datetime_obj = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S")
    return datetime_obj.strftime("%Y-%m-%d")


def extract_username_and_time_range(metadata: str) -> str:
    """
    Pulls the username and time range from the metadata string
    Example: "Account Statement - (@username) - December 31st to February 1st 2024" returns ("@username", "December 31st to February 1st 2024")
    """
    pattern = r'\((@\w+)\) - (.*)'  # Match the @string inside the () and everything after ") - "
    match = re.search(pattern, metadata)

    if match:
        username = match.group(1)
        time_range = match.group(2)
        return username, time_range
    return ''


def float_to_currency(amount: float) -> str:
    return f'${amount:.2f}'
