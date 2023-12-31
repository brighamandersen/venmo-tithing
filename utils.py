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


def get_date_range_str(start_date: str, end_date: str) -> str:
    return f'from {start_date} to {end_date}'


def process_transactions(transactions: list) -> tuple:
    payments_to_me: list[str] = []
    total_income = 0.0

    for transaction in transactions:
        is_income = transaction['balance_increase']
        if is_income:
            transaction_date = datetime_str_to_date_str(
                transaction["payment"]["date_created"])
            transaction_amount = transaction['amount']
            transaction_actor_name = transaction["payment"]["actor"]["display_name"]
            transaction_note = transaction['note']

            payments_to_me.append(
                f'{transaction_date}: {float_to_currency(transaction_amount)} from {transaction_actor_name} for {transaction_note}')
            total_income += transaction_amount

    tithing = calculate_tithing(total_income)

    return payments_to_me, total_income, tithing
