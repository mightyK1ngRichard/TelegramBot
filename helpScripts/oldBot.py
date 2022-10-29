# Copyright © 2022 mightyK1ngRichard <dimapermyakov55@gmail.com>

import telebot
from telebot import types
import random
import requests
from bs4 import BeautifulSoup
from pyowm import OWM

TOKEN = '1933398269:AAESSDXK_KgOXtqJ0Io_zSfVvNw7BIwKikE'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('🎲 Рандомное число')
    item2 = types.KeyboardButton('🌦 Погода')
    item3 = types.KeyboardButton('📈 Курсы валют')
    item4 = types.KeyboardButton('📚 Информация')
    item5 = types.KeyboardButton('🎮 Game')
    item6 = types.KeyboardButton('📸️ Фото')
    markup.add(item1, item2, item3, item4, item5, item6)
    bot.send_message(message.chat.id, 'Привет, {0.first_name}!'.format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == '🎲 Рандомное число':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('от 0 до 10')
            item2 = types.KeyboardButton('от 0 до 100')
            item3 = types.KeyboardButton('от 0 до 1000')
            back = types.KeyboardButton('⬅️ Назад')
            markup.add(item1, item2, item3, back)
            bot.send_message(message.chat.id, 'Выберите интервал', reply_markup=markup)

        elif message.text == 'от 0 до 10':
            bot.send_message(message.chat.id, 'Ваше число: ' + str(random.randint(0, 10)))

        elif message.text == 'от 0 до 100':
            bot.send_message(message.chat.id, 'Ваше число: ' + str(random.randint(0, 100)))

        elif message.text == 'от 0 до 1000':
            bot.send_message(message.chat.id, 'Ваше число: ' + str(random.randint(0, 1000)))


        elif message.text == '🌦 Погода':
            owm = OWM('d2d5eba60bb37a00ce164aea31b6b7ae')
            place = "Москва"
            mrg = owm.weather_manager()
            observation = mrg.weather_at_place(place)
            w = observation.weather

            t = w.temperature("celsius")
            t1 = t['temp']
            t2 = t['feels_like']
            t3 = t['temp_max']
            t4 = t['temp_min']
            bot.send_message(message.chat.id,
                             f"в городе {place} темпиратура {t1}, ощущается как {t2}, максимальная {t3} и минимальная {t4}")

        elif message.text == '📈 Курсы валют':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('🇺🇸 Курс Доллара')
            item2 = types.KeyboardButton('🇪🇺 Курс Евро')
            back = types.KeyboardButton('⬅️ Назад')
            markup.add(item1, item2, back)
            bot.send_message(message.chat.id, '📈 Курсы валют', reply_markup=markup)


        elif message.text == '🇺🇸 Курс Доллара':
            url = 'https://minfin.com.ua/currency/nbu/'
            a1 = requests.get(url)
            a2 = a1.text
            a3 = BeautifulSoup(a2)
            table = a3.find('table', {'class': 'table-auto'})
            tr = table.find('td', {'class': 'responsive-hide'})
            tr = tr.text
            tr = tr[:8]
            dollar = 'курс доллара' + str(tr) + ' Гривен'
            bot.reply_to(message, dollar)


        elif message.text == '🇪🇺 Курс Евро':
            bot.reply_to(message, '86,72 рубля')


        elif message.text == '📚 Информация':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('💾 О боте')
            item2 = types.KeyboardButton('📦 Что в коробке?')
            back = types.KeyboardButton('⬅️ Назад')
            markup.add(item1, item2, back)
            bot.send_message(message.chat.id, '📚 Информация', reply_markup=markup)

        elif message.text == '💾 О боте':
            bot.reply_to(message, 'Здоров, это бот гениального, но скромного парня.')

        elif message.text == '📦 Что в коробке?':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Математика')
            item2 = types.KeyboardButton('Русский и литература')
            back = types.KeyboardButton('⬅️ Назад')
            markup.add(item1, item2, back)
            bot.send_message(message.chat.id, 'Настал час сделать выбор!', reply_markup=markup)

        elif message.text == 'Математика':
            stick = open('фото/Верно.png', 'rb')
            bot.send_sticker(message.chat.id, stick)

        elif message.text == 'Русский и литература':
            stick = open('фото/Неверно.png', 'rb')
            bot.send_sticker(message.chat.id, stick)

        elif message.text == '📸️ Фото':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            items = [types.KeyboardButton('🔑 Шпора'),
                     types.KeyboardButton('🏎 Стикер меня'),
                     types.KeyboardButton('👨‍🔬 Стикер гения'),
                     types.KeyboardButton('⬅️ Назад')]
            markup.add(*items)
            bot.send_message(message.chat.id, 'Выбирай фотографию! ', reply_markup=markup)

        elif message.text == '⬅️ Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            items = [types.KeyboardButton('🎲 Рандомное число'),
                     types.KeyboardButton('🌦 Погода'),
                     types.KeyboardButton('📈 Курсы валют'),
                     types.KeyboardButton('📚 Информация'),
                     types.KeyboardButton('🎮 Game'),
                     types.KeyboardButton('📸️ Фото')]
            markup.add(*items)
            bot.send_message(message.chat.id, '⬅️ Назад', reply_markup=markup)

        elif message.text == '👨‍🔬 Стикер гения':
            stick = open('фото/илон.jpg', 'rb')
            bot.send_sticker(message.chat.id, stick)

        elif message.text == '🔑 Шпора':
            stick = open('фото/морзе.jpg', 'rb')
            bot.send_photo(message.chat.id, stick)

        elif message.text == '🏎 Стикер меня':
            stick = open('фото/ламба.jpg', 'rb')
            bot.send_sticker(message.chat.id, stick)

        elif message.text == '🎮 Game':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            items = [types.KeyboardButton('Brawl stars'),
                     types.KeyboardButton('PUBG mobile'),
                     types.KeyboardButton('Clash of clans'),
                     types.KeyboardButton('VK'),
                     types.KeyboardButton('⬅️ Назад')]
            markup.add(*items)
            bot.send_message(message.chat.id, '🎮 Game', reply_markup=markup)

        elif message.text == 'PUBG mobile':
            bot.send_message(message.chat.id, 'Welcome to my clan, keep its name: V АТАКЕ')

        elif message.text == 'Clash of clans':
            bot.send_message(message.chat.id, 'Welcome to my clan, keep your hashtag: #YUJ92Y0Q')

        elif message.text == 'VK':
            bot.send_message(message.chat.id, 'Keep my vk: https://vk.com/boss_permyakoovv')

        elif message.text == 'Brawl stars':
            bot.send_message(message.chat.id, 'Welcome to my clan, keep your hashtag: #LCRPU2VL')

        elif message.text.splite().lower() in ['Привет', 'Hi', 'Hello', 'Прив', 'Здр']:
            bot.send_message(message.chat.id, 'Ещё раз привет! Я бот Дмитрия! Чем могу помочь?')

        else:
            bot.reply_to(message, 'Я тебя не понимаю 🤷‍♂')


if __name__ == '__main__':
    bot.polling(none_stop=True)
