from json import loads
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys


class VenmoBot():
    def __init__(self):
        self.TIMEOUT = 10

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

    def kill_bot(self, exit_code=0):
        self.driver.quit()
        sys.exit(exit_code)

    def login(self, venmo_email: str, venmo_password: str):
        self.driver.get("https://account.venmo.com/settings/security")

        email_input = self.driver.find_element(By.ID, 'email')
        email_input.send_keys(venmo_email)
        email_input.send_keys(Keys.ENTER)

        password_input = self.driver.find_element(By.ID, 'password')
        password_input.send_keys(venmo_password)
        password_input.send_keys(Keys.ENTER)

        try:
            WebDriverWait(self.driver, self.TIMEOUT).until(
                EC.text_to_be_present_in_element(
                    (By.TAG_NAME, "h1"), "Security")
            )
        except:
            self.kill_bot(exit_code=1)
            print(
                'Error occurred while logging in. Check your username and password and try again.')
            sys.exit(1)

    def scrape_transactions(self, start_date: str, end_date: str):
        self.driver.get(
            f'https://account.venmo.com/api/statement/download?startDate={start_date}&endDate={end_date}')
        try:
            json_string = self.driver.find_element(By.TAG_NAME, 'pre').text
            response = loads(json_string)
            transactions = response['data']['transactions']
            return transactions
        except:
            self.kill_bot(exit_code=1)
            print(
                'Error occurred while scraping transactions. Check your start and end dates and try again.')
            sys.exit(1)
