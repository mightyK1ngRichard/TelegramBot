# Copyright © 2022 mightyK1ngRichard <dimapermyakov55@gmail.com>

from telebot import TeleBot, types

TOKEN = '5715759447:AAFCFHQ9M1xLp_KRcKKe2Bqk_XORZXXo5vg'

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        types.KeyboardButton('GitHub'),
        types.InlineKeyboardButton('VK'),
        types.InlineKeyboardButton('VK-memes'),
        types.InlineKeyboardButton('Instagram'),
        types.InlineKeyboardButton('Gmail')
    ]
    markup_reply.add(*buttons)

    bot.send_message(message.chat.id, 'Выберите кнопку:', reply_markup=markup_reply)


@bot.message_handler(content_types=['text'])
def get_text(message):
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
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю! Нажми на кнопку!')


if __name__ == '__main__':
    bot.polling(none_stop=True)
