from time import sleep
from os import system
from datetime import datetime
from random import randint
from useful import *

system('cls')


def main():
    while True:
        header1('FOGUINHO EXPRESS')
        menu_principal = input('[1] - Login\n[2] - Cadastro\n\n[3] - Sair\n\n-> ')
        match menu_principal:
            case '1':
                system('cls')
                pagina_login()
            case '2':
                system('cls')
                pagina_cadastro()
            case '3':
                sair()
            case _:
                print('Inválido! Informe Corretamente!')
                sleep(1)
                system('cls')
                continue





def pagina_login():
    while True:
        header2('LOGIN')
        print('\n[1] - Voltar\n')
        login = input('Login: ')
        if login == '1':
            end_points('Voltando ao menu principal')
            return main()

        senha = mask_password()
        if senha == '1':
            end_points('Voltando ao menu principal')
            return main()


def pagina_cadastro():
    header2('CADASTRO')
    opc = input('Qual cadastro deseja realizar?\n[1] - Admin        [3] - Sair\n[2] - Cliente\n-> ')
    match opc:
        case '1':
            system('cls')
            cadastro_admin()
        case '2':
            system('cls')
            cadastro_cliente()
        case '3':
            end_points('Voltando ao menu principal')
            return main()


def sair():
    while True:
        sair = input('Tem certeza? [S/N]: ').strip().upper()
        match sair:
            case 'S':
                header1('VOLTE SEMPRE!')
                sleep(2)
                system('cls')
                quit()
            case 'N':
                system('cls')
                break
            case _:
                print('Inválido! Informe corretamente?')
                continue





def cadastro_pessoa():
    while True:
        print('\n[1] - Voltar\n')
        nome_pessoa = input('Nome: ')
        if nome_pessoa == '1':
          end_points('Voltando ao menu de cadastro')
          return pagina_cadastro()  
        elif len(nome_pessoa) == 0 or nome_pessoa.isalpha() == False:
            print('Informe seu nome corretamente!!!')
            continue
        else:
            break

    while True:
        dt_nasc_pessoa = input('Data de nascimento Ex:(ddmmaaaa): ')
        if dt_nasc_pessoa == '1':
            end_points('Voltando ao menu de cadastro')
            return pagina_cadastro()
        elif len(dt_nasc_pessoa) == 8:
            data_formatada = format_date(dt_nasc_pessoa)
            break
        else:
            print('Inválido! Informe conforme o exemplo')
            continue

    while True:
        email_pessoa = input('Email: ')
        if email_pessoa == '1':
            end_points('Voltando ao menu de cadastro')
            return pagina_cadastro()
        if '@' and '.' not in email_pessoa:
            print('Informe um email corretamente!!! Ex: exemplo@exemplo.com')
            continue
        break


def cadastro_admin():
    header2('CADASTRO ADMIN')
    cadastro_pessoa()
    matricula = randint(100000, 999999)
    desde = datetime.today().strftime('%d-%m-%Y')
    while True:
        login_admin = input('Login: ')
        if login_admin == '1':
            end_points('Voltando ao menu de cadastro')
            return pagina_cadastro()
        
        senha_admin = mask_password()
        if senha_admin == '1':
            end_points('Voltando ao menu de cadastro')
            return pagina_cadastro()
        
        perfil = 'Administrador'
        
        break


def cadastro_cliente():
    header2('CADASTRO CLIENTE')
    cadastro_pessoa()
    matricula = randint(100000, 999999)
    desde = datetime.today().strftime('%d-%m-%Y')
    while True:
        login_cliente = input('Login: ')
        if login_cliente == '1':
            end_points('Voltando ao menu de cadastro')
            return pagina_cadastro()
        
        senha_cliente = mask_password()
        if senha_cliente == '1':
            end_points('Voltando ao menu de cadastro')
            return pagina_cadastro()
        
        perfil = 'Cliente'
        
        break
    





main()