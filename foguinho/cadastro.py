from useful import *
import paginas_loja


def format_date(d):
    date = f'{d[:2]}-{d[2:4]}-{d[4:]}'
    return date


def format_cpf(c):
    cpf = f'{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}'
    return cpf


def cadastro_pessoa():
    while True:
        print('\n[1] - Voltar\n')
        nome_pessoa = input('Nome: ')
        if back(nome_pessoa):
            break
        elif len(nome_pessoa) == 0 or nome_pessoa.isalpha() == False:
            print('Informe seu nome corretamente!!!')
            continue

        while True:
            dt_nasc_pessoa = input('Data de nascimento Ex:(ddmmaaaa): ')
            if back(dt_nasc_pessoa):
                break
            elif len(dt_nasc_pessoa) == 8:
                data_formatada = format_date(dt_nasc_pessoa)
                break
            else:
                print('Inválido! Informe conforme o exemplo')
                continue

        while True:
            email_pessoa = input('Email: ')
            if '@' and '.' not in email_pessoa:
                print('Informe um email corretamente!!! Ex: exemplo@exemplo.com')
                continue
            break

        while True:
            cpf_pessoa = format_cpf(input('CPF: '))
            if cpf_pessoa > 11:
                print('Informe o cpf corretamente!!! Ex: 12345678900')
            break

        cadastro_endereco_pessoa()



def cadastro_endereco_pessoa():
    while True:
        cep = input('CEP')
        if len(cep) > 8:
            print('Informe seu CEP corretamente!')
            continue
        break


    logradouro = input('Logradouro: ')
    num = input('N°: ')
    bairro = input('Bairro: ')
    cidade = input('Cidade: ')
    
    while True:
        estado = input('Estado: ').upper().strip()
        if len(estado) > 2:
            print('Informe corretamente! Ex: SP')
        


def cadastro_admin():
    header2('CADASTRO ADMIN')
    cadastro_pessoa()
    login_admin = 0






def cadastro_cliente():
    header2('CADASTRO CLIENTE')
    cadastro_pessoa()



def back(b):
    if b == '1':
        end_points('Voltando ao menu de cadastro')
        paginas_loja.pagina_cadastro()
        return True
        