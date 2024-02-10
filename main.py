import csv
import os
from utils import calculate_tithing, currency_str_to_float, datetime_to_date, float_to_currency, stringify_income_transaction


# CSV - Calculate tithing


print('\nGrabbing income from CSV and calculating tithing...\n')

transaction_history_csv = '~/Downloads/transaction_history.csv'
transaction_history_csv = os.path.expanduser(transaction_history_csv)

income_transactions = []

with open(transaction_history_csv, 'r') as csv_file:
    reader = csv.reader(csv_file)

    # Skip the first 4 rows of metadata
    for _ in range(4):
        next(reader)

    PAYMENT_DATE_COLUMN_INDEX = 2
    PAYMENT_DESCRIPTION_COLUMN_INDEX = 5
    PAYER_NAME_COLUMN_INDEX = 6
    TOTAL_AMOUNT_COLUMN_INDEX = 8
    for row in reader:
        if row[TOTAL_AMOUNT_COLUMN_INDEX] == '':  # Skip over empty cells
            continue

        transaction_amount = currency_str_to_float(
            row[TOTAL_AMOUNT_COLUMN_INDEX])
        if transaction_amount > 0:  # Only add income
            income_transactions.append({
                'date': datetime_to_date(row[PAYMENT_DATE_COLUMN_INDEX]),
                'description': row[PAYMENT_DESCRIPTION_COLUMN_INDEX],
                'payer': row[PAYER_NAME_COLUMN_INDEX],
                'amount': transaction_amount
            })

total_income = sum(transaction['amount']
                   for transaction in income_transactions)
tithing = calculate_tithing(total_income)

for transaction in income_transactions:
    print(stringify_income_transaction(transaction))

print(f'Total income:', float_to_currency(total_income))
print(f'Total tithing:', float_to_currency(tithing))
