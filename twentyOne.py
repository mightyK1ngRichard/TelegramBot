# Copyright © 2022 mightyK1ngRichard <dimapermyakov55@gmail.com>
from random import choice


class Card:
    def __init__(self, name: str, suit: str, number: int):
        self.suit = suit
        self.name = name
        self.number = number


CARDS = [
    Card(name='Шестёрка', suit='Пики', number=6),
    Card(name='Семёрка', suit='Пики', number=7),
    Card(name='Восьмёрка', suit='Пики', number=8),
    Card(name='Девятка', suit='Пики', number=9),
    Card(name='Десятка', suit='Пики', number=10),
    Card(name='Валет', suit='Пики', number=8),
    Card(name='Дама', suit='Пики', number=9),
    Card(name='Король', suit='Пики', number=10),
    Card(name='Туз', suit='Пики', number=11),

    Card(name='Шестёрка', suit='Крести', number=6),
    Card(name='Семёрка', suit='Крести', number=7),
    Card(name='Восьмёрка', suit='Крести', number=8),
    Card(name='Девятка', suit='Крести', number=9),
    Card(name='Десятка', suit='Крести', number=10),
    Card(name='Валет', suit='Крести', number=8),
    Card(name='Дама', suit='Крести', number=9),
    Card(name='Король', suit='Крести', number=10),
    Card(name='Туз', suit='Крести', number=11),

    Card(name='Шестёрка', suit='Черви', number=6),
    Card(name='Семёрка', suit='Черви', number=7),
    Card(name='Восьмёрка', suit='Черви', number=8),
    Card(name='Девятка', suit='Черви', number=9),
    Card(name='Десятка', suit='Черви', number=10),
    Card(name='Валет', suit='Черви', number=8),
    Card(name='Дама', suit='Черви', number=9),
    Card(name='Король', suit='Черви', number=10),
    Card(name='Туз', suit='Черви', number=11),

    Card(name='Шестёрка', suit='Буби', number=6),
    Card(name='Семёрка', suit='Буби', number=7),
    Card(name='Восьмёрка', suit='Буби', number=8),
    Card(name='Девятка', suit='Буби', number=9),
    Card(name='Десятка', suit='Буби', number=10),
    Card(name='Валет', suit='Буби', number=8),
    Card(name='Дама', suit='Буби', number=9),
    Card(name='Король', suit='Буби', number=10),
    Card(name='Туз', suit='Буби', number=11),
]


def game() -> tuple:
    user_sum = 0
    banker_sum = 0
    flag_for_banker = True
    while True:
        answer = True if input('Взять или стоп? 1|0: ') == '1' else False
        if not answer and not flag_for_banker:
            return 'Игрок победил', user_sum, banker_sum if user_sum > banker_sum else 'Ничья', user_sum, banker_sum \
                if user_sum == banker_sum else 'Банкир победил', user_sum, banker_sum

        elif answer:
            res = CARDS.pop(CARDS.index(choice(CARDS)))
            user_sum += res.number
            print(f'Выпала карта: {res.name} {res.suit}')
            if user_sum > 21:
                return 'Вы проиграли!', user_sum, banker_sum
            elif user_sum == 21:
                return 'Игрок победил', user_sum, banker_sum
        print(f'==> Сумма игрока = {user_sum}')

        # Ход банкира.
        if flag_for_banker:
            res = CARDS.pop(CARDS.index(choice(CARDS)))
            print(f'Выпала карта: {res.name} {res.suit}')
            banker_sum += res.number
            if banker_sum > 21:
                return 'Банкир проиграл!', user_sum, banker_sum

            elif banker_sum == 21:
                return 'Банкир победил', user_sum, banker_sum

            elif (banker_sum > 15 and answer) or (banker_sum > user_sum and not answer):
                flag_for_banker = False
                print('Банкир закончил набирать карты!')
                if not answer and not flag_for_banker:
                    return ('Игрок победил', user_sum, banker_sum) if user_sum > banker_sum else (
                        'Ничья', user_sum, banker_sum) if user_sum == banker_sum else (
                        'Банкир победил', user_sum, banker_sum)
    print(f'==> Сумма банкира = {banker_sum}')
    print(f'\n{"-" * 30}\n')


if __name__ == '__main__':
    res_game, user_sum_res, bot_sum = game()
    print(f'{res_game}\nВаш результат: {user_sum_res}\nРезультат банкира: {bot_sum}')
