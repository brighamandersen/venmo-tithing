def float_to_currency(amount: float) -> str:
    return f'${amount:.2f}'


def calculate_tithing(income: float) -> float:
    return income * 0.1
