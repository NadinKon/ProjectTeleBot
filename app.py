# from aiogram import types, Dispatcher, Bot
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# from aiogram.utils import executor
# import requests
# from jokes import list_jokes
# from advice import list_advice
# import os
# from dotenv import load_dotenv
# load_dotenv()
#
#
# bot = Bot(token=os.environ.get('TOKEN'))
# weather_token = os.environ.get('WEATHER')
# EXCHANGE = os.environ.get('EXCHANGE_API_KEY')
# dp = Dispatcher(bot)
#
# b1 = KeyboardButton('/Анекдотик')
# b2 = KeyboardButton('/Совет_дня')
# b3 = KeyboardButton('/Сегодня')
# b4 = KeyboardButton('/Погода')
# b5 = KeyboardButton('/Конвертация_валюты')
#
# kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
# kb_client.add(b1, b4).row(b2, b3).row(b5)
#
#
# @dp.message_handler(commands=['start', 'help'])
# async def command_start(message: types.Message):
#     name = message.from_user.first_name
#     await bot.send_message(message.from_user.id, f'Привет {name}! Как я могу помочь?', reply_markup=kb_client)
#     await message.delete()
#
# @dp.message_handler(commands=['Погода'])
# async def weather_command(message: types.Message):
#     await bot.send_message(message.from_user.id, 'Введите город, а я посмотрю какая там погода!')
#
#     @dp.message_handler()
#     async def new_message(message: types.Message):
#         city = message.text.strip()
#         #weather_res = ''
#         try:
#             params = {'q': city, 'units': 'metric', 'lang': 'ru', 'appid': weather_token}
#             response = requests.get(f'https://api.openweathermap.org/data/2.5/weather', params=params)
#             if not response:
#                 raise
#             w = response.json()
#             weather_res = f"На улице {w['weather'][0]['description']}, {round(w['main']['temp'])} градусов"
#         except:
#             weather_res = 'Не получилось узнать погоду, попробуйте позже.'
#         await bot.send_message(message.from_user.id, weather_res)
#         await message.delete()
#
#
# @dp.message_handler(commands=['Анекдотик'])
# async def open_command(message: types.Message):
#     await bot.send_message(message.from_user.id, list_jokes[0])
#     del list_jokes[0]
#
#
# @dp.message_handler(commands=['Совет_дня'])
# async def place_command(message: types.Message):
#     await bot.send_message(message.from_user.id, list_advice[0])
#
#
# @dp.message_handler(commands=['Сегодня'])
# async def menu_command(message: types.Message):
#     await bot.send_message(message.from_user.id, list_advice[1])
#
#
# @dp.message_handler(commands=['Конвертация_валюты'])
# async def convert_currency(message: types.Message):
#     await bot.send_message(message.from_user.id, "Введите сумму, исходную и целевую валюты (например, 100 USD RUB):")
#
#     @dp.message_handler()
#     async def currency_handler(message: types.Message):
#         try:
#             amount, base_currency, target_currency = message.text.strip().split()
#             amount = float(amount)
#             response = requests.get(f'https://v6.exchangerate-api.com/v6/{EXCHANGE}/latest/{base_currency.upper()}').json()
#             if response.get('result') == 'success':
#                 rate = response['conversion_rates'][target_currency.upper()]
#                 converted_amount = round(amount * rate, 2)
#                 await message.reply(f"{amount} {base_currency.upper()} = {converted_amount} {target_currency.upper()}")
#
#             else:
#                 await message.reply("Ошибка при получении данных об обменном курсе. Проверьте правильность введенных данных и попробуйте снова.")
#
#         except Exception as e:
#             await message.reply("Ошибка при обработке запроса. Убедитесь, что вводите данные в правильном формате: <сумма> <исходная валюта> <целевая валюта>")
#
#
# def register_handler_client(dp: Dispatcher):
#     dp.register_message_handler(command_start, commands=['start', 'help'])
#     dp.register_message_handler(open_command, commands=['Анекдотик'])
#     dp.register_message_handler(place_command, commands=['Совет_дня'])
#     dp.register_message_handler(menu_command, commands=['Сегодня'])
#     dp.register_message_handler(weather_command, commands=['Погода'])
#     dp.register_message_handler(weather_command, commands=['Конвертация_валюты'])
#
#
# executor.start_polling(dp)