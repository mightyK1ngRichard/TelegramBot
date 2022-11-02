# Copyright © 2022 mightyK1ngRichard <dimapermyakov55@gmail.com>

import json
from random import randint


class User:
    def __init__(self, id_user: int, name: str, age: int, phone_number: str):
        self.id_user = id_user
        self.name = name
        self.age = age
        self.phone_number = phone_number


def add_user() -> dict:
    data = User(2, input('имя: '), int(input('возраст: ')), input('телефон: '))
    res = dict()
    res[data.id_user] = {'name': data.name, 'age': data.age, 'phone_number': data.phone_number}
    return res


def main():
    lst = []
    lst.append(User(0, 'дима', 19, '0930'))
    lst.append(User(1, 'вова', 19, '33'))
    for el in lst:
        if el.name == 'вова':
            print(el.id_user)
            break


if __name__ == '__main__':
    main()
