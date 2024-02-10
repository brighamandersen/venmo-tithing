from datetime import datetime


def calculate_tithing(income: float) -> float:
    TITHING_PERCENTAGE = 0.1
    return income * TITHING_PERCENTAGE


def currency_str_to_float(currency_str: str) -> float:
    return float(currency_str.replace('$', '').replace(',', '').replace(' ', '').replace('+', ''))


def datetime_to_date(datetime_string: str) -> str:
    datetime_obj = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S")
    return datetime_obj.strftime("%Y-%m-%d")


def float_to_currency(amount: float) -> str:
    return f'${amount:.2f}'


def stringify_income_transaction(income_transaction) -> str:
    return f"{income_transaction['date']}: {float_to_currency(income_transaction['amount'])} from {income_transaction['payer']} for {income_transaction['description']}"
