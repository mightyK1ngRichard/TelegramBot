# Copyright © 2022 mightyK1ngRichard <dimapermyakov55@gmail.com>

from telebot import TeleBot, types
from random import randint
from helpScripts.tests import TIME_TABLE
from helpScripts.LessonBot import TOKEN
from twentyOne import CARDS
from random import choice

# import os
# from dotenv import load_dotenv

# Доработать.
# TOKEN = str(os.getenv('TOKEN'))
bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    menu(message, f'Привет, *{message.from_user.first_name} {message.from_user.last_name}*!')


@bot.message_handler(content_types=['text'])
def main_text(message: types.Message):
    if message.text == '🎲 Рандомное число':
        msg = bot.send_message(message.chat.id, 'Введите диапозон в формате: 0, 100. Где 0 - начало, 100 конец.')
        bot.register_next_step_handler(msg, get_user_number)

    elif message.text == '⏱ Моё расписание':
        markup = types.InlineKeyboardMarkup()
        buttons = [
            types.InlineKeyboardButton('Числитель', callback_data='числитель'),
            types.InlineKeyboardButton('Знаменатель', callback_data='знаменатель')
        ]
        markup.add(*buttons)
        bot.send_message(message.chat.id, 'Выберите:', reply_markup=markup)

    elif message.text == '🃏𝟸𝟷':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Старт', callback_data='старт'))
        bot.send_message(message.chat.id, 'Начните игру!', reply_markup=markup)

    elif message.text == '📶 Связь со мной':
        social_network(message)

    elif message.text == '📷 Фото':
        photo = open('pictures/time-table.png', 'rb')
        bot.send_photo(message.chat.id, photo)

    elif message.text == '🔙 Назад':
        menu(message, 'Выберите пункт меню:')

    elif message.text == 'Крестики нолики':
        pass

    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю! Нажми на кнопку!')


def twenty_one(message: types.Message, data: tuple):
    user_sum, banker_sum, flag_for_banker = data
    answer = True if message.text == 'Продолжить' else False
    if not answer and not flag_for_banker:
        res_game, user_sum_res, bot_sum = ('❗Вы победили', user_sum, banker_sum) if user_sum > banker_sum else (
            '❗Ничья', user_sum, banker_sum) if user_sum == banker_sum else ('❗Банкир победил', user_sum, banker_sum)
        bot.send_message(message.chat.id,
                         f'{res_game}\nВаш результат: {user_sum_res}\nРезультат банкира: {bot_sum}')
        menu(message, 'Выберите пункт меню.')
        return

    elif answer:
        res = CARDS.pop(CARDS.index(choice(CARDS)))
        user_sum += res.number
        bot.send_message(message.chat.id, f'Выпала карта: {res.name} {res.suit}')

        if user_sum > 21:
            bot.send_message(message.chat.id,
                             f"❗️Вы проиграли!\nСумма игрока: {user_sum}\nСумма банкира: {banker_sum}")
            menu(message, 'Выберите пункт меню.')
            return

        elif user_sum == 21:
            bot.send_message(message.chat.id,
                             f"❗Вы победили!\nСумма игрока: {user_sum}\nСумма банкира: {banker_sum}")
            menu(message, 'Выберите пункт меню.')
            return

    bot.send_message(message.chat.id, f'==> Сумма игрока = {user_sum}')

    # Ход банкира.
    if flag_for_banker:
        res = CARDS.pop(CARDS.index(choice(CARDS)))
        bot.send_message(message.chat.id, f'Выпала карта: {res.name} {res.suit}')
        banker_sum += res.number

    if banker_sum > 21:
        bot.send_message(message.chat.id,
                         f"❗️Банкир проиграл!\nСумма игрока: {user_sum}\nСумма банкира: {banker_sum}")
        menu(message, 'Выберите пункт меню.')
        return

    elif banker_sum == 21:
        bot.send_message(message.chat.id,
                         f"❗️Банкир победил!\nСумма игрока: {user_sum}\nСумма банкира: {banker_sum}")
        menu(message, 'Выберите пункт меню.')
        return

    elif (banker_sum > 15 and answer) or (banker_sum > user_sum and not answer):
        flag_for_banker = False
        bot.send_message(message.chat.id, '> Банкир перестал набирать карты!')
        if not answer and not flag_for_banker:
            res_game, user_sum_res, bot_sum = (
                '❗Игрок победил', user_sum, banker_sum) if user_sum > banker_sum else (
                '❗Ничья', user_sum, banker_sum) if user_sum == banker_sum else (
                '❗Банкир победил', user_sum, banker_sum)
            bot.send_message(message.chat.id,
                             f'{res_game}\nВаш результат: {user_sum_res}\nРезультат банкира: {bot_sum}')
            msg = menu(message, 'Выберите пункт меню.')
            bot.register_next_step_handler(msg, main_text)

    # Переход.
    bot.send_message(message.chat.id, f'==> Сумма банкира = {banker_sum}\n\n{"-" * 30}\n')
    all_data = (user_sum, banker_sum, flag_for_banker)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        types.KeyboardButton('Продолжить'),
        types.KeyboardButton('Стоп'),
    ]
    markup.add(*buttons)
    msg = bot.send_message(message.chat.id, 'Выберите кнопку:', reply_markup=markup)
    bot.register_next_step_handler(msg, game_second_step, all_data)


def game_second_step(message: types.Message, data: tuple):
    user_sum, banker_sum, flag_for_banker = data
    answer = True if message.text == 'Продолжить' else False

    if not answer and not flag_for_banker:
        res_game, user_sum_res, bot_sum = ('❗Вы победили', user_sum, banker_sum) if user_sum > banker_sum else (
            '❗Ничья', user_sum, banker_sum) if user_sum == banker_sum else ('❗Банкир победил', user_sum, banker_sum)
        bot.send_message(message.chat.id,
                         f'{res_game}\nВаш результат: {user_sum_res}\nРезультат банкира: {bot_sum}')
        menu(message, 'Выберите пункт меню.')
        return

    elif answer:
        res = CARDS.pop(CARDS.index(choice(CARDS)))
        user_sum += res.number
        bot.send_message(message.chat.id, f'Выпала карта: {res.name} {res.suit}')

        if user_sum > 21:
            bot.send_message(message.chat.id,
                             f"❗️Вы проиграли!\nСумма игрока: {user_sum}\nСумма банкира: {banker_sum}")
            menu(message, 'Выберите пункт меню.')
            return

        elif user_sum == 21:
            bot.send_message(message.chat.id,
                             f"❗Вы победили!\nСумма игрока: {user_sum}\nСумма банкира: {banker_sum}")
            menu(message, 'Выберите пункт меню.')
            return

    bot.send_message(message.chat.id, f'==> Сумма игрока = {user_sum}')

    # Ход банкира.
    if flag_for_banker:
        res = CARDS.pop(CARDS.index(choice(CARDS)))
        bot.send_message(message.chat.id, f'Выпала карта: {res.name} {res.suit}')
        banker_sum += res.number

    if banker_sum > 21:
        bot.send_message(message.chat.id,
                         f"❗️Банкир проиграл!\nСумма игрока: {user_sum}\nСумма банкира: {banker_sum}")
        menu(message, 'Выберите пункт меню.')
        return

    elif banker_sum == 21:
        bot.send_message(message.chat.id,
                         f"❗️Банкир победил!\nСумма игрока: {user_sum}\nСумма банкира: {banker_sum}")
        menu(message, 'Выберите пункт меню.')
        return

    elif (banker_sum > 15 and answer) or (banker_sum > user_sum and not answer):
        flag_for_banker = False
        bot.send_message(message.chat.id, '> Банкир перестал набирать карты!')
        if not answer and not flag_for_banker:
            res_game, user_sum_res, bot_sum = (
                '❗Игрок победил', user_sum, banker_sum) if user_sum > banker_sum else (
                '❗Ничья', user_sum, banker_sum) if user_sum == banker_sum else (
                '❗Банкир победил', user_sum, banker_sum)
            bot.send_message(message.chat.id,
                             f'{res_game}\nВаш результат: {user_sum_res}\nРезультат банкира: {bot_sum}')
            menu(message, 'Выберите пункт меню.')
            return

    # Переход.
    bot.send_message(message.chat.id, f'==> Сумма банкира = {banker_sum}\n\n{"-" * 30}\n')
    all_data = (user_sum, banker_sum, flag_for_banker)
    markup = types.ReplyKeyboardMarkup()
    buttons = [
        types.KeyboardButton('Продолжить'),
        types.KeyboardButton('Стоп'),
    ]
    markup.add(*buttons)
    msg = bot.send_message(message.chat.id, 'Выберите кнопку:', reply_markup=markup)
    bot.register_next_step_handler(msg, twenty_one, all_data)


@bot.callback_query_handler(func=lambda call: True)
def call_answer(call: types.CallbackQuery):
    if call.data == 'числитель':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        buttons = [
            types.KeyboardButton('Понедельник'),
            types.KeyboardButton('Вторник'),
            types.KeyboardButton('Среда'),
            types.KeyboardButton('Четверг'),
            types.KeyboardButton('Пятница'),
            types.KeyboardButton('Суббота'),
            types.KeyboardButton('Воскресенье')
        ]
        markup.add(*buttons)
        msg = bot.send_message(call.message.chat.id, 'Выберите день недели: ', reply_markup=markup)
        bot.register_next_step_handler(msg, get_time_table_numerator, week_day='числитель')

    elif call.data == 'знаменатель':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        buttons = [
            types.KeyboardButton('Понедельник'),
            types.KeyboardButton('Вторник'),
            types.KeyboardButton('Среда'),
            types.KeyboardButton('Четверг'),
            types.KeyboardButton('Пятница'),
            types.KeyboardButton('Суббота'),
            types.KeyboardButton('Воскресенье')
        ]
        markup.add(*buttons)
        msg = bot.send_message(call.message.chat.id, 'Выберите день недели: ', reply_markup=markup)
        bot.register_next_step_handler(msg, get_time_table_numerator, week_day='знаменатель')

    elif call.data == 'старт':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [
            types.KeyboardButton('Продолжить'),
        ]
        markup.add(*buttons)
        msg = bot.send_message(call.message.chat.id, 'Выберите кнопку!', reply_markup=markup)
        bot.register_next_step_handler(call.message, twenty_one, (0, 0, True))


def get_time_table_numerator(message: types.Message, week_day: str):
    res = '\n'.join(TIME_TABLE[week_day][message.text])
    bot.send_message(message.chat.id, f'Расписание на "{message.text}":\n\n{res}')
    menu(message, 'Выберите пункт:')


def social_network(message: types.Message):
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


def choose_social_network(message: types.Message):
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
        bot.send_message(message.chat.id, 'Я тебя не понимаю! Повторите попытку!')

    menu(message, 'Выберите пункт:')


def get_user_number(message: types.Message):
    start_range, end_range = message.text.split(', ')
    bot.send_message(message.chat.id, f"Ваше число: {str(randint(int(start_range.strip()), int(end_range.strip())))}")
    menu(message, 'Выберите пункт меню.')


def menu(message: types.Message, text: str):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = [
        types.KeyboardButton('🎲 Рандомное число'),
        types.KeyboardButton('⏱ Моё расписание'),
        types.KeyboardButton('📶 Связь со мной'),
        types.KeyboardButton('🃏𝟸𝟷'),
        types.KeyboardButton('📷 Фото')
    ]
    markup.add(*button)
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='markdown')


if __name__ == '__main__':
    bot.polling(none_stop=True)
