# Copyright © 2022 mightyK1ngRichard <dimapermyakov55@gmail.com>

TIME_TABLE = {
    "числитель": {
        "понедельник": [
            'Самостоятельная работа',
        ],
        "вторник": [
            'Экология (сем)',
            'ТВиМС (сем)',
            'Электротехника (сем)',
            'ТВиМС (лек)'
        ],
        "среда": [
            'Модели данных (лек)',
            'Физика (лек)',
            'Модели данных (лаб)',
            'Модели данных (лаб)'
        ],
        "четверг": [
            'Физра',
            'Физика(сем)',
            'Иностранный язык (сем)'
        ],
        "пятница": [
            'Электротехника (лек)',
            'АСОИУ (лек)',
            'Электроника (лаб)',
            'Электроника (лаб)'
        ],
        "суббота": [
            'Правоведение (лек)',
            'ТВиМС (лек)',
            'Физра'
        ],
        "воскресенье": [
            'Самостоятельная работа.'
        ]
    },
    "знаменатель": {

    }
}


def main():
    # lst = list(map(lambda el: el.strip().lower(), input().split(',')))
    # if 'числитель' in lst:
    #     lst.remove('числитель')
    # print(lst)
    res = (TIME_TABLE['числитель']['вторник'])
    res = '\n'.join(res)
    print(res)


if __name__ == '__main__':
    main()
