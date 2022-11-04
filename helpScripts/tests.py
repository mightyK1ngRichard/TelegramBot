# Copyright © 2022 mightyK1ngRichard <dimapermyakov55@gmail.com>
import json
import re

Num = 0


class Player:
    def __init__(self, user_name: str, user_role: str | None, choosing_partner: int | None):
        self.name = user_name
        self.role = user_role
        self.choosing_partner = choosing_partner


def main():
    # global Num
    Num = 8
    print(Num)


if __name__ == '__main__':
    main()
