# Copyright © 2022 mightyK1ngRichard <dimapermyakov55@gmail.com>

from telebot import TeleBot, types

TOKEN = '5715759447:AAFCFHQ9M1xLp_KRcKKe2Bqk_XORZXXo5vg'

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


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'VK':
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton('Мой VK')
        markup_reply.add(button)

        bot.send_message(call.message.chat.id, 'Нажми кнопку:', reply_markup=markup_reply)


@bot.message_handler(content_types=['text'])
def get_text(message):
    if message.text == 'Мой VK':
        bot.send_message(message.chat.id, 'https://github.com/mightyK1ngRichard')


if __name__ == '__main__':
    bot.polling(none_stop=True)
