# Copyright © 2022 mightyK1ngRichard <dimapermyakov55@gmail.com>

from telebot import TeleBot, types
from random import randint

# import os
# from dotenv import load_dotenv


# Доработать.
# TOKEN = str(os.getenv('TOKEN'))

TOKEN = '5715759447:AAFCFHQ9M1xLp_KRcKKe2Bqk_XORZXXo5vg'
bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    menu(message, f'Привет, *{message.from_user.first_name} {message.from_user.last_name}*!')


@bot.message_handler(content_types=['text'])
def get_text(message):
    if message.text == '🎲 Рандомное число':
        # bot.send_message(message.chat.id, 'Выберите диапазон!\n Введите начало(число): ')
        # bot.register_next_step_handler(message, number)
        bot.send_message(message.chat.id, str(randint(1, 1000)))

    elif message.text == '📶 Соц.сети':
        social_network(message)

    elif message.text == '📷 Фото':
        photo = open('pictures/time-table.png', 'rb')
        bot.send_photo(message.chat.id, photo)

    elif message.text == '🔙 Назад':
        menu(message, 'Выберите пункт меню:')

    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю! Нажми на кнопку!')


def menu(message, text):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = [
        types.KeyboardButton('🎲 Рандомное число'),
        types.KeyboardButton('📶 Соц.сети'),
        types.KeyboardButton('📷 Фото')
    ]
    markup.add(*button)
    return bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='markdown')


def choose_social_network(message):
    if message.text == 'GitHub':
        bot.send_message(message.chat.id, 'https://github.com/mightyK1ngRichard')

    elif message.text == 'VK':
        bot.send_message(message.chat.id, 'https://vk.com/mightyk1ngrichard')

    elif message.text == 'VK-memes':
        bot.send_message(message.chat.id, 'https://vk.com/iu5memes')

    elif message.text == 'Instagram':
        bot.send_message(message.chat.id, 'https://www.instagram.com/permyakoovv/')

    elif message.text == 'Gmail':
        bot.send_message(message.chat.id, 'dimapermyakov55@gmail.com')

    elif message.text == '🔙 Назад':
        menu(message, 'Выберите пункт:')

    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю! Повторите попытку!')\

    menu(message, 'Выберите пункт:')


def social_network(message):
    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        types.KeyboardButton('GitHub'),
        types.InlineKeyboardButton('VK'),
        types.InlineKeyboardButton('VK-memes'),
        types.InlineKeyboardButton('Instagram'),
        types.InlineKeyboardButton('Gmail'),
        types.InlineKeyboardButton('🔙 Назад'),
    ]
    markup_reply.add(*buttons)
    msg = bot.send_message(message.chat.id, 'Выберите соц.сети:', reply_markup=markup_reply)
    bot.register_next_step_handler(msg, choose_social_network)


if __name__ == '__main__':
    bot.polling(none_stop=True)
