# Copyright © 2022 mightyK1ngRichard <dimapermyakov55@gmail.com>
import json
import re


class Player:
    def __init__(self, user_name: str, user_role: str | None, choosing_partner: int | None):
        self.name = user_name
        self.role = user_role
        self.choosing_partner = choosing_partner


def main():
    d = {
        5: 3,
        4: 2
    }
    print(d)
    d.clear()
    print(d)


if __name__ == '__main__':
    main()
