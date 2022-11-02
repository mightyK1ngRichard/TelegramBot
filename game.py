# Copyright © 2022 mightyK1ngRichard <dimapermyakov55@gmail.com>
import telebot
from telebot import types

"""
Проблемы: 
1. Начинать играть одновременно. Не заходить, когда другие уже начали, т.к. не знаю, как такое отслеживать.
"""


class Player:
    def __init__(self, id_user: int, user_name: str, user_role: str | None, choosing_partner: int | None):
        self.user_id = id_user
        self.name = user_name
        self.role = user_role
        self.choosing_partner = choosing_partner


TOKEN = '1933398269:AAESSDXK_KgOXtqJ0Io_zSfVvNw7BIwKikE'

ALL_QUESTIONS = ['Кого бы Вы взяли с собой в плавание?']  # Список вопросов.
COUNTER_OF_QUESTIONS = 0  # Счётчик, сколько вопросов уже спросили.
USERS = []  # Список игроков.

bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    USERS.append(Player(message.chat.id, user_name=message.from_user.first_name, user_role=None, choosing_partner=None))
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
    if call.data == 'главный':
        global COUNTER_OF_QUESTIONS
        # Создаём кнопки из игроков.
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [types.KeyboardButton(el.name) for el in USERS]

        # Если игрок только один, то ждём.
        if len(buttons) == 1:
            msg = bot.send_message(call.message.chat.id,
                                   'Игроков больше нет! Подождите, когда кто-то придёт и повторите попытку!')
            menu(msg, 'Дождитесь игроков и выберите роль!')
            return

        # Проверим, есть ли уже главный игрок.
        for player in USERS:
            if player.role == 'Главный игрок':
                bot.send_message(call.message.chat.id, 'Главный игрок уже есть!\nВаша роль: второстепенный игрок.')
                markup.add(*buttons)
                msg = bot.send_message(call.message.chat.id, text=ALL_QUESTIONS[COUNTER_OF_QUESTIONS],
                                       reply_markup=markup)

                # TODO: ПОФИКСИТЬ СЧËТЧИК. Чтоб для каждого свой
                COUNTER_OF_QUESTIONS += 1
                for user in USERS:
                    if user.user_id == call.message.chat.id:
                        user.role = 'Второстепенный игрок'
                        break
                bot.register_next_step_handler(msg, check_users, 'Второстепенный игрок')

        # Если всё хорошо.
        markup.add(*buttons)
        msg = bot.send_message(call.message.chat.id, text=ALL_QUESTIONS[COUNTER_OF_QUESTIONS], reply_markup=markup)
        for player in USERS:
            if player.user_id == call.message.chat.id:
                player.role = 'Главный игрок'
                break
        # TODO: ПОФИКСИТЬ СЧËТЧИК. Чтоб для каждого свой
        COUNTER_OF_QUESTIONS += 1
        bot.register_next_step_handler(msg, check_users)

    elif call.data == 'второстепенный':
        pass


def check_users(message: types.Message):
    # Найдём индекс выбранного игрока в списке.
    index = 0
    answer = message.text
    for player in USERS:
        if player.name == answer:
            index = player.user_id
            break

    for player in USERS:
        if player.user_id == message.chat.id:
            # Задаём индекс партнёра, которого он выбрал.
            player.choosing_partner = index
            break


if __name__ == '__main__':
    bot.polling(none_stop=True)
