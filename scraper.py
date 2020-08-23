import requests
from bs4 import BeautifulSoup

url = 'https://geizhals.de/samsung-c27f398-lc27f398fwuxen-a1490511.html'

headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 '
                  '(KHTML, like Gecko) Version/13.1.2 Safari/605.1.15'
}


def check_price():
    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.select_one(".variant__header__headline").get_text(strip=True)
    price = float(soup.select_one(".gh_price").get_text(strip=True)[2:].replace(",", "."))
    print(title)
    print(price)


check_price()


