import re
import os
import stdiomask
from time import sleep
from random import randint
from datetime import date, datetime


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


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


def mask_password():
    senha = stdiomask.getpass(prompt='Senha: ', mask='*')
    return senha


def date_today():
    return date.today().strftime('%d-%m-%Y')


def format_date(date):
    formatted_date = f'{date[:2]}-{date[2:4]}-{date[4:]}'
    return formatted_date


def validar_email(email):
    padrao = r'^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]*@[a-zA-Z]+\.[a-z]{1,3}$'
    if re.fullmatch(padrao, email):
        return True
    else:
        return False
    

def validar_data(data):
    try:
        datetime.strptime(data, '%d-%m-%Y')
        return True
    except ValueError:
        return False


def gerar_matricula_administrador():
    matricula_admin = f'{randint(0, 9999)}-A'
    return matricula_admin


def gerar_matricula_cliente():
    matricula_cliente = f'{randint(0, 9999)}-C'
    return matricula_cliente
    
    
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def format_float(flt):
    format_num = f'R${flt:.2f}'
    return format_num.replace('.', ',')
