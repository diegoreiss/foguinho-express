from time import sleep
from os import system
import stdiomask

    
def header1(msg):
    print('=' * 50)
    print(f'{msg:^50}')
    print('=' * 50)
    

def header2(msg):
    print('=-' * 25)
    print(f'{msg:^50}')
    print('=-' * 25)
    

def end_points(msg):
    print(msg, end='')
    for _ in range(4):
        print('.', end='', flush=True)
        sleep(0.5)
    print()
    system('cls')


def format_date(d):
    date = f'{d[:2]}-{d[2:4]}-{d[4:]}'
    return date


def mask_password():
    senha = stdiomask.getpass(prompt='Senha: ', mask='*')
    return senha