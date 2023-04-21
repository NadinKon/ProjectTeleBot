import requests
from bs4 import BeautifulSoup as bs
import re

url = 'https://moigoroskop.org/goroskop/'


def parser(url):
    try:
        r = requests.get(url)
        soup = bs(r.text, 'html.parser')
        g = soup.find_all("p")
        day = re.sub('<[^>]*>', '', str(g[0]))
        advice = re.sub('<[^>]*>', '', str(g[1]))
        return [advice, day]
    except:
        return


list_advice = parser(url)
