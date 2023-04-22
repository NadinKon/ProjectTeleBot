import logging
from aiogram import types, Dispatcher, Bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import requests
from aiohttp import ClientSession

from jokes import list_jokes
from advice import list_advice
import os
import random
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()
# Настройка логирования с указанным уровнем логов
logging.basicConfig(level=logging.INFO)
# Загрузка токенов и ID из переменных окружения
bot = Bot(token=os.environ.get('TOKEN'))
weather_token = os.environ.get('WEATHER')
EXCHANGE = os.environ.get('EXCHANGE_API_KEY')
chat_id_group = os.environ.get('GROUP_CHAT_ID')

# Создание диспетчера с использованием хранилища на основе памяти
dp = Dispatcher(bot, storage=MemoryStorage())

# Создание кнопок клавиатуры
b1 = KeyboardButton('/Анекдот')
b2 = KeyboardButton('/Совет_дня')
b3 = KeyboardButton('/Сегодня')
b4 = KeyboardButton('/Погода')
b5 = KeyboardButton('/Конвертация_валюты')
b6 = KeyboardButton('/Картинка')
b7 = KeyboardButton('/Создать_опрос')

# Создание и настройка клавиатуры
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.add(b1, b6).row(b2, b3).row(b4, b5).row(b7)


# Определение состояний бота
class BotStates(StatesGroup):
    weather = State()
    convert_currency = State()


# Обработчик старта и приветствие
@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    name = message.from_user.first_name
    await bot.send_message(message.from_user.id, f'Привет {name}! Как дела? Жми на кнопку в меню ↓ ↓ ↓', reply_markup=kb_client)
    await message.delete()


# Обработчик комманды узнать погоду
@dp.message_handler(commands=['Погода'])
async def weather_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Введите город, а я посмотрю какая там погода!')
    await BotStates.weather.set()

    @dp.message_handler(lambda message: not message.text.startswith('/'), state=BotStates.weather)
    async def new_message(message: types.Message, state: FSMContext):
        city = message.text.strip()
        try:
            params = {'q': city, 'units': 'metric', 'lang': 'ru', 'appid': weather_token}
            response = requests.get(f'https://api.openweathermap.org/data/2.5/weather', params=params)
            if not response:
                raise
            w = response.json()
            weather_res = f"На улице {w['weather'][0]['description']}, {round(w['main']['temp'])} градусов"
        except Exception as e:
            weather_res = 'Не получилось узнать погоду, попробуйте позже.'
        await bot.send_message(message.from_user.id, weather_res)
        await state.finish()


# Обработчик комманды анекдот(выдает 1 анекдот)
@dp.message_handler(commands=['Анекдот'])
async def open_command(message: types.Message):
    await bot.send_message(message.from_user.id, list_jokes[0])
    del list_jokes[0]


# Обработчик комманды совет дня(выдает 1 совет)
@dp.message_handler(commands=['Совет_дня'])
async def place_command(message: types.Message):
    await bot.send_message(message.from_user.id, list_advice[0])


# Обработчик комманды сегодня(выдает информацию о том какой сегодня день)
@dp.message_handler(commands=['Сегодня'])
async def menu_command(message: types.Message):
    await bot.send_message(message.from_user.id, list_advice[1])


# Обработчик комманды конвертация валюты(выдает запрошенную информацию по валюте)
@dp.message_handler(commands=['Конвертация_валюты'])
async def convert_currency(message: types.Message):
    await bot.send_message(message.from_user.id, "Введите сумму, исходную и целевую валюты (например, 100 USD RUB):")
    await BotStates.convert_currency.set()

    @dp.message_handler(lambda message: not message.text.startswith('/'), state=BotStates.convert_currency)
    async def currency_handler(message: types.Message, state: FSMContext):
        try:
            amount, base_currency, target_currency = message.text.strip().split()
            amount = float(amount)
            response = requests.get(f'https://v6.exchangerate-api.com/v6/{EXCHANGE}/latest/{base_currency.upper()}').json()
            if response.get('result') == 'success':
                rate = response['conversion_rates'][target_currency.upper()]
                converted_amount = round(amount * rate, 2)
                await message.reply(f"{amount} {base_currency.upper()} = {converted_amount} {target_currency.upper()}")

            else:
                await message.reply("Ошибка при получении данных. Проверьте правильность введенных данных и попробуйте снова.")

        except Exception as e:
            await message.reply("Убедитесь, что вводите данные в правильном формате: сумма исходная валюта целевая валюта")
        await state.finish()

# Обработчик комманды картинка(выдает 1 картинку с животным)
@dp.message_handler(commands=['Картинка'])
async def send_cute_animal(message: types.Message):
    url = "https://some-random-api.ml/img/{}"
    animals = ["dog", "cat", "panda", "fox", "red_panda", "koala", "bird", "raccoon", "kangaroo"]

    chosen_animal = random.choice(animals)
    async with ClientSession() as session:
        async with session.get(url.format(chosen_animal)) as resp:
            image_data = await resp.json()

    image_url = image_data["link"]
    await bot.send_photo(chat_id=message.chat.id, photo=image_url)

# Обработчик комманды позволяет создать опрос и отправляет в общий чат
@dp.message_handler(commands=["Создать_опрос"])
async def create_poll(message: types.Message):
    args = message.get_args()
    if not args:
        await message.reply("Напишите: /Создать_опрос вопрос;вариант 1; вариант 2;дополнительные варианты")
        return

    try:
        parts = args.split(";")
        if len(parts) < 3:
            raise ValueError(
                "Необходимо указать минимум вопрос и два варианта ответа, разделенных точкой с запятой (;)")

        question = parts[0].strip()
        options = [option.strip() for option in parts[1:]]

        if len(options) < 2 or len(options) > 10:
            raise ValueError("Неверное количество вариантов ответа. Допустимое количество: от 2 до 10.")

        d = await bot.send_poll(chat_id=chat_id_group, question=question, options=options)
        print(d)
    except ValueError as e:
        await message.reply(str(e))
    except Exception as e:
        logging.exception(e)
        await message.reply("Произошла ошибка при создании опроса. Пожалуйста, попробуйте еще раз.")


# Функция регистрации обработчиков
def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(open_command, commands=['Анекдот'])
    dp.register_message_handler(place_command, commands=['Совет_дня'])
    dp.register_message_handler(menu_command, commands=['Сегодня'])
    dp.register_message_handler(weather_command, commands=['Погода'])
    dp.register_message_handler(convert_currency, commands=['Конвертация_валюты'])
    dp.register_message_handler(send_cute_animal, commands=['Картинка'])
    dp.register_message_handler(create_poll, commands=['Создать_опрос'])


# Запуск бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
