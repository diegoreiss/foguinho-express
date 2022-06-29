from time import sleep
import os
import stdiomask
from tabulate import tabulate
    
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
    for _ in range(3):
        print('.', end='', flush=True)
        sleep(0.5)
    print()
    clear()


def format_date(d):
    date = f'{d[:2]}-{d[2:4]}-{d[4:]}'
    return date


def format_float(f):
    float_num = f
    format_num = f'R${float_num:.2f}'
    return format_num.replace('.', ',')
    

def mask_password():
    senha = stdiomask.getpass(prompt='Senha: ', mask='*')
    return senha


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    