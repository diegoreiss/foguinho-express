from time import sleep
from datetime import datetime
from random import randint
from useful import *
from database import *

clear()
conexao()

def main():
    while True:
        header1('FOGUINHO EXPRESS')
        menu_principal = input('[1] - Login\n[2] - Cadastro\n\n[3] - Sair\n\n-> ')
        match menu_principal:
            case '1':
                clear()
                pagina_login()
            case '2':
                clear()
                pagina_cadastro()
            case '3':
                sair()
            case _:
                print('Inválido! Informe Corretamente!')
                sleep(1)
                clear()
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

        if validar_login(login, senha):
            dados = pegar_dados(login, senha)
            print('Login efetuado com sucesso!!!')
            sleep(1)
            print(f'Bem vindo {dados[1][0]}!!!')
            sleep(1)
            clear()
            break
        else:
            print('Login ou senha incorreto, informe novamente!')
            sleep(1)
            clear()
            continue
    
    match dados[2]:
        case 'Administrador':
            pagina_admin(login, senha)
        case 'Cliente':
            pagina_cliente(login, senha)
    

def pagina_admin(l, s):
    dados_admin = pegar_dados(l, s)
    while True:
        header1('PÁGINA ADMIN')
        opc = input('O que você deseja fazer?\n\n[1] - Gerenciar produtos\n[2] - Ver pessoas cadastradas\n\n[3] - Sair\n\n-> ')

        match opc:
            case '1':
                clear()
                gerenciamento_produto(l, s)
            case '2':
                pessoas_cadastradas()
            case '3':
                end_points('Saindo')
                return pagina_login()
            case _:
                print('Inválido! Informe corretamente!')
                sleep(1)
                clear()
                continue


def gerenciamento_produto(l, s):
    dados_admin = pegar_dados(l, s)
    while True:
        header1('GERENCIAMENTO DE PRODUTOS')
        opc = input('O que você deseja fazer?\n\n[1] - Adicionar produto\n[2] - Remover produto\n[3] - Ver produtos cadastrados\n\n[4] - Sair\n\n-> ')

        match opc:
            case '1':
                clear()
                cadastro_produto(l, s)
            case '2':
                remover_produto(l, s)
            case '3':
                produtos_cadastrados(l, s)
            case '4':
                end_points('Saindo')
                return pagina_admin(l, s)
                

def cadastro_produto(l, s):
    dados_admin = pegar_dados(l, s)
    adicionado_por = ''
    while True:
        header1('CADASTRO PRODUTO')
        print('\n[1] - Voltar\n')
        nome_produto = input('Nome do Produto: ').strip().title()
        
        
        
        valor_produto= float(input(f'Valor do(a) {nome_produto}: R$'))
        
        
        categoria_produto = input('Categoria do produto: ').strip().title()
        
        break    
        
    for i in dados_admin[1]:
        adicionado_por += i + ' '

    id_admin = dados_admin[1]
    
    insert_produto(nome_produto, valor_produto, categoria_produto, adicionado_por, id_admin)
    
    print(f'{nome_produto} cadastrado com sucesso!')
    end_points('Voltando ao menu de gerenciamento de produtos')
    return gerenciamento_produto(l, s)

def remover_produto(l, s):
    pass


def produtos_cadastrados(l, s):
    pass


def pagina_cliente(l, s):
    while True:
        header1('PÁGINA CLIENTE')
        opc = input('O que você deseja fazer?\n[1] - Comprar Produtos\n[2] - Meu histórico de compras\n[3] - Informações sobre minha conta\n\n[4] - Sair\n-> ')
        
        match opc:
            case '1':
                pass
            case '2':
                pass
            case '3':
                pass
            case '4':
                end_points('Saindo')
                return pagina_login()
            case _:
                print('Inválido! Informe corretamente!')
                sleep(1)
                clear()
                continue

    
def pagina_cadastro():
    header2('CADASTRO')
    opc = input('Qual cadastro deseja realizar?\n[1] - Admin        [3] - Sair\n[2] - Cliente\n-> ')
    match opc:
        case '1':
            clear()
            cadastro_admin()
        case '2':
            clear()
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
                clear()
                quit()
            case 'N':
                clear()
                break
            case _:
                print('Inválido! Informe corretamente?')
                continue





def cadastro_pessoa():
    while True:
        nome_pessoa = input('Nome: ').strip().title()
        if len(nome_pessoa) == 0:
            print('Informe seu nome corretamente!!!')
            continue
        else:
            break

    while True:
        dt_nasc_pessoa = input('Data de nascimento Ex:(ddmmaaaa): ')
        if len(dt_nasc_pessoa) == 8:
            data_formatada = format_date(dt_nasc_pessoa)
            break
        else:
            print('Inválido! Informe conforme o exemplo')
            continue

    while True:
        email_pessoa = input('Email: ').strip()
        if '@' and '.' not in email_pessoa:
            print('Informe um email corretamente!!! Ex: exemplo@exemplo.com')
            continue
        else:
            break
    
    insert_pessoa(nome_pessoa, dt_nasc_pessoa, email_pessoa)
    

def cadastro_admin():
    header2('CADASTRO ADMIN')
    cadastro_pessoa()
    matricula = randint(100000, 999999)
    desde = datetime.today().strftime('%d-%m-%Y')
    
    insert_admin(matricula, desde)
    
    while True:
        login_admin = input('Login: ')
        if not validar_cadastro(login_admin):
            print('Usuário ja existe!')
            continue

        
        senha_admin = mask_password()
        
        perfil = 'Administrador'
        
        break
    
    insert_admin_login(login_admin, senha_admin, perfil)
    end_points('Voltando ao menu principal')
    return main()


def cadastro_cliente():
    header2('CADASTRO CLIENTE')
    cadastro_pessoa()
    matricula = randint(100000, 999999)
    desde = datetime.today().strftime('%d-%m-%Y')
    
    insert_cliente(matricula, desde)
    
    while True:
        login_cliente = input('Login: ')
        if not validar_cadastro(login_cliente):
            print('Usuário ja existe! Informe novamente')
            sleep(1)
            continue

        senha_cliente = mask_password()
        perfil = 'Cliente'

        break
    
    insert_cliente_login(login_cliente, senha_cliente, perfil)
    end_points('Voltando ao menu principal')
    return main()
    





main()