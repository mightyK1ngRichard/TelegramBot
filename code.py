# Copyright © 2022 mightyK1ngRichard <dimapermyakov55@gmail.com>

from telebot import TeleBot, types
from main import TOKEN
from random import randint

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    menu(message, f'Привет, *{message.from_user.first_name} {message.from_user.last_name}*!')


@bot.message_handler(content_types=['text'])
def get_text(message):
    if message.text == '🎲 Рандомное число':
        bot.send_message(message.chat.id, 'Выберите диапазон!\n Введите начало(число): ')
        bot.register_next_step_handler(message, number)
    elif message.text == '📶 Соц.сети':
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
        bot.send_message(message.chat.id, 'Выберите соц.сети:', reply_markup=markup_reply)
    elif message.text == 'GitHub':
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
        menu(message, '🔙 Назад')

    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю! Нажми на кнопку!')


def menu(message, text):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = [
        types.KeyboardButton('🎲 Рандомное число'),
        types.KeyboardButton('📶 Соц.сети'),
        types.KeyboardButton('📷 Фото'),
        types.KeyboardButton('🔙 Назад'),
    ]
    markup.add(*button)
    return bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='markdown')


def number(message):
    number = int(message.text)
    bot.send_message(message.chat.id, f'Ваша число {randint(0, number)}.')


if __name__ == '__main__':
    bot.polling(none_stop=True)
