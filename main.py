# Copyright © 2022 mightyK1ngRichard <dimapermyakov55@gmail.com>

from telebot import TeleBot, types
from random import randint
from random import choice
from helpScripts.SwitchFilesHere import CARDS, TIME_TABLE, TOKEN

bot = TeleBot(TOKEN)
CARDS_LIST = list()


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    text = f"""
    Привет, *{message.from_user.first_name} {message.from_user.last_name if message.from_user.last_name is not None else ''}*! 
    Я бета версия одного чувачка, и вот что я умею:
    1. Могу помочь с расписанием ИУ5-33Б. (В будущем расширюсь)
    2. Могу дать контакты админа.
    3. Могу сыграть с тобой в 21 очко.
    4. Могу отправить фотографию расписания. (Доработаюсь)
    5. Могу выдать случайное число из заданного диапазона.

    Будьте осторожны, я мог не учесть некоторые "малость неумные" действия пользователя, приводящим к исключениям.
    Если Вам удалось сделать такое "умное" действие, что даже я не учёл его возможность, напишите админу.

    *А так наслаждайтесь проигрышами банкиру!*
"""
    menu(message, text)


@bot.message_handler(content_types=['text'])
def main_text(message: types.Message):
    if message.text == '🎲 Рандомное число':
        msg = bot.send_message(message.chat.id, 'Введите диапозон в формате: 0, 100.\nГде 0 - начало, 100 конец.',
                               reply_markup=types.ReplyKeyboardRemove(selective=True))
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
        return

    elif message.text == 'Крестики нолики':
        pass

    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю! Нажми на кнопку!')


def twenty_one(message: types.Message, data: tuple):
    if message.text in ['Продолжить', 'Стоп']:
        user_sum, banker_sum, flag_for_banker = data
        text = """"""
        answer = True if message.text == 'Продолжить' else False

        if not answer and not flag_for_banker:
            res_game, user_sum_res, bot_sum = ('❗Вы победили', user_sum, banker_sum) if user_sum > banker_sum else (
                '❗Ничья', user_sum, banker_sum) if user_sum == banker_sum else ('❗Банкир победил', user_sum, banker_sum)
            bot.send_message(message.chat.id,
                             text + f'{res_game}\nВаш результат: {user_sum_res}\nРезультат банкира: {bot_sum}')
            menu(message, 'Выберите пункт меню.')
            return

        elif answer:
            res = CARDS_LIST.pop(CARDS_LIST.index(choice(CARDS_LIST)))
            user_sum += res.number
            # bot.send_message(message.chat.id, f'Выпала карта: {res.name} {res.suit}')
            text += f'Выпала карта: {res.name} {res.suit}\n'
            if user_sum > 21:
                bot.send_message(message.chat.id,
                                 text + f"❗️Вы проиграли!\nСумма игрока: {user_sum}\nСумма банкира: {banker_sum}")
                menu(message, 'Выберите пункт меню.')
                return

            elif user_sum == 21:
                bot.send_message(message.chat.id,
                                 text + f"❗Вы победили!\nСумма игрока: {user_sum}\nСумма банкира: {banker_sum}")
                menu(message, 'Выберите пункт меню.')
                return

        text += f'==> Сумма игрока = {user_sum}\n'
        # Ход банкира.
        if flag_for_banker:
            res = CARDS_LIST.pop(CARDS_LIST.index(choice(CARDS_LIST)))
            text += f'Выпала карта: {res.name} {res.suit}\n'
            banker_sum += res.number

        if banker_sum > 21:
            bot.send_message(message.chat.id,
                             text + f"❗️Банкир проиграл!\nСумма игрока: {user_sum}\nСумма банкира: {banker_sum}")
            menu(message, 'Выберите пункт меню.')
            return

        elif banker_sum == 21:
            bot.send_message(message.chat.id,
                             text + f"❗️Банкир победил!\nСумма игрока: {user_sum}\nСумма банкира: {banker_sum}")
            menu(message, 'Выберите пункт меню.')
            return

        text += f'==> Сумма банкира = {banker_sum}\n'
        if flag_for_banker:
            if (banker_sum > 17 and answer) or (banker_sum > user_sum and not answer):
                flag_for_banker = False
                text += '> С этого момента Банкир перестаёт набирать карты!\n'
                if not answer:
                    res_game, user_sum_res, bot_sum = (
                        '❗Игрок победил', user_sum, banker_sum) if user_sum > banker_sum else (
                        '❗Ничья', user_sum, banker_sum) if user_sum == banker_sum else (
                        '❗Банкир победил', user_sum, banker_sum)
                    bot.send_message(message.chat.id,
                                     text + f'{res_game}\nВаш результат: {user_sum_res}\nРезультат банкира: {bot_sum}')
                    menu(message, 'Выберите пункт меню.')
                    return

        # Переход.
        bot.send_message(message.chat.id, text)
        all_data = (user_sum, banker_sum, flag_for_banker)
        if answer:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = [
                types.KeyboardButton('Продолжить'),
                types.KeyboardButton('Стоп'),
            ]
            markup.add(*buttons)
            msg = bot.send_message(message.chat.id, 'Выберите кнопку:', reply_markup=markup)
            bot.register_next_step_handler(msg, game_second_step, all_data)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = [
                types.KeyboardButton('Стоп')
            ]
            markup.add(*buttons)
            msg = bot.send_message(message.chat.id, 'Выберите кнопку:', reply_markup=markup)
            bot.register_next_step_handler(msg, game_second_step, all_data)

    else:
        bot.send_message(message.chat.id,
                         'НУ ТЫ ДЕБИЛ? Ну вот для кого я кнопки делал?!\nХорошо, что я умный и предугадал то, '
                         'что ты дебил!')
        bot.send_video(message.chat.id,
                       'https://tenor.com/view/понасенков-переиграл-уничтожил-ponasenkov-gif-20047373')
        menu(message, 'Выберите пункт меню, дурачок: ')
        return


def game_second_step(message: types.Message, data: tuple):
    if message.text in ['Продолжить', 'Стоп']:
        user_sum, banker_sum, flag_for_banker = data
        answer = True if message.text == 'Продолжить' else False

        text = """"""
        if not answer and not flag_for_banker:
            res_game, user_sum_res, bot_sum = ('❗Вы победили', user_sum, banker_sum) if user_sum > banker_sum else (
                '❗Ничья', user_sum, banker_sum) if user_sum == banker_sum else ('❗Банкир победил', user_sum, banker_sum)
            bot.send_message(message.chat.id,
                             text + f'{res_game}\nВаш результат: {user_sum_res}\nРезультат банкира: {bot_sum}')
            menu(message, 'Выберите пункт меню.')
            return

        elif answer:
            res = CARDS_LIST.pop(CARDS_LIST.index(choice(CARDS_LIST)))
            user_sum += res.number
            text += f'Выпала карта: {res.name} {res.suit}\n'
            if user_sum > 21:
                bot.send_message(message.chat.id,
                                 text + f"❗️Вы проиграли!\nСумма игрока: {user_sum}\nСумма банкира: {banker_sum}")
                menu(message, 'Выберите пункт меню.')
                return

            elif user_sum == 21:
                bot.send_message(message.chat.id,
                                 text + f"❗Вы победили!\nСумма игрока: {user_sum}\nСумма банкира: {banker_sum}")
                menu(message, 'Выберите пункт меню.')
                return

        text += f'==> Сумма игрока = {user_sum}\n'
        # Ход банкира.
        if flag_for_banker:
            res = CARDS_LIST.pop(CARDS_LIST.index(choice(CARDS_LIST)))
            text += f'Выпала карта: {res.name} {res.suit}\n'
            banker_sum += res.number

        if banker_sum > 21:
            bot.send_message(message.chat.id,
                             text + f"❗️Банкир проиграл!\nСумма игрока: {user_sum}\nСумма банкира: {banker_sum}")
            menu(message, 'Выберите пункт меню.')
            return

        elif banker_sum == 21:
            bot.send_message(message.chat.id,
                             text + f"❗️Банкир победил!\nСумма игрока: {user_sum}\nСумма банкира: {banker_sum}")
            menu(message, 'Выберите пункт меню.')
            return

        text += f'==> Сумма банкира = {banker_sum}\n'

        if flag_for_banker:
            if (banker_sum > 17 and answer) or (banker_sum > user_sum and not answer):
                flag_for_banker = False
                text += '> С этого момента Банкир перестаёт набирать карты!\n'
                if not answer:
                    res_game, user_sum_res, bot_sum = (
                        '❗Игрок победил', user_sum, banker_sum) if user_sum > banker_sum else (
                        '❗Ничья', user_sum, banker_sum) if user_sum == banker_sum else (
                        '❗Банкир победил', user_sum, banker_sum)
                    bot.send_message(message.chat.id,
                                     text + f'{res_game}\nВаш результат: {user_sum_res}\nРезультат банкира: {bot_sum}')
                    menu(message, 'Выберите пункт меню.')
                    return

        # Переход.
        bot.send_message(message.chat.id, text)
        all_data = (user_sum, banker_sum, flag_for_banker)
        if answer:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = [
                types.KeyboardButton('Продолжить'),
                types.KeyboardButton('Стоп'),
            ]
            markup.add(*buttons)
            msg = bot.send_message(message.chat.id, 'Выберите кнопку:', reply_markup=markup)
            bot.register_next_step_handler(msg, twenty_one, all_data)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = [
                types.KeyboardButton('Стоп')
            ]
            markup.add(*buttons)
            msg = bot.send_message(message.chat.id, 'Выберите кнопку:', reply_markup=markup)
            bot.register_next_step_handler(msg, twenty_one, all_data)

    else:
        bot.send_message(message.chat.id,
                         'НУ ТЫ ДЕБИЛ? Ну вот для кого я кнопки делал?!\nХорошо, что я умный и предугадал то, '
                         'что ты дебил!')
        bot.send_video(message.chat.id,
                       'https://tenor.com/view/понасенков-переиграл-уничтожил-ponasenkov-gif-20047373')
        menu(message, 'Выберите пункт меню, дурачок: ')
        return


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
        bot.register_next_step_handler(msg, get_time_table, week_day='числитель')

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
        bot.register_next_step_handler(msg, get_time_table, week_day='знаменатель')

    elif call.data == 'старт':
        global CARDS_LIST
        CARDS_LIST = CARDS[:]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [
            types.KeyboardButton('Продолжить'),
        ]
        markup.add(*buttons)
        msg = bot.send_message(call.message.chat.id, 'Выберите кнопку!', reply_markup=markup)
        bot.register_next_step_handler(msg, twenty_one, (0, 0, True))


def get_time_table(message: types.Message, week_day: str):
    if message.text in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']:
        res = '\n'.join(TIME_TABLE[week_day][message.text])
        bot.send_message(message.chat.id, f'Расписание на "{message.text}":\n\n{res}')
        menu(message, 'Выберите пункт:')
        return

    else:
        bot.send_message(message.chat.id, 'Ну дурак есть дурак!\nДля особо одарённых я добавил кнопки!')
        menu(message, 'Выберите пункт:')
        return


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
        return

    else:
        bot.send_message(message.chat.id, 'Ну вот дурак, он и есть дурак!\nДля особо одарённых я добавил кнопки!')
        menu(message, 'Выберите пункт, дурак:')
        return

    menu(message, 'Выберите пункт:')


def get_user_number(message: types.Message):
    res = message.text.split(',')
    if len(res) > 4095:
        bot.send_message(message.chat.id, 'Ну ты кнч жесть даун... Куда столько символов?')
        menu(message, 'Выберите пункт меню: ')
        return

    if ',' not in str(res):
        bot.send_message(message.chat.id, 'Идиот! Где запятая?')
        menu(message, 'Выберите пункт меню: ')
        return

    try:
        res = list(map(int, res))
    except ValueError:
        bot.send_message(message.chat.id, 'Ты идиот? Вводи числа!')
        menu(message, 'Выберите пункт меню: ')
        return

    if len(res) != 2:
        bot.send_message(message.chat.id, 'Идиот! Надо вводить два числа через запятую!')
        menu(message, 'Выберите пункт меню: ')
        return

    start_range, end_range = sorted(res)

    bot.send_message(message.chat.id, f"Ваше число: {randint(start_range, end_range)}")
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
