import requests  # for http-requests
from bs4 import BeautifulSoup  # for scraping
import smtplib  # for emails
from settings import username, password
import time
import sqlite3
from datetime import date

connection = sqlite3.connect('prices.db')
cursor = connection.cursor()


def create_table_prices():
    create_table_query = 'CREATE TABLE IF NOT EXISTS prices' \
                         '(date DATE,' \
                         'price REAL);'
    cursor.execute(create_table_query)
    connection.commit()


def insert_price(price: float):
    insert_query = 'INSERT INTO prices VALUES (?, ?);'
    cursor.execute(insert_query, (date.today(), price))
    connection.commit()


url = 'https://geizhals.de/samsung-c27f398-lc27f398fwuxen-a1490511.html'

headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 '
                  '(KHTML, like Gecko) Version/13.1.2 Safari/605.1.15'
}

reference_price = 120.00
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')


def get_title() -> str:
    title = soup.select_one('.variant__header__headline').get_text(strip=True)
    return title


def get_price() -> float:
    price = float(soup.select_one(".gh_price").get_text(strip=True)[2:].replace(",", "."))
    return price


def check_price(title: str, price: float):
    if price < reference_price:
        send_mail(title, price)


def send_mail(title: str, price: float):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    subject = f'Price Alert: {title} {price}'
    body = 'Check the link: https://geizhals.de/samsung-c27f398-lc27f398fwuxen-a1490511.html'
    message = f'Subject: {subject}\n\n{body}'
    server.sendmail(
        username,
        username,
        message
    )
    print('Email has been sent.')
    server.quit()


while True:
    check_price(get_title(), get_price())
    create_table_prices()
    insert_price(get_price())
    time.sleep(86400)
