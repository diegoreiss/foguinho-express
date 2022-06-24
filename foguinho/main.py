from time import sleep
from os import system
from paginas_loja import pagina_login, pagina_cadastro, sair
from useful import header1

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

main()