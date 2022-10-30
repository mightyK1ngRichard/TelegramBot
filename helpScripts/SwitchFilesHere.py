# Copyright © 2022 mightyK1ngRichard <dimapermyakov55@gmail.com>

TOKEN = '5715759447:AAFCFHQ9M1xLp_KRcKKe2Bqk_XORZXXo5vg'

TIME_TABLE = {
    "числитель": {
        "Понедельник": [
            'Самостоятельная работа',
        ],
        "Вторник": [
            '1. Экология (сем) - 732л',
            '2. ТВиМС (сем) - 830л',
            '3. Электротехника (сем) - 529л',
            '4. ТВиМС (лек) - 224л'
        ],
        "Среда": [
            'Модели данных (лек) - 501ю',
            'Физика (лек) - 501ю',
            'Модели данных (лаб) - 306.2э',
            'Модели данных (лаб) - 306.2э'
        ],
        "Четверг": [
            '1. Физра - каф. ФВ',
            '2. Физика(сем) - 259л',
            '3. Иностранный язык (сем) - каф. Л2'
        ],
        "Пятница": [
            '1. Электротехника (лек) - 501ю',
            '2. АСОИУ (лек) - 501ю',
            '3. Электроника (лаб) - 215м',
            '4. Электроника (лаб) - 215м'
        ],
        "Суббота": [
            '1. Правоведение (лек) - 224л',
            '2. ТВиМС (лек) - 224л',
            '3. Физра - каф. ФВ'
        ],
        "Воскресенье": [
            'Самостоятельная работа.'
        ]
    },
    "знаменатель": {
        "Понедельник": [
            'Самостоятельная работа',
        ],
        "Вторник": [
            '1. ТВиМС (сем) - 830л',
            '2. Правоведение (сем) - 615л',
            '3. Экология (лек) - 224л'
        ],
        "Среда": [
            '1. Модели данных (лек) - 501ю',
            '2. Физика (лек) - 501ю',
            '3. Физика (лаб) - каф. ФН4',
            '4. Физика (лаб) - каф. ФН4'
        ],
        "Четверг": [
            '1. Физра - каф. ФВ',
            '2. Базовые компоненты интернет технологий (лек) - 224л',
            '3. Иностранный язык (сем) - каф. Л2'
            '3. Базовые компоненты интернет технологий (сем) - 306.2э'
        ],
        "Пятница": [
            '1. Электротехника (лек) - 501ю',
            '2. АСОИУ (лек) - 501ю'
        ],
        "Суббота": [
            '1. Правоведение (лек) - 224л',
            '2. ТВиМС (лек) - 224л',
            '3. Физра - каф. ФВ'
        ],
        "Воскресенье": [
            'Самостоятельная работа.'
        ]
    }
}


class Card:
    def __init__(self, name: str, suit: str, number: int):
        self.suit = suit
        self.name = name
        self.number = number


CARDS = [
    Card(name='Двойка', suit='Пики', number=2),
    Card(name='Тройка', suit='Пики', number=3),
    Card(name='Четвёрка', suit='Пики', number=4),
    Card(name='Пятёрка', suit='Пики', number=5),
    Card(name='Шестёрка', suit='Пики', number=6),
    Card(name='Семёрка', suit='Пики', number=7),
    Card(name='Восьмёрка', suit='Пики', number=8),
    Card(name='Девятка', suit='Пики', number=9),
    Card(name='Десятка', suit='Пики', number=10),
    Card(name='Валет', suit='Пики', number=2),
    Card(name='Дама', suit='Пики', number=3),
    Card(name='Король', suit='Пики', number=4),
    Card(name='Туз', suit='Пики', number=11),

    Card(name='Двойка', suit='Крести', number=2),
    Card(name='Тройка', suit='Крести', number=3),
    Card(name='Четвёрка', suit='Крести', number=4),
    Card(name='Пятёрка', suit='Крести', number=5),
    Card(name='Шестёрка', suit='Крести', number=6),
    Card(name='Семёрка', suit='Крести', number=7),
    Card(name='Восьмёрка', suit='Крести', number=8),
    Card(name='Девятка', suit='Крести', number=9),
    Card(name='Десятка', suit='Крести', number=10),
    Card(name='Валет', suit='Крести', number=2),
    Card(name='Дама', suit='Крести', number=3),
    Card(name='Король', suit='Крести', number=4),
    Card(name='Туз', suit='Крести', number=11),

    Card(name='Двойка', suit='Черви', number=2),
    Card(name='Тройка', suit='Черви', number=3),
    Card(name='Четвёрка', suit='Черви', number=4),
    Card(name='Пятёрка', suit='Черви', number=5),
    Card(name='Шестёрка', suit='Черви', number=6),
    Card(name='Семёрка', suit='Черви', number=7),
    Card(name='Восьмёрка', suit='Черви', number=8),
    Card(name='Девятка', suit='Черви', number=9),
    Card(name='Десятка', suit='Черви', number=10),
    Card(name='Валет', suit='Черви', number=2),
    Card(name='Дама', suit='Черви', number=3),
    Card(name='Король', suit='Черви', number=4),
    Card(name='Туз', suit='Черви', number=11),

    Card(name='Двойка', suit='Буби', number=2),
    Card(name='Тройка', suit='Буби', number=3),
    Card(name='Четвёрка', suit='Буби', number=4),
    Card(name='Пятёрка', suit='Буби', number=5),
    Card(name='Шестёрка', suit='Буби', number=6),
    Card(name='Семёрка', suit='Буби', number=7),
    Card(name='Восьмёрка', suit='Буби', number=8),
    Card(name='Девятка', suit='Буби', number=9),
    Card(name='Десятка', suit='Буби', number=10),
    Card(name='Валет', suit='Буби', number=2),
    Card(name='Дама', suit='Буби', number=3),
    Card(name='Король', suit='Буби', number=4),
    Card(name='Туз', suit='Буби', number=11),
]
