import telebot
import pyowm
import logging
from telebot import types

bot = telebot.TeleBot('1272174121:AAHIYMKvUX_lSX9c214_WoXxm942US9-CcE')
owm = pyowm.OWM('75e806666123223ccb1d244918864867', language='ru')
city = " "


@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Введите название города")

@bot.message_handler(commands=['today'])
def today(message):
    try:
        observation = owm.weather_at_place(city)
        w = observation.get_weather()
        temp = w.get_temperature('celsius')["temp"]
        answer = "В городе " + city + " сейчас " + w.get_detailed_status() + "\n"
        answer += "Примерная температура: " + str(temp) + " C°"
        bot.send_message(message.chat.id, answer)
    except Exception as woops:
        logging.warning(str(woops))  # will print a message to the console
        answer = "Что-то пошло не так... Проверьте правильность введенных значений."
        bot.send_message(message.chat.id, answer)



@bot.message_handler(content_types=["text"])
def send_message(message):
    global city
    city = message.text.lower()
    bot.send_message(message.chat.id, "Выберите команду", reply_markup=keyboard())



def keyboard():
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	btn1 = types.KeyboardButton('/today')
	markup.add(btn1)
	return markup
bot.polling(none_stop=True)
