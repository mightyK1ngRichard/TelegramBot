# Copyright © 2022 mightyK1ngRichard <dimapermyakov55@gmail.com>
from random import randint

social_network = {
    '📶 Соц.сети':
        {
            'GitHub': 'https://github.com/mightyK1ngRichard',
            'VK': 'https://vk.com/mightyk1ngrichard'
        },
    '🎲 Рандомное число': f'{randint(0, 1000)}'
}


def main():
    print(social_network[0])


if __name__ == '__main__':
    main()
