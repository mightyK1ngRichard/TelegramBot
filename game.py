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
ALL_QUESTIONS = ['Кого бы Вы взяли с собой в плавание?', '']
COUNTER_OF_QUESTIONS = 0  # Счётчик, сколько вопросов уже спросили.
HOST_GAMER_ID: int = 0

USERS = dict()

bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    USERS[message.chat.id] = Player(message.from_user.first_name)
    text = f'Вы добавлены в игру под именем {message.from_user.first_name}'
    bot.send_message(message.chat.id, text)
    # -------------- Для тестов.
    print(f'ID ==> {message.chat.id}')
    print(len(USERS))
    # --------------
    if len(USERS) != 1:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Старт'))
        bot.send_message(message.chat.id,
                         f'Ну что, народ собран! Вас: {len(USERS)} чел.\nНажмите кнопку старт и следуйте по кнопкам!',
                         reply_markup=markup)
        # Если игрок только один, то ждём.
        menu(message=message, text_for_user='Выберите свою роль:')


def menu(message: types.Message, text_for_user: str):
    markup = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton(text='Главный игрок', callback_data='главный'),
        types.InlineKeyboardButton(text='Второстепенный игрок', callback_data='второстепенный')
    ]
    markup.add(*buttons)
    bot.send_message(message.chat.id, text=text_for_user, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def issuing_roles(call: types.CallbackQuery):
    # ID_user = call.message.chat.id
    if call.data == 'главный':
        # Создаём кнопки из игроков.
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [types.KeyboardButton(data.name) for user_id_from_dict, data in USERS.items()
                   if user_id_from_dict != call.message.chat.id]

        if len(buttons) == 0:
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
                                       text=ALL_QUESTIONS[USERS[call.message.chat.id].counter_for_question],
                                       reply_markup=markup)
                if USERS[call.message.chat.id].counter_for_question + 1 < len(ALL_QUESTIONS):
                    USERS[call.message.chat.id].counter_for_question += 1
                USERS[call.message.chat.id].role = 'Второстепенный игрок'
                bot.register_next_step_handler(msg, check_users)

        # Если всё хорошо.
        markup.add(*buttons)
        msg = bot.send_message(call.message.chat.id,
                               text=ALL_QUESTIONS[USERS[call.message.chat.id].counter_for_question],
                               reply_markup=markup)
        USERS[call.message.chat.id].role = 'Главный игрок'
        global HOST_GAMER_ID
        HOST_GAMER_ID = call.message.chat.id
        if USERS[call.message.chat.id].counter_for_question + 1 < len(ALL_QUESTIONS):
            USERS[call.message.chat.id].counter_for_question += 1
        bot.register_next_step_handler(msg, check_users)

    elif call.data == 'второстепенный':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [types.KeyboardButton(data.name) for user_id_from_dict, data in USERS.items()
                   if user_id_from_dict != call.message.chat.id]
        markup.add(*buttons)
        msg = bot.send_message(call.message.chat.id,
                               text=ALL_QUESTIONS[USERS[call.message.chat.id].counter_for_question],
                               reply_markup=markup)
        USERS[call.message.chat.id].counter_for_question += 1
        USERS[call.message.chat.id].role = 'Второстепенный игрок'
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

    global HOST_GAMER_ID
    # сверяем.
    if USERS[HOST_GAMER_ID].choosing_partner == USERS[message.chat.id].choosing_partner:
        msg = bot.send_message(message.chat.id, 'Ваш выбор совпал с выбором главного игрока!\nВы выбываете!',
                               reply_markup=types.ReplyKeyboardRemove())
        bot.next_step_backend(msg, start)


if __name__ == '__main__':
    bot.polling(none_stop=True)
