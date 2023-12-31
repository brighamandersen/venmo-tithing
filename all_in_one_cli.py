from json import loads
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
from utils import required_input, calculate_tithing, float_to_currency, datetime_str_to_date_str


TIMEOUT = 10


def main():
    print('\nWelcome to the Venmo tithing calculator!\n')

    print("Log in to your Venmo account")
    venmo_email = required_input('Email:\t\t')
    venmo_password = required_input('Password:\t', is_password=True)

    print("\nEnter what range to download (must be 2022 and after)")
    start_date = required_input('Start date (YYYY-MM-DD):\t')
    end_date = required_input('End date (YYYY-MM-DD):\t\t')
    range_str = f'from {start_date} to {end_date}'

    print('\nGetting venmo transactions and calculating tithing (this will take several seconds)...\n')

    # Selenium - Login to access credentials for API

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # Hit a simple venmo url to get an access token
    driver.get("https://account.venmo.com/settings/security")

    email_input = driver.find_element(By.ID, 'email')
    email_input.send_keys(venmo_email)
    email_input.send_keys(Keys.ENTER)

    password_input = driver.find_element(By.ID, 'password')
    password_input.send_keys(venmo_password)
    password_input.send_keys(Keys.ENTER)

    try:
        WebDriverWait(driver, TIMEOUT).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), "Security")
        )
    except:
        driver.quit()
        print(
            'Error occurred while logging in. Check your username and password and try again.')
        sys.exit(1)

    # Now that you have credentials, get transactions from the API
    transactions = []
    driver.get(
        f'https://account.venmo.com/api/statement/download?startDate={start_date}&endDate={end_date}')
    try:
        json_string = driver.find_element(By.TAG_NAME, 'pre').text
        response = loads(json_string)
        transactions = response['data']['transactions']
    except:
        driver.quit()
        print(
            'Error occurred while scraping transactions. Check your start and end dates and try again.')
        sys.exit(1)

    driver.quit()

    # Calculate tithing from json

    income = []

    print(f'Payments to me {range_str}:')

    for transaction in transactions:
        is_income = transaction['balance_increase']
        if is_income:
            transaction_date = datetime_str_to_date_str(
                transaction["payment"]["date_created"])
            transaction_amount = transaction['amount']
            transaction_actor_name = transaction["payment"]["actor"]["display_name"]
            transaction_note = transaction['note']

            print(
                f'{transaction_date}: {float_to_currency(transaction_amount)} from {transaction_actor_name} for {transaction_note}')
            income.append(transaction_amount)

    total_income = sum(income)
    tithing = calculate_tithing(total_income)

    print(f'\nTotals {range_str}:')
    print(f'Income:\t\t' + float_to_currency(total_income))
    print(f'Tithing:\t' + float_to_currency(tithing))


if __name__ == '__main__':
    main()
