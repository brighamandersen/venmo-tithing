from flask import Flask, flash, get_flashed_messages, render_template, request, redirect, url_for, session
import csv
import os
from utils import calculate_tithing, currency_str_to_float, datetime_to_date, float_to_currency, stringify_income_transaction

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/results', methods=['GET'])
def results():
    income_transactions = session.get('income_transactions')
    total_income_str = session.get('total_income_str')
    tithing_str = session.get('tithing_str')

    return render_template(
        'results.html',
        income_transactions=income_transactions,
        total_income_str=total_income_str,
        tithing_str=tithing_str
    )


@app.route('/process-csv', methods=['POST'])
def process_csv():
    # Get FileStorage object from the request
    uploaded_csv_file = request.files.get('transactions-csv')

    # Save csv to a temporary location
    tmp_csv = '/tmp/transaction_history.csv'
    uploaded_csv_file.save(tmp_csv)

    # Process csv to populate income_transactions
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

    # Make calculations
    total_income = sum(transaction['amount']
                       for transaction in income_transactions)
    tithing = calculate_tithing(total_income)

    # Save data to session to use in index
    session['income_transactions'] = income_transactions
    session['total_income_str'] = float_to_currency(total_income)
    session['tithing_str'] = float_to_currency(tithing)

    return redirect(url_for('results'))


if __name__ == '__main__':
    app.run()
