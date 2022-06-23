from time import sleep
from os import system
from loja import *
from useful import * 


while True:
    header1('FOGUINHO EXPRESS')
    menu_principal = input('[1] - Login\n[2] - Cadastro\n\n[3] - Sair\n\n-> ')
    match menu_principal:
        case '1':
            system('clear')
            pagina_login()
        case '2':
            system('clear')
            pagina_cadastro()
        case '3':
            sair()
        case _:
            print('Inválido! Informe Corretamente!')
            sleep(1)
            system('clear')
            continue
