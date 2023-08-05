# coding=utf-8
# author=uliontse

from data import *


def test_data():
    for lottery_name in ('ssq', 'qlc', 'kl8', '3d', 'dlt', 'pls', 'plw', 'qxc'):
        print(f'{lottery_name}: {load_random_data(lottery_name=lottery_name, amount=2)}')
        print(load_history_data(lottery_name=lottery_name).shape)


if __name__ == '__main__':
    test_data()
