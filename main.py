# Copyright © 2022 mightyK1ngRichard <dimapermyakov55@gmail.com>
"""
Этот файл чисто как теория. Запускать его не надо.

Документация - https://pypi.org/project/pyTelegramBotAPI/

# message - <class 'telebot.types.Message'>
# https://core.telegram.org/bots/api#message
Прикольная штука:
text_for_user = f'Привет, <b> {message.from_user.first_name} {message.from_user.last_name}</b>'
bot.send_message(message.chat.id, text_for_user, parse_mode='html')
"""

from telebot import TeleBot, types

TOKEN = ''
bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup_inline = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton('Посетить GitHub', url='https://github.com/mightyK1ngRichard'),
        types.InlineKeyboardButton('Посетить VK', callback_data='VK')
    ]
    markup_inline.add(*buttons)

    bot.send_message(message.chat.id, 'GitHub:', reply_markup=markup_inline)


@bot.message_handler(content_types=['photo'])
def get_user_photo(message):
    bot.send_message(message.chat.id, 'Прикольно..')


@bot.message_handler(content_types=['sticker'])
def get_user_sticker(message):
    bot.send_message(message.chat.id, 'Ну типо... Ну прикольно')


@bot.message_handler(commands=['info'])
def go_to_github(message):
    markup_inline = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton('Посетить GitHub', url='https://github.com/mightyK1ngRichard'),
        types.InlineKeyboardButton('Посетить VK', callback_data='VK')
    ]
    markup_inline.add(*buttons)

    bot.send_message(message.chat.id, 'GitHub:', reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'VK':
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton('Мой VK')
        markup_reply.add(button)

        bot.send_message(call.message.chat.id, 'Нажми кнопку:', reply_markup=markup_reply)


@bot.message_handler(commands=[''])
def help_user(message):
    # resize_keyboard - Подстраиваются под размер монитора.
    # row_width - сколько кнопок в ряду.
    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        types.KeyboardButton('Вэб Сайт'),
        types.KeyboardButton('Start')
    ]
    markup_reply.add(*buttons)
    bot.send_message(message.chat.id, 'Выберите кнопку:', reply_markup=markup_reply)


@bot.message_handler(commands=['info'])
def message_user(message):
    if message.text.lower() in ['привет', 'здравствуй', 'hi', 'здарова']:
        bot.send_message(message.chat.id, f'Привет, *{message.from_user.first_name} {message.from_user.last_name}*',
                         parse_mode='markdown')

    elif message.text.lower() in ['фото', 'скинь фото', 'фотка', 'photo']:
        photo = open('screen.png', 'rb')
        bot.send_photo(message.chat.id, photo)

    elif message.text.split().lower() == 'вэб сайт':
        bot.send_message(message.chat.id, 'https://github.com/mightyK1ngRichard')


@bot.message_handler(content_types=['text'])
def get_text(message):
    if message.text == 'Мой VK':
        bot.send_message(message.chat.id, 'https://github.com/mightyK1ngRichard')


if __name__ == '__main__':
    bot.polling(none_stop=True)
