# Telegram-бот
Этот проект представляет собой пример телеграм-бота, который выполняет различные функции, такие как отправка анекдотов, советов дня, погоды, конвертация валюты, отправка картинок с животными и создание опросов.

## **Установка**
Убедитесь, что у вас установлен Python 3.7 или выше.

Установите зависимости, используя команду:
pip install -r requirements.txt

**Создайте файл .env в корневом каталоге проекта с содержимым:**<br>
TOKEN=your_telegram_bot_token<br>
WEATHER=your_openweathermap_api_key<br>
EXCHANGE_API_KEY=your_exchange_rate_api_key<br>
GROUP_CHAT_ID=your_group_chat_id<br>

Замените your_telegram_bot_token, your_openweathermap_api_key, your_exchange_rate_api_key, и your_group_chat_id на соответствующие значения.

Запустите бота, выполнив команду:<br>
python main.py

## **Использование**

Отправьте одну из следующих команд боту:

/start или /help - для начала работы.<br>

Далее нажимая на кнопки можно получить необходимый результат:<br>
/Анекдот - бот прилшет анекдот.<br>
/Совет_дня - бот пришлет совет дня.<br>
/Сегодня - бот пришлет информацию о текущем дне.<br>
/Погода - бот пришлет погоду в указанном городе.<br>
/Конвертация_валюты - конвертировать сумму из одной валюты в другую.<br>
/Картинка - бот пришлет картинку с животным.<br>
/Создать_опрос - бот создаст опрос и отправить его в групповой чат.<br>
