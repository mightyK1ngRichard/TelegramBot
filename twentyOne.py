# Copyright © 2022 mightyK1ngRichard <dimapermyakov55@gmail.com>
from random import choice


class Card:
    def __init__(self, name: str, suit: str, number: int):
        self.suit = suit
        self.name = name
        self.number = number


CARDS = [
    Card(name='шестёрка', suit='пики', number=6),
    Card(name='семёрка', suit='пики', number=7),
    Card(name='восьмёрка', suit='пики', number=8),
    Card(name='девятка', suit='пики', number=9),
    Card(name='десятка', suit='пики', number=10),
    Card(name='валет', suit='пики', number=8),
    Card(name='дама', suit='пики', number=9),
    Card(name='король', suit='пики', number=10),
    Card(name='туз', suit='пики', number=11),

    Card(name='шестёрка', suit='крести', number=6),
    Card(name='семёрка', suit='крести', number=7),
    Card(name='восьмёрка', suit='крести', number=8),
    Card(name='девятка', suit='крести', number=9),
    Card(name='десятка', suit='крести', number=10),
    Card(name='валет', suit='крести', number=8),
    Card(name='дама', suit='крести', number=9),
    Card(name='король', suit='крести', number=10),
    Card(name='туз', suit='крести', number=11),

    Card(name='шестёрка', suit='черви', number=6),
    Card(name='семёрка', suit='черви', number=7),
    Card(name='восьмёрка', suit='черви', number=8),
    Card(name='девятка', suit='черви', number=9),
    Card(name='десятка', suit='черви', number=10),
    Card(name='валет', suit='черви', number=8),
    Card(name='дама', suit='черви', number=9),
    Card(name='король', suit='черви', number=10),
    Card(name='туз', suit='черви', number=11),

    Card(name='шестёрка', suit='буби', number=6),
    Card(name='семёрка', suit='буби', number=7),
    Card(name='восьмёрка', suit='буби', number=8),
    Card(name='девятка', suit='буби', number=9),
    Card(name='десятка', suit='буби', number=10),
    Card(name='валет', suit='буби', number=8),
    Card(name='дама', suit='буби', number=9),
    Card(name='король', suit='буби', number=10),
    Card(name='туз', suit='буби', number=11),
]


def game() -> tuple:
    user_sum = 0
    banker_sum = 0
    flag_for_banker = True
    while True:
        answer = bool(input('Взять или стоп? 1|0: '))
        if answer:
            res = CARDS.pop(CARDS.index(choice(CARDS)))
            user_sum += res.number
            print(f'Выпала карта: {res.name} {res.suit}')
            if user_sum > 21:
                return 'Вы проиграли!', user_sum, banker_sum
        print(f'Сумма игрока = {user_sum}')

        # Ход банкира.
        if flag_for_banker:
            res = CARDS.pop(CARDS.index(choice(CARDS)))
            print(f'Выпала карта: {res.name} {res.suit}')
            banker_sum += res.number
            if banker_sum > 21:
                return 'Банкир проиграл!', user_sum, banker_sum

            if banker_sum == 21:
                return 'Банкир победил', user_sum, banker_sum

            elif (banker_sum > 15 and answer) or (banker_sum > user_sum and not answer):
                flag_for_banker = False
                print('Банкир закончил набирать карты!')

        print(f'Сумма банкира = {banker_sum}')
        print(f'\n{"-" * 30}\n')


if __name__ == '__main__':
    res_game, user_sum_res, bot_sum = game()
    print(f'{res_game}\nВаш результат: {user_sum_res}\nРезультат банкира: {bot_sum}')
