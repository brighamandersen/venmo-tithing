from utils import required_input, get_date_range_str, float_to_currency, process_transactions
from bot import VenmoBot


def main():
    print('\nWelcome to the Venmo tithing calculator!\n')

    # Get inputs
    print("Log in to your Venmo account")
    venmo_email = required_input('Email:\t\t')
    venmo_password = required_input('Password:\t', is_password=True)
    print("\nEnter what range to download (must be 2022 and after)")
    start_date = required_input('Start date (YYYY-MM-DD):\t')
    end_date = required_input('End date (YYYY-MM-DD):\t\t')
    date_range_str = get_date_range_str(start_date, end_date)

    # Login, scrape, and process transactions
    bot = VenmoBot()
    print('\nLogging in to Venmo...\n')
    bot.login(venmo_email, venmo_password)
    print('\nProcessing transactions...\n')
    transactions = bot.scrape_transactions(start_date, end_date)
    payments_to_me, total_income, tithing = process_transactions(transactions)

    # Display results
    print(f'Payments to me {date_range_str}:')
    for payment in payments_to_me:
        print(payment)
    print(f'\nTotals {date_range_str}:')
    print(f'Income:\t\t' + float_to_currency(total_income))
    print(f'Tithing:\t' + float_to_currency(tithing))

    bot.kill_bot()


if __name__ == '__main__':
    main()
