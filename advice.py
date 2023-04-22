import requests
from bs4 import BeautifulSoup as bs
import re

url = 'https://moigoroskop.org/goroskop/'


# Функция для удаления HTML-тегов из текста
def clean_html(text: str) -> str:
    return re.sub('<[^>]*>', '', text)


# Функция для парсинга совета дня с указанного URL
def parser(url: str):
    try:
        # Отправка запроса на получение HTML-страницы
        r = requests.get(url)

        # Создание объекта BeautifulSoup для анализа HTML
        soup = bs(r.text, 'html.parser')

        # Поиск всех абзацев на странице
        paragraphs = soup.find_all("p")

        # Извлечение текста из абзацев и очистка от HTML-тегов
        day = clean_html(str(paragraphs[0]))
        advice = clean_html(str(paragraphs[1]))

        # Возврат списка с результатом
        return [advice, day]

    except Exception as e:
        # Вывод ошибки, если что-то пошло не так
        print(f"Error: {e}")
        return


list_advice = parser(url)
