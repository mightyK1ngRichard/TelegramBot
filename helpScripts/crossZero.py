# Copyright © 2022 mightyK1ngRichard <dimapermyakov55@gmail.com>

from random import sample


def cross_zero(using_bot=False):
    data = ['ind=' + str(el) for el in range(9)]
    elements = ['  x  ', '  0  ']
    free_elements = [int(el) for el in range(9)]
    for i in range(9):
        # Игра с ботом.
        if using_bot:
            # Ход игрока.
            if i % 2 == 0:
                print_cross_zero(data)
                index = (input('Enter the index: '))

                try:
                    for letter in index:
                        if letter.isalpha():
                            raise ValueError('Letter in the word!')

                except ValueError:
                    print('Letter in the word!')
                    i -= 1
                    continue

                index = int(index)
                if data[index] != '  x  ' and data[index] != '  0  ' and 0 <= index <= 8:
                    data[index] = elements[i % 2]
                    free_elements.pop(free_elements.index(index))

                else:
                    print('Value with this index has already created.')
                    print('repeat the input!')
                    i -= 1
                    continue

            # Ход бота.
            else:
                index_bot = sample(free_elements, 1)
                free_elements.pop(free_elements.index(index_bot[0]))
                data[index_bot[0]] = elements[i % 2]

        # Игра без бота.
        else:
            print_cross_zero(data)
            index = (input('Enter the index: '))
            if index.isalpha():
                print('Enter the number!')
                i -= 1
                continue

            index = int(index)
            if data[index] != '  x  ' and data[index] != '  0  ' and 0 <= index <= 8:
                data[index] = elements[i % 2]

            else:
                print('Value with this index has already created.')
                print('repeat the input!')
                i -= 1
                continue

        # Проверка полей.
        for el_cross_zero in elements:
            res = [] * 1
            res.append(all(map(lambda el: el == el_cross_zero, data[:3])))
            res.append(all(map(lambda el: el == el_cross_zero, data[3:6])))
            res.append(all(map(lambda el: el == el_cross_zero, data[6:])))
            if any(res):
                print_cross_zero(data)
                return f'\'{el_cross_zero.strip()}\' is winner!'

            res.clear()
            res.append(all(map(lambda el: el == el_cross_zero, data[::3])))
            res.append(all(map(lambda el: el == el_cross_zero, data[1::3])))
            res.append(all(map(lambda el: el == el_cross_zero, data[2::3])))
            if any(res):
                print_cross_zero(data)
                return f'\'{el_cross_zero.strip()}\' is winner!'
            res.clear()

            res.append(all(map(lambda el: el == el_cross_zero, data[::4])))
            res.append(all(map(lambda el: el == el_cross_zero, data[2:7:2])))
            if any(res):
                print_cross_zero(data)
                return f'\'{el_cross_zero.strip()}\' is winner!'

            res.clear()

    return 'friendship won'


def print_cross_zero(arr):
    print('\n' + '-' * 25)
    print(end='|')
    for i, el in enumerate(arr):
        print(' ' + el, end=' |')
        if i == 2 or i == 5:
            print('\n' + '-' * 25)
            print(end='|')
    print('\n' + '-' * 25)


print(cross_zero(using_bot=True))
