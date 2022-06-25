
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
        return paginas_loja.pagina_cadastro()
        