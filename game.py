# Copyright © 2022 mightyK1ngRichard <dimapermyakov55@gmail.com>
import telebot
from telebot import types

"""
Проблемы: 
1. Начинать играть одновременно. Не заходить, когда другие уже начали, т.к. не знаю, как такое отслеживать.
2. Отвечать на вопросы все вместе. Т.е не отвечать на второй вопрос, пока другие не ответили на первый.
"""


class Player:
    def __init__(self, user_name: str, user_role: str | None = None, choosing_partner: int | None = None,
                 counter_for_question: int = 0):
        self.name = user_name
        self.role = user_role
        self.choosing_partner = choosing_partner
        self.counter_for_question = counter_for_question


TOKEN = '1933398269:AAESSDXK_KgOXtqJ0Io_zSfVvNw7BIwKikE'

# Список вопросов.
ALL_QUESTIONS = ['Кого бы Вы взяли с собой в плавание?']
COUNTER_OF_QUESTIONS = 0  # Счётчик, сколько вопросов уже спросили.
USERS = {
    0: Player('')
}

bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    USERS[message.chat.id] = Player(message.from_user.first_name)
    text = f'Вы добавлены в игру под именем {message.from_user.first_name}'
    bot.send_message(message.chat.id, text)
    print(len(USERS))
    menu(message=message, text_for_user='Выберите свою роль:')


def menu(message: types.Message, text_for_user: str):
    markup = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton(text='Главный игрок', callback_data='главный'),
        types.InlineKeyboardButton(text='Второстепенный игрок', callback_data='второстепенный')
    ]
    markup.add(*buttons)
    bot.send_message(message.chat.id, text=text_for_user, reply_markup=markup)


# TODO: решить что-то с юзерами. И вопросами.
@bot.callback_query_handler(func=lambda call: True)
def issuing_roles(call: types.CallbackQuery):
    ID_user = call.message.chat.id
    if call.data == 'главный':
        # Создаём кнопки из игроков.
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [types.KeyboardButton(data.name) for user_id_from_dict, data in USERS.items()
                   if user_id_from_dict != ID_user]

        # Если игрок только один, то ждём.
        if len(buttons) == 1:
            msg = bot.send_message(call.message.chat.id,
                                   'Игроков больше нет! Подождите, когда кто-то придёт и повторите попытку!')
            menu(msg, 'Дождитесь игроков и выберите роль!')
            return

        # Проверим, есть ли уже главный игрок.
        for _, data in USERS.items():
            if data.role == 'Главный игрок':
                bot.send_message(call.message.chat.id, 'Главный игрок уже есть!\nВаша роль: второстепенный игрок.')
                markup.add(*buttons)
                msg = bot.send_message(call.message.chat.id,
                                       text=ALL_QUESTIONS[USERS[ID_user].counter_for_question], reply_markup=markup)
                USERS[ID_user].counter_for_question += 1
                USERS[ID_user].role = 'Второстепенный игрок'
                bot.register_next_step_handler(msg, check_users, 'Второстепенный игрок')

        # Если всё хорошо.
        markup.add(*buttons)
        msg = bot.send_message(call.message.chat.id, text=ALL_QUESTIONS[USERS[ID_user].counter_for_question],
                               reply_markup=markup)
        USERS[ID_user].role = 'Главный игрок'
        USERS[ID_user].counter_for_question += 1
        bot.register_next_step_handler(msg, check_users)

    elif call.data == 'второстепенный':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [types.KeyboardButton(data.name) for user_id_from_dict, data in USERS.items()
                   if user_id_from_dict != ID_user]
        markup.add(*buttons)
        msg = bot.send_message(call.message.chat.id, text=ALL_QUESTIONS[USERS[ID_user].counter_for_question],
                               reply_markup=markup)
        USERS[ID_user].counter_for_question += 1
        USERS[ID_user].role = 'Второстепенный игрок'
        bot.register_next_step_handler(msg, check_users, 'Второстепенный игрок')


def check_users(message: types.Message):
    # Найдём индекс выбранного игрока в списке.
    index_user_answer = 0
    answer = message.text
    for player_id_from_dict, data in USERS.items():
        if data.name == answer:
            index_user_answer = player_id_from_dict
            break
    # Задали индекс человека, которого выбрали.
    USERS[message.chat.id].choosing_partner = index_user_answer
    print(USERS[index_user_answer].name)


if __name__ == '__main__':
    bot.polling(none_stop=True)
