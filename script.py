from json import loads
from time import sleep
import getpass
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils import calculate_tithing, float_to_currency


def main():
    print('\nWelcome to the Venmo tithing calculator!\n')

    print("Log in to your Venmo account")
    venmo_email = input('Email:\t\t')
    venmo_password = getpass.getpass('Password:\t')

    print("\nEnter what range to download (must be 2022 and after)")
    start_date = input('Start date (i.e. 2022-12-25):\t')
    end_date = input('End date (i.e. 2022-12-25):\t')

    print('\nGetting venmo transactions and calculating tithing (expect a 10 second wait)...\n')

    # Selenium - Login to access credentials for API

    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # Hit a simple venmo url to get an access token
    driver.get("https://account.venmo.com/settings/security")
    sleep(2)

    email_input = driver.find_element(By.ID, 'email')
    email_input.send_keys(venmo_email)
    email_input.send_keys(Keys.ENTER)

    password_input = driver.find_element(By.ID, 'password')
    password_input.send_keys(venmo_password)
    password_input.send_keys(Keys.ENTER)

    sleep(5)  # Wait for login to complete

    # Now that you have credentials, get data from the API
    transactions_url = f'https://account.venmo.com/api/statement/download?startDate={start_date}&endDate={end_date}'
    driver.get(transactions_url)
    sleep(2)
    json_string = driver.find_element(By.TAG_NAME, 'pre').text
    response = loads(json_string)

    driver.close()

    # Calculate tithing from json

    transactions = response['data']['transactions']
    income = []

    for transaction in transactions:
        if transaction['balance_increase']:
            income.append(transaction['amount'])

    total_income = sum(income)
    tithing = calculate_tithing(total_income)

    print('Range:\t\t' + f'{start_date} to {end_date}')
    print(f'Income:\t\t' + float_to_currency(total_income))
    print(f'Tithing:\t' + float_to_currency(tithing))


if __name__ == '__main__':
    main()
