# Venmo Tithing Calculator 💰

Automatically find out how much tithing you pay from your venmo income in just a few clicks.

https://youtu.be/hZwowByqQ-g
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/hZwowByqQ-g/0.jpg)]([https://www.youtube.com/watch?v=hZwowByqQ-g](https://youtu.be/hZwowByqQ-g))


### Usage

[venmo-tithing.brighambandersen.com](https://venmo-tithing.brighambandersen.com)

### Motivation for Project

I love doing coding projects that actually have real-world application. Even if they're small projects, I love being able to help family, friends, and anyone who is in need of a solution that can be solved via code. My mom approached me one day, saying it was frustrating to figure out how much tithing she owed on her nannying job. She receives her pay via Venmo, and she typically would do things old school where she'd pull up the Venmo app, then manually write down all the times where she made money on a sheet of paper, manually write tally up the totals, then take 10% of that and figure out tithing. When I heard this I really wanted to come up with a solution to keep her from having to do all that grunt work!

### The Ideal Solution

The ideal solution would be to get transaction data from Venmo's API, but after extensive research, the Venmo API is no longer available for public use. This made my job much more difficult. However, I wanted an automatic solution, so then I tried scraping data from Venmo's website using Selenium, but apparently Venmo discourages that because they locked me out of my account for a few days. It was quite tragic because at that point I had fully finished the script to grab all the data and perform all the calculations. If you're interested to see that solution, see the [archive/ folder](archive) (particularly [`main.py`](archive/main.py) and [`bot.py`](archive/bot.py)) file here in this repo to see that code.

### The Workaround Solution

While I was saddened to see that I couldn't achieve a fully automated solution, I wanted to give my mom something she could use, so I went ahead and found the most hassle-free solution. It's a website that has you log into venmo and then download your transactions for the pay period you're interested in, then you just drag and drop the CSV into my website and it does the rest. It will scan the CSV and pull out all the relevant data then perform the calculations. You'll then see a list of your transactions that produced income, the total amount of income you made, and how much tithing to pay! 💰

### Development

1. Get the secret key, then save it in a `.env` in the root of this project.

2. Run flask

   In development

   ```
    python app.py
   ```

   In prod on a server that runs constantly (you can change the port as needed)

   ```
   python3 -m gunicorn -w 1 --bind 0.0.0.0:5002 wsgi:app --daemon
   ```
