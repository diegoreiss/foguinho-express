from time import sleep
from os import system
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
            return main()

        senha = mask_password()
        if senha == '1':
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
            back_to_home()


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


def back_to_home():
        end_points('Voltando ao menu principal')
        return True


def cadastro_pessoa():
    while True:
        print('\n[1] - Voltar\n')
        nome_pessoa = input('Nome: ')
        back_to_cadastro(nome_pessoa)
        if len(nome_pessoa) == 0 or nome_pessoa.isalpha() == False:
            print('Informe seu nome corretamente!!!')
            continue

        while True:
            dt_nasc_pessoa = input('Data de nascimento Ex:(ddmmaaaa): ')
            back_to_cadastro(dt_nasc_pessoa)
            if len(dt_nasc_pessoa) == 8:
                data_formatada = format_date(dt_nasc_pessoa)
                break
            else:
                print('Inválido! Informe conforme o exemplo')
                continue

        while True:
            email_pessoa = input('Email: ')
            back_to_cadastro(email_pessoa)
            if '@' and '.' not in email_pessoa:
                print('Informe um email corretamente!!! Ex: exemplo@exemplo.com')
                continue
            break
        break




def cadastro_admin():
    header2('CADASTRO ADMIN')
    cadastro_pessoa()
    while True:
        login_admin = input('Login: ')
        back_to_cadastro(login_admin)
    
    

        senha_admin = mask_password()




def cadastro_cliente():
    header2('CADASTRO CLIENTE')
    cadastro_pessoa()



def back_to_cadastro(b):
    if b == '1':
        end_points('Voltando ao menu de cadastro')
        return pagina_cadastro()
        

main()