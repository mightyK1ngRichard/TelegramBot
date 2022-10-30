# Copyright © 2022 mightyK1ngRichard <dimapermyakov55@gmail.com>

import json


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
    with open("data.json", "a") as write_file:
        json.dump(add_user(), write_file)


if __name__ == '__main__':
    main()
