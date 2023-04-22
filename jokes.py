import requests
from bs4 import BeautifulSoup as bs

url = 'https://www.anekdot.ru/last/good'


# Функция для удаления лишних пробелов и переносов строк
def clean_whitespace(text: str) -> str:
    return ' '.join(text.split())


# Функция для парсинга анекдотов с указанного URL
def parser(url: str):
    try:
        # Отправка запроса на получение HTML-страницы
        r = requests.get(url)

        # Создание объекта BeautifulSoup для анализа HTML
        soup = bs(r.text, 'html.parser')

        # Поиск всех блоков с анекдотами на странице
        anekdots = soup.find_all('div', class_='text')

        # Извлечение текста из блоков и очистка от лишних пробелов и переносов строк
        return [clean_whitespace(c.text) for c in anekdots]
    except Exception as e:
        # Вывод ошибки, если что-то пошло не так
        print(f"Error: {e}")
        return


# Получение списка анекдотов
list_jokes = parser(url)
