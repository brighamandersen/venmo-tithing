from flask import Flask, render_template, request, redirect, url_for
import csv
import os
from utils import calculate_tithing, currency_str_to_float, datetime_to_date, float_to_currency, stringify_income_transaction

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/process-csv', methods=['POST'])
def process_csv():
    # Get FileStorage object from the request
    transaction_history_csv = request.files.get('transactions-csv')

    # Save csv to a temporary location
    tmp_csv = '/tmp/transaction_history.csv'
    transaction_history_csv.save(tmp_csv)

    income_transactions = []

    with open(tmp_csv, 'r') as csv_file:
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

        # Remove the temporary file
        os.remove(tmp_csv)

    # Print each income transaction
    for transaction in income_transactions:
        print(stringify_income_transaction(transaction))

    # Print total income
    total_income = sum(transaction['amount']
                       for transaction in income_transactions)
    total_income_str = float_to_currency(total_income)

    # Print total tithing
    tithing = calculate_tithing(total_income)
    tithing_str = float_to_currency(tithing)

    # return redirect(url_for('index'))
    return render_template('index.html', income_transactions=income_transactions, total_income_str=total_income_str, tithing_str=tithing_str)
