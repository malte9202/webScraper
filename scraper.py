import requests
from bs4 import BeautifulSoup
import smtplib

url = 'https://geizhals.de/samsung-c27f398-lc27f398fwuxen-a1490511.html'

headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 '
                  '(KHTML, like Gecko) Version/13.1.2 Safari/605.1.15'
}

reference_price = 150.00
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')


def get_title() -> str:
    title = soup.select_one('.variant__header__headline').get_text(strip=True)
    return title


def get_price() -> float:
    price = float(soup.select_one(".gh_price").get_text(strip=True)[2:].replace(",", "."))
    return price


def check_price(price: float):
    if price < reference_price:
        send_mail()


def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('email', 'password')
    subject = 'Price fell down!'
    body = 'Check the Geizhals link: https://geizhals.de/samsung-c27f398-lc27f398fwuxen-a1490511.html'
    message = f'Subject: {subject}\n\n{body}'
    server.sendmail(
        'sender',
        'empfänger',
    )
    print('Email has been sent.')
    server.quit()


check_price(149)


