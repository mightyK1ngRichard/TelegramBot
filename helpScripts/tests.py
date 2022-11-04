# Copyright © 2022 mightyK1ngRichard <dimapermyakov55@gmail.com>
import json
import re


class Player:
    def __init__(self, user_name: str, user_role: str | None, choosing_partner: int | None):
        self.name = user_name
        self.role = user_role
        self.choosing_partner = choosing_partner


def main():
    lst = {
        '0': 6,
        '1': 2,
    }
    print((lst))
    del(lst['0'])
    print((lst))


if __name__ == '__main__':
    main()
