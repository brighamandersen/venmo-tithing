import requests
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv
import os
import pandas as pd


def currency_to_float(currency_str):
    return float(currency_str.replace('$', '').replace(',', '').replace(' ', '').replace('+', ''))


def float_to_currency(float_amount):
    return f'${float_amount:.2f}'


def calculate_tithing(income):
    return income * 0.1


print('Welcome to the Venmo tithing calculator!\n')

print("Let's log in to your Venmo account.")
venmo_email = input('Email: ')
venmo_password = input('Password: ')

print("\nNow let's enter what range to download (must be 2022 and after).")
start_date = input('Start date (i.e. 2022-12-25): ')
end_date = input('End data (i.e. 2022-12-25): ')

# Selenium - Download CSV for month

driver = webdriver.Chrome()

# Hit a simple venmo url to get an access token
driver.get("https://account.venmo.com/settings/security")

email_input = driver.find_element(By.ID, 'email')
email_input.send_keys(venmo_email)
email_input.send_keys(Keys.ENTER)

password_input = driver.find_element(By.ID, 'password')
password_input.send_keys(venmo_password)
password_input.send_keys(Keys.ENTER)

sleep(5)  # Wait for login to complete

# Now that you have credentials, grab the csv file you want
driver.get(
    f'https://account.venmo.com/api/statement/download?startDate={start_date}&endDate={end_date}&csv=true&profileId=2806426909016064864&accountType=personal')
sleep(5)  # Wait for download to complete

driver.close()

# CSV - Calculate tithing

print('\nGenerating CSV and calculating tithing...\n')

transaction_history_csv = '~/Downloads/transaction_history.csv'
transaction_history_csv = os.path.expanduser(transaction_history_csv)

income = []

with open(transaction_history_csv, 'r') as csv_file:
    reader = csv.reader(csv_file)

    # Skip the first 4 rows of metadata
    for _ in range(4):
        next(reader)

    TOTAL_AMOUNT_COL = 8
    for row in reader:
        if row[TOTAL_AMOUNT_COL] == '':  # Skip over empty cells
            continue

        transaction_amount = currency_to_float(row[TOTAL_AMOUNT_COL])
        if transaction_amount > 0:  # Only add income
            income.append(transaction_amount)

total_income = sum(income)
tithing = calculate_tithing(total_income)

print(f'Range: {start_date} - {end_date}')
print(f'Total income:', float_to_currency(total_income))
print(f'Total tithing:', float_to_currency(tithing))
