from time import sleep
from os import system


def header(s):
    print('='* 50)
    print(f'{s:^50}')
    print('='* 50)


def points(s):
    print(s, end='')
    for _ in range(4):
        print('.', end='', flush=True)
        sleep(0.5)
    print()


def clear():
    system('clear')


def wait(n):
    sleep(n)