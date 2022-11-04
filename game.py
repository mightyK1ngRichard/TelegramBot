# Copyright © 2022 mightyK1ngRichard <dimapermyakov55@gmail.com>
import telebot
from telebot import types

"""
Проблемы: 
1. Начинать играть одновременно. Не заходить, когда другие уже начали, т.к. не знаю, как такое отслеживать.
2. Отвечать на вопросы все вместе. Т.е не отвечать на второй вопрос, пока другие не ответили на первый.
"""


class Player:
    def __init__(self, user_name: str, user_role: str | None = None, choosing_partner: int = 0,
                 counter_for_question: int = 0):
        self.name = user_name
        self.role = user_role
        self.choosing_partner = choosing_partner
        self.counter_for_question = counter_for_question


TOKEN = '1933398269:AAESSDXK_KgOXtqJ0Io_zSfVvNw7BIwKikE'
bot = telebot.TeleBot(token=TOKEN)
ALL_QUESTIONS = ['Кого бы Вы взяли с собой в плавание?']  # Список вопросов.
COUNTER_OF_QUESTIONS = 0  # Счётчик, сколько вопросов уже спросили.
HOST_GAMER_ID: str  # ID главного игрока.
USERS = dict()  # Словарь игроков. формат - id : Player


# FLAG_START_GAME = False  # Флаг начала игры.


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    USERS[message.chat.id] = Player(message.from_user.first_name)
    # text = f'Вы добавлены в очередь под именем: "{message.from_user.first_name}"'
    # if FLAG_START_GAME:
    #     bot.send_message(message.chat.id, 'Игра уже идёт! Ждите конца!')

    # elif len(USERS) > 1 and not FLAG_START_GAME:
    if len(USERS) > 1:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton('Старт'))
        msg = bot.send_message(message.chat.id,
                               f'Ну что, народ собран! Вас: {len(USERS)} чел.\nНажмите кнопку старт и следуйте по '
                               f'кнопкам!', reply_markup=markup)
        # Если игрок только один, то ждём.
        bot.register_next_step_handler(msg, menu, 'Выберите роль:')


def menu(message: types.Message, text_for_user: str):
    if message.text == 'Старт':
        # global FLAG_START_GAME
        # FLAG_START_GAME = True
        markup = types.InlineKeyboardMarkup()
        buttons = [
            types.InlineKeyboardButton(text='Главный игрок', callback_data='главный'),
            types.InlineKeyboardButton(text='Второстепенный игрок', callback_data='второстепенный')
        ]
        markup.add(*buttons)
        bot.send_message(message.chat.id, text=text_for_user, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def issuing_roles(call: types.CallbackQuery):
    if call.data == 'главный':
        # Создаём кнопки из игроков.
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [types.KeyboardButton(data.name) for user_id_from_dict, data in USERS.items()
                   if user_id_from_dict != call.message.chat.id]

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
        if USERS[call.message.chat.id].counter_for_question + 1 < len(ALL_QUESTIONS):
            USERS[call.message.chat.id].counter_for_question += 1
        USERS[call.message.chat.id].role = 'Второстепенный игрок'
        bot.register_next_step_handler(msg, check_users)


def check_users(message: types.Message):
    if USERS[message.chat.id].role == 'Главный игрок':
        answer = message.text
        index_user_answer: int = 0
        for player_id_from_dict, data in USERS.items():
            if data.name == answer:
                index_user_answer = int(player_id_from_dict)
                break
        USERS[message.chat.id].choosing_partner = index_user_answer
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Продолжить'))
        msg = bot.send_message(message.chat.id, 'Нажмите продолжить', reply_markup=markup)
        bot.register_next_step_handler(msg, game_chat)

    else:
        # Найдём индекс выбранного игрока в списке.
        answer = message.text
        index_user_answer: int = 0
        for player_id_from_dict, data in USERS.items():
            if data.name == answer:
                index_user_answer = int(player_id_from_dict)
                break

        # Задали индекс человека, которого выбрали.
        USERS[message.chat.id].choosing_partner = index_user_answer

        # сверяем.
        if USERS[HOST_GAMER_ID].choosing_partner == USERS[message.chat.id].choosing_partner:
            msg = bot.send_message(message.chat.id, 'Ваш выбор совпал с выбором главного игрока!\nВы выбываете!',
                                   reply_markup=types.ReplyKeyboardRemove())
            del (USERS[message.chat.id])
            bot.register_next_step_handler(msg, waiting_for_finish)
        else:
            text = 'В игре остались:\n'
            for id_el, data in USERS.items():
                text += data.name
                text += '\n'
            text = text[0:-1]
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton('Продолжить'))

            msg = bot.send_message(message.chat.id, text, reply_markup=markup)
            bot.register_next_step_handler(msg, game_chat)


WINNERS = 'Победили:\n'


def game_chat(message: types.Message):
    global WINNERS
    if message.text == 'Продолжить':
        if len(USERS) == 0:
            msg = bot.send_message(message.chat.id, f'Вопросы закончились! Игра завершена. {WINNERS}',
                                   reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(msg, waiting_for_finish)

        elif USERS[message.chat.id].counter_for_question + 1 >= len(ALL_QUESTIONS):
            for id_el, data in USERS.items():
                WINNERS += data.name
                WINNERS += '\n'
            USERS.clear()
            WINNERS = WINNERS[0:-1]
            msg = bot.send_message(message.chat.id, f'Вопросы закончились! Игра завершена. {WINNERS}',
                                   reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(msg, waiting_for_finish)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = [types.KeyboardButton(data.name) for user_id_from_dict, data in USERS.items()
                       if user_id_from_dict != message.chat.id]
            markup.add(*buttons)
            msg = bot.send_message(message.chat.id,
                                   text=ALL_QUESTIONS[USERS[message.chat.id].counter_for_question],
                                   reply_markup=markup)
            if USERS[message.chat.id].counter_for_question + 1 < len(ALL_QUESTIONS):
                USERS[message.chat.id].counter_for_question += 1
            bot.register_next_step_handler(msg, check_users)


def waiting_for_finish(message: types.Message):
    if len(USERS) == 0:
        bot.send_message(message.chat.id, 'Игра закончена! Напишите "/start"')


if __name__ == '__main__':
    bot.polling(none_stop=True)
