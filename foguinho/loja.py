from useful import *
from os import system
from time import sleep


def pagina_login():
    header2('LOGIN')
    login = input('Login: ')
    senha = input('Senha: ')


def pagina_cadastro():
    header2('CADASTRO')
    opc = input('Qual cadastro deseja realizar?\n[1] - Admin        [3] - Sair\n[2] - Cliente\n-> ')
    match opc:
        case '1':
            pass
            #cadastro_admin()
        case '2':
            pass
            #cadastro_cliente()
        case '3':
            end_points('Voltando ao menu principal')
            pass


def cadastro_admin():
    pass


def sair():
    while True:
        sair = input('Tem certeza? [S/N]: ').strip().upper()[0]
        match sair:
            case 'S':
                header1('VOLTE SEMPRE!')
                sleep(2)
                quit()
            case 'N':
                break
            case _:
                print('Inválido! Informe corretamente?')
                continue
    pass