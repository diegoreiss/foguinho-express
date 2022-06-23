from database import *
from useful import *

Database()
while True:
    header('MENU PRINCIPAL')
    opc = input('[1] - Login\n[2] - Cadastro\n[3] - Ver cadastros\n[4] - Sair\n-> ')
    match opc:
        case '1':
            clear()
            validate()
            wait(1)
            while True:
                header('FASE DE TESTES LOGIN EFETUADO')
                opc2 = input('[1] - Visualizar meu dados\n[2] - Logout\n-> ')
                match opc2:
                    case '1':
                        print('Testes...')
                    case '2':
                        points('Saindo')
                        clear()
                        break
        case '2':
            nome = input('Nome: ')
            senha = input('Senha: ')
            insert(nome, senha)
            print('Cadastro feito')
            wait(1)
            clear()
        case '3':
            header('PESSOAS CADASTRADAS')
            view()
            wait(3)
            clear()
        case '4':
            points('Programa Finalizando')
            clear()
            break
        case _:
            print('Inválido!')
        

