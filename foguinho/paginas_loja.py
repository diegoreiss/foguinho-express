from useful import *
from os import system
from time import sleep
from cadastro import cadastro_admin, cadastro_cliente


def pagina_login():

    while True:
        header2('LOGIN')
        print('\n[1] - Voltar\n')
        login = input('Login: ')

        if login == '1':
            end_points('Voltando ao menu principal')
            break    

        senha = input('Senha: ')

        if senha == '1':
            end_points('Voltando ao menu principal')
            break


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
            pass


def sair():
    while True:
        sair = input('Tem certeza? [S/N]: ').strip().upper()
        match sair:
            case 'S':
                header1('VOLTE SEMPRE!')
                sleep(2)
                quit()
            case 'N':
                system('cls')
                break
            case _:
                print('Inválido! Informe corretamente?')
                continue