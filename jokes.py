import requests
from bs4 import BeautifulSoup as bs

url = 'https://www.anekdot.ru/last/good'


def parser(url):
    try:
        r = requests.get(url)
        soup = bs(r.text, 'html.parser')
        anekdots = soup.find_all('div', class_='text')
        return [c.text for c in anekdots]
    except:
        return


list_jokes = parser(url)
