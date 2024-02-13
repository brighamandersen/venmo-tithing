from flask import Flask, render_template, request, redirect, url_for, session
import csv
import os
from utils import calculate_tithing, currency_str_to_float, datetime_to_date, extract_username_and_time_range, float_to_currency
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/results', methods=['GET'])
def results():
    username = session.get('username')
    time_range = session.get('time_range')
    income_transactions = session.get('income_transactions')
    total_income_str = session.get('total_income_str')
    tithing_str = session.get('tithing_str')

    return render_template(
        'results.html',
        username=username,
        time_range=time_range,
        income_transactions=income_transactions,
        total_income_str=total_income_str,
        tithing_str=tithing_str
    )


@app.route('/process-csv', methods=['POST'])
def process_csv():
    # Get FileStorage object from the request
    uploaded_csv_file = request.files.get('csv-input')

    # Save csv to a temporary location
    tmp_csv = '/tmp/transaction_history.csv'
    uploaded_csv_file.save(tmp_csv)

    # Process csv to populate income_transactions
    income_transactions = []
    total_income = 0
    with open(tmp_csv, 'r') as csv_file:
        reader = csv.reader(csv_file)

        # Grab metadata from first row
        first_row = next(reader)
        first_cell = first_row[0]
        session['csv_metadata'] = first_row[0]
        session['username'], session['time_range'] = extract_username_and_time_range(
            first_cell)
        # Skip over the next 3 rows
        for _ in range(3):
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
                total_income += transaction_amount
                income_transactions.append({
                    'date': datetime_to_date(row[PAYMENT_DATE_COLUMN_INDEX]),
                    'description': row[PAYMENT_DESCRIPTION_COLUMN_INDEX],
                    'payer': row[PAYER_NAME_COLUMN_INDEX],
                    'amount_str': float_to_currency(transaction_amount)
                })

    # Remove the temporary file
    os.remove(tmp_csv)

    # Make tithing calculation
    tithing = calculate_tithing(total_income)

    # Save data to session to use in index
    session['income_transactions'] = income_transactions
    session['total_income_str'] = float_to_currency(total_income)
    session['tithing_str'] = float_to_currency(tithing)

    return redirect(url_for('results'))


if __name__ == '__main__':
    app.run(debug=True)
