import logging
import requests, os
import random
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.environ.get('TOKEN'))
weather_token = os.environ.get('WEATHER')
EXCHANGE = os.environ.get('EXCHANGE_API_KEY')
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


class BotStates(StatesGroup):
    weather = State()
    convert_currency = State()

async def on_start(message: types.Message):
    await message.reply("Привет! Выберите функцию:\n"
                        "1. Узнать погоду\n"
                        "2. Конвертировать валюты\n"
                        "3. Получить случайную картинку с милым животным\n"
                        "4. Создать опрос")


@dp.message_handler(commands=['start', 'help'])
async def start_handler(message: types.Message):
    await on_start(message)


@dp.message_handler(lambda message: message.text.strip().lower() == '1', state=None)
async def get_weather(message: types.Message, state: FSMContext):
    await message.reply("Введите название города, чтобы узнать погоду:")
    await BotStates.weather.set()

@dp.message_handler(lambda message: not message.text.startswith('/'), state=BotStates.weather)
async def weather_handler(message: types.Message, state: FSMContext):
    city = message.text.strip()
    try:
        params = {'q': city, 'units': 'metric', 'lang': 'ru', 'appid': weather_token}
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather', params=params)
        if not response:
            raise
        w = response.json()
        weather_res = f"На улице {w['weather'][0]['description']}, {round(w['main']['temp'])} градусов"
    except:
        weather_res = 'Не получилось узнать погоду, попробуйте позже.'
    await bot.send_message(message.from_user.id, weather_res)
    await state.finish()
    await on_start(message)


@dp.message_handler(lambda message: message.text.strip().lower() == '2', state=None)
async def convert_currency(message: types.Message, state: FSMContext):
    await message.reply("Введите сумму, исходную и целевую валюты (например, 100 USD RUB):")
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
            await message.reply("Ошибка при получении данных об обменном курсе. Проверьте правильность введенных данных и попробуйте снова.")

    except Exception as e:
        await message.reply("Ошибка обработки запроса. Убедитесь, что данные в правильном формате: <сумма> <исходная валюта> <целевая валюта>")
    await state.finish()
    await on_start(message)


dp.register_message_handler(get_weather, lambda message: message.text.strip().lower() == '1')
dp.register_message_handler(convert_currency, lambda message: message.text.strip().lower() == '2')


if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
