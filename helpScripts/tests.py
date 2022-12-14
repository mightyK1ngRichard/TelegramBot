# Copyright © 2022 mightyK1ngRichard <dimapermyakov55@gmail.com>
from aiogram import Bot, types, Dispatcher, executor
from asyncio import sleep

# from telebot import types

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
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
ALL_QUESTIONS = ['Кого бы Вы взяли с собой в плавание?', 'Кто самый жёский?']  # Список вопросов.
HOST_GAMER_ID: str = '0'  # ID главного игрока.
USERS = dict()  # Словарь игроков. формат - id : Player
# USERS = {
#     '0': Player('Stas', 'Главный игрок', 1),
#     '1': Player('Helen', 'Второстепенный игрок', 2),
#     '2': Player('Vova', 'Второстепенный игрок', 3),
#     '3': Player('Richard', 'Второстепенный игрок', 1),
# }
WINNERS = 'Победили:\n'


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    USERS[message.chat.id] = Player(message.from_user.first_name)
    text: str = f"Привет, {message.from_user.first_name}\nЭто игра между пользователями! Если вы один," \
                f"кто добавлен в очередь, подождите, когда придёт кто-то ещё и нажмите /start"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton('OK'))
    msg = await message.answer(reply_markup=markup)
    await bot.register_next_step_handler(msg, start_help)


def start_help(message: types.Message):
    if len(USERS) > 1:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton('Старт'))
        msg = await message.answer(
            text='Ну что, народ собран! Вас: {len(USERS)} чел.\nНажмите кнопку старт и следуйте по кнопкам!',
            reply_markup=markup)
        # Если игрок только один, то ждём.
        bot.register_next_step_handler(msg, menu, 'Выберите роль:')

    else:
        await message.answer(text='Вы тут одни. Дождитесь игрока и нажмите /start ещё раз.')


def menu(message: types.Message, text_for_user: str):
    if message.text == 'Старт':
        markup = types.InlineKeyboardMarkup()
        buttons = [
            types.InlineKeyboardButton(text='Главный игрок', callback_data='главный'),
            types.InlineKeyboardButton(text='Второстепенный игрок', callback_data='второстепенный')
        ]
        markup.add(*buttons)
        await message.answer(text=text_for_user, reply_markup=markup)


@dp.callback_query_handler(func=lambda call: True)
async def issuing_roles(call: types.CallbackQuery):
    if call.data == 'главный':
        # Проверим, есть ли уже главный игрок.
        for _, data in USERS.items():
            if data.role == 'Главный игрок':
                # Создаём кнопки из игроков.
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                buttons = [types.KeyboardButton(data.name) for user_id_from_dict, data in USERS.items()
                           if user_id_from_dict != call.message.chat.id]
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
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [types.KeyboardButton(data.name) for user_id_from_dict, data in USERS.items()
                   if user_id_from_dict != call.message.chat.id]
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
        msg = await message.answer(text='Нажмите продолжить', reply_markup=markup)
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
            msg = await message.answer(text='Ваш выбор совпал с выбором главного игрока!\nВы выбываете!',
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

            msg = await message.answer(text=text, reply_markup=markup)
            bot.register_next_step_handler(msg, game_chat)


def game_chat(message: types.Message):
    global WINNERS
    if message.text == 'Продолжить':
        if len(USERS) == 0:
            msg = await message.answer(f'Вопросы закончились! Игра завершена. {WINNERS}',
                                       reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(msg, waiting_for_finish)

        elif USERS[message.chat.id].counter_for_question + 1 > len(ALL_QUESTIONS):
            for id_el, data in USERS.items():
                WINNERS += data.name
                WINNERS += '\n'
            USERS.clear()
            WINNERS = WINNERS[0:-1]
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton('Закончить'))
            msg = await message.answer(text=f'Вопросы закончились! Игра завершена. {WINNERS}',
                                       reply_markup=markup)
            bot.register_next_step_handler(msg, waiting_for_finish)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = [types.KeyboardButton(data.name) for user_id_from_dict, data in USERS.items()
                       if user_id_from_dict != message.chat.id]
            markup.add(*buttons)
            msg = await message.answer(text=ALL_QUESTIONS[USERS[message.chat.id].counter_for_question],
                                       reply_markup=markup)
            # if USERS[message.chat.id].counter_for_question + 1 < len(ALL_QUESTIONS):
            # TODO: Убедиться, что тут можно увеличивать счётчик.
            USERS[message.chat.id].counter_for_question += 1
            bot.register_next_step_handler(msg, check_users)


def waiting_for_finish(message: types.Message):
    if len(USERS) == 0:
        await message.answer(text='Игра закончена! Напишите /start, чтобы сыграть снова!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
