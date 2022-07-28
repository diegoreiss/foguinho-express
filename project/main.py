import useful
import database
from time import sleep
from tabulate import tabulate

database.conexao()
database.tabelas()
useful.clear()


def main():
    while True:
        useful.header1('FOGUINHO EXPRESS')
        menu_principal = input('\n[1] - Login\n[2] - Cadastro\n\n[3] - Sair\n\n>> ')

        match menu_principal:
            case '1':
                useful.clear()
                pagina_login()
            case '2':
                useful.clear()
                pagina_cadastro()
            case '3':
                sair_do_mercado()
            case _:
                print('\nINVÁLIDO! Informe um dos itens acima!!!')
                sleep(1)
                useful.clear()


def pagina_login():
    while True:
        useful.header2('LOGIN')
        print('\n[1] - Voltar\n')

        login = input('Login: ')
        if login == '1':
            print()
            useful.end_points('Voltando ao menu principal')
            useful.clear()
            return main()
        else:
            senha = useful.mask_password()

            if senha == '1':
                print()
                useful.end_points('Voltando ao menu principal')
                useful.clear()
                return main()
            else:
                if database.efetuar_login(login, senha):
                    dados_usuario_logado = database.pegar_dados_login(login, senha)
                    primeiro_nome_usuario = dados_usuario_logado[1].split()
                    print('\nLogin efetuado com sucesso!!!')
                    sleep(1)
                    print(f'Bem vindo {primeiro_nome_usuario[0]}!')
                    sleep(1)
                    match dados_usuario_logado[2]:
                        case 'Administrador':
                            pagina_administrador(dados_usuario_logado)
                        case 'Cliente':
                            pagina_cliente(dados_usuario_logado)
                else:
                    print('\nLogin ou senha incorretos. Informe novamente.')
                    sleep(1)
                    useful.clear()
                    continue


def pagina_cadastro():
    while True:
        useful.header2('CADASTRO')
        opcao_cadastro = input(
            '\nQual cadastro deseja realizar?\n\n[1] - Administrador\n[2] - Cliente\n\n[3] - Sair\n\n>> ')

        match opcao_cadastro:
            case '1':
                pagina_cadastro_administrador()
            case '2':
                pagina_cadastro_cliente()
            case '3':
                print()
                useful.end_points('Voltando ao menu principal')
                useful.clear()
                return main()
            case _:
                print('\nINVÁLIDO! Informe um dos itens acima!!!')
                sleep(1)
                useful.clear()


def pagina_cadastro_pessoa():
    print()
    while True:
        nome_pessoa = input('Nome: ').strip().lower().title()

        if len(nome_pessoa) == 0:
            print('Infome um nome, por favor.')
            continue
        elif not nome_pessoa.replace(' ', '').isalpha():
            print('INVÁLIDO! Informe um nome válido!')
            continue
        else:
            print()
            break

    while True:
        dt_nasc_pessoa = input('Data de Nascimento (formato DDMMAAAA): ').strip()

        if len(dt_nasc_pessoa) > 8 or len(dt_nasc_pessoa) < 8:
            print('INVÁLIDO! Informe conforme o exemplo dado!')
            continue
        elif not dt_nasc_pessoa.isdecimal():
            print('INVÁLIDO! Informe uma data válida!!!')
            continue
        else:
            data_formatada = useful.format_date(dt_nasc_pessoa)

            if useful.validar_data(data_formatada):
                break
            else:
                print('A data que você inseriu é inválida, informe novamente.')
                sleep(1)
                continue

    while True:
        email_pessoa = input('\nEmail: ')

        if useful.validar_email(email_pessoa):
            if database.validar_email_cadastro(email_pessoa):
                break
            else:
                print('O email que você inseriu ja pertence a outro usuário. Informe outro email.')
                sleep(1)
                continue
        else:
            print('O email que você inseriu é inválido, informe novamente.')
            sleep(1)
            continue

    lista_dados_pessoa = [nome_pessoa, data_formatada, email_pessoa]

    return lista_dados_pessoa


def pagina_cadastro_administrador():
    useful.clear()
    useful.header2('CADASTRO ADMINISTRADOR')

    while True:
        lista_dados_admin = []
        pegar_lista_dados_admin = pagina_cadastro_pessoa()

        while True:
            username_administrador = input('\nNome de Usuário: ').strip()
            if database.validar_username_cadastro(username_administrador):
                break
            else:
                print('Esse nome de usuário já foi cadastrado. Informe novamente.')
                sleep(1)
                continue
        print()

        while True:
            print('Cadastre uma senha entre 6 e 16 caracteres')
            senha_administrador = useful.mask_password()

            if senha_administrador == '':
                print('\nInforme uma senha para a sua conta de administrador.')
                continue
            elif len(senha_administrador) < 6 or len(senha_administrador) > 16:
                print('\nA sua senha não corresponde as regras de senha informados')
                continue
            else:
                break

        nomes_coluna = ['NOME', 'DT_NASCIMENTO', 'EMAIL']
        for dado in pegar_lista_dados_admin:
            for nome in nomes_coluna:
                lista_dados_admin.append([nome, dado])
                nomes_coluna.remove(nome)
                break
        print()

        lista_dados_admin.append(['NOME DE USUÁRIO', username_administrador])
        lista_dados_admin.append(['SENHA', senha_administrador])

        useful.clear()

        while True:
            useful.header2('SUAS INFORMAÇÕES')
            print(tabulate(lista_dados_admin, headers=['COLUNA', 'VALORES'], tablefmt='psql'))
            confirmar_cadastro_admin = input(
                '\nDeseja confirmar seu cadastro?\n\n[1] - Sim\n[2] - Limpar e refazer cadastro\n\n[3] - Limpar e '
                'sair do menu de cadastro\n\n>> ')

            match confirmar_cadastro_admin:
                case '1':
                    break
                case '2':
                    break
                case '3':
                    print()
                    useful.end_points('Limpando')
                    useful.end_points('Voltando a página de cadastro inicial')
                    useful.clear()
                    return pagina_cadastro()
                case _:
                    print('\nINVÁLIDO! Informe um dos itens acima.')
                    sleep(1)
                    useful.clear()

        if confirmar_cadastro_admin == '1':

            while True:
                matricula = useful.gerar_matricula_administrador()
                if database.validar_matricula_admin(matricula):
                    break
                else:
                    continue

            dt_cadastro = useful.date_today()
            perfil = 'Administrador'

            database.insert_pessoa(lista_dados_admin[0][1], lista_dados_admin[1][1], lista_dados_admin[2][1])
            database.insert_admin(matricula, dt_cadastro)
            database.insert_admin_login(lista_dados_admin[3][1], lista_dados_admin[4][1], perfil)

            print('\nCadastro concluído!!!')
            sleep(1)
            useful.end_points('Voltando ao menu principal')
            useful.clear()
            return main()
        elif confirmar_cadastro_admin == '2':
            print()
            useful.end_points('Limpando')
            useful.end_points('Voltando ao início do cadastro')
            useful.clear()
            useful.header2('CADASTRO ADMINISTRADOR')
            continue


def pagina_cadastro_cliente():
    useful.clear()
    useful.header2('CADASTRO CLIENTE')

    while True:
        lista_dados_cliente = []
        pegar_lista_dados_cliente = pagina_cadastro_pessoa()

        while True:
            username_cliente = input('\nNome de Usuário: ').strip()
            if database.validar_username_cadastro(username_cliente):
                break
            else:
                print('Esse nome de usuario já foi cadastrado. Informe novamente.')
                sleep(1)
                continue

        print()

        while True:
            print('Cadastre uma senha entre 6 e 16 caracteres')
            senha_cliente = useful.mask_password()

            if senha_cliente == '':
                print('\nInforme uma senha para a sua conta de cliente.')
            elif len(senha_cliente) < 6 or len(senha_cliente) > 16:
                print('\nA sua senha não corresponde as regras de senha informados.')
                continue
            else:
                break

        nomes_coluna = ['NOME', 'DT_NASCIMENTO', 'EMAIL']
        for dado in pegar_lista_dados_cliente:
            for nome in nomes_coluna:
                lista_dados_cliente.append([nome, dado])
                nomes_coluna.remove(nome)
                break
        print()

        lista_dados_cliente.append(['NOME DE USUARIO', username_cliente])
        lista_dados_cliente.append(['SENHA', senha_cliente])

        useful.clear()

        while True:
            useful.header2('SUAS INFORMAÇÕES')
            print(tabulate(lista_dados_cliente, headers=['COLUNA', 'VALORES'], tablefmt='psql'))
            confirmar_cadastro_cliente = input(
                '\nDeseja confirmar seu cadastro?\n\n[1] - Sim\n[2] - Limpar e refazer cadastro\n\n[3] - Limpar e '
                'sair do menu de cadastro\n\n>> ')

            match confirmar_cadastro_cliente:
                case '1':
                    break
                case '2':
                    break
                case '3':
                    print()
                    useful.end_points('Limpando')
                    useful.end_points('Voltando a página de cadastro inicial')
                    useful.clear()
                    return pagina_cadastro()
                case _:
                    print('\nINVÁLIDO! Informe um dos itens acima.')
                    sleep(1)
                    useful.clear()

        if confirmar_cadastro_cliente == '1':

            while True:
                matricula = useful.gerar_matricula_cliente()
                if database.validar_matricula_cliente(matricula):
                    break
                else:
                    continue

            dt_cadastro = useful.date_today()
            perfil = 'Cliente'

            database.insert_pessoa(lista_dados_cliente[0][1], lista_dados_cliente[1][1], lista_dados_cliente[2][1])
            database.insert_cliente(matricula, dt_cadastro)
            database.insert_cliente_login(lista_dados_cliente[3][1], lista_dados_cliente[4][1], perfil)

            print('\nCadastro concluído!!!')
            sleep(1)
            useful.end_points('Voltando ao menu principal')
            useful.clear()
            return main()
        elif confirmar_cadastro_cliente == '2':
            print()
            useful.end_points('Limpando')
            useful.end_points('Voltando ao início do cadastro')
            useful.clear()
            useful.header2('CADASTRO CLIENTE')


def pagina_administrador(dados):
    useful.clear()
    while True:
        useful.header1('PÁGINA ADMIN')
        opcao_admin = input(f'\nO que deseja fazer {dados[1].split()[0]}?\n'
                            '\n[1] - Gerenciar produtos'
                            '\n[2] - Ver pessoas cadastradas\n'
                            '\n[3] - Sair\n\n>> ')
        match opcao_admin:
            case '1':
                gerenciamento_produto(dados)
            case '2':
                ver_pessoas_cadastradas()
            case '3':
                print()
                useful.end_points('Saindo')
                useful.clear()
                return pagina_login()
            case _:
                print('\nINVÁLIDO! Informe um dos itens acima.')
                sleep(1)
                useful.clear()
                continue


def gerenciamento_produto(dados):
    useful.clear()
    while True:
        useful.header1('GERENCIAMENTO DE PRODUTOS')
        opcao_gerenciamento = input('\nO que deseja fazer?\n\n[1] - Adicionar produto\n[2] - Remover produto\n[3] - '
                                    'Ver produtos cadastrados\n\n[4] - Sair\n\n>> ')
        match opcao_gerenciamento:
            case '1':
                cadastro_produto(dados)
            case '2':
                remover_produto()
            case '3':
                ver_produtos_cadastrados()
            case '4':
                print()
                useful.end_points('Saindo')
                return pagina_administrador(dados)
            case _:
                print('\nINVÁLIDO! Informe um dos itens acima.')
                sleep(1)
                useful.clear()
                continue


def cadastro_produto(dados):
    useful.clear()
    while True:
        useful.header1('CADASTRO DE PRODUTO')

        while True:
            nome_produto = input('\nNome do produto: ').strip().title()

            if nome_produto == '':
                print('\nInforme um nome para o seu produto, por favor.')
                sleep(1)
                continue
            elif not nome_produto.replace(' ', '').replace(',', '').isalnum():
                print('Informe um nome válido para o seu produto!')
                sleep(1)
                continue
            elif not database.validar_nome_produto(nome_produto):
                print(f'O produto {nome_produto} ja foi cadastrado! Informe novamente!')
                sleep(1)
            else:
                break

        while True:
            valor_produto = input(f'\nValor do produto {nome_produto}: R$').strip().replace('.', ',')

            if valor_produto == '':
                print('\nInforme um valor para o seu produto, por favor.')
                sleep(1)
                continue
            elif useful.isfloat(valor_produto.replace(',', '.')):
                valor_produto = useful.format_float(float(valor_produto.replace(',', '.')))
                break
            else:
                print('Informe um valor válido para seu produto.')
                sleep(1)
                continue

        while True:
            categoria_produto = input(f'\nCategoria do produto {nome_produto}: ').strip().title()

            if categoria_produto == '':
                print('\nInforme um nome para a categoria do seu produto, por favor.')
                sleep(1)
                continue
            elif not categoria_produto.replace(' ', '').isalpha():
                print('\nINVÁLIDO! Informe uma categoria válida!')
                sleep(1)
                continue
            else:
                break

        tabela_produto = []
        nome_coluna_produtos = ['NOME', 'VALOR', 'CATEGORIA']
        lista_produto = [nome_produto, valor_produto, categoria_produto]

        for dado in lista_produto:
            for nome in nome_coluna_produtos:
                tabela_produto.append([nome, dado])
                nome_coluna_produtos.remove(nome)
                break

        useful.clear()

        while True:
            useful.header2('INFORMAÇÕES DO PRODUTO')
            print(tabulate(tabela_produto, headers=['COLUNA', 'VALORES'], tablefmt='psql'))
            confirmar_cadastro_produto = input('\nDeseja confirmar seu cadastro?\n\n[1] - Sim\n[2] - Limpar e refazer '
                                               'cadastro de produtos\n\n[3] - Limpar e sair do menu de cadastro de '
                                               'produtos\n\n>> ')
            match confirmar_cadastro_produto:
                case '1':
                    break
                case '2':
                    break
                case '3':
                    print()
                    useful.end_points('Limpando')
                    useful.end_points('Voltando a página de gerenciamento de produtos')
                    useful.clear()
                    return gerenciamento_produto(dados)
                case _:
                    print('\nINVÁLIDO! Informe um dos itens acima.')
                    sleep(1)
                    useful.clear()

        if confirmar_cadastro_produto == '1':
            database.insert_produto(nome_produto, valor_produto, categoria_produto)
            database.insert_produtos_cadastrados(dados[0], database.ultimo_produto_cadastrado(), dados[1], useful.date_today())
            print(f'\nCadastro de {nome_produto} concluído!!!')
            sleep(1)
            useful.end_points('Voltando ao menu de gerenciamento de produtos')
            useful.clear()
            return gerenciamento_produto(dados)
        elif confirmar_cadastro_produto == '2':
            print()
            useful.end_points('Limpando')
            useful.end_points('Voltando ao inicio do cadastro')
            useful.clear()
            continue


def remover_produto():
    useful.clear()
    while True:
        useful.header2('REMOVER PRODUTOS')
        produtos_cadastrados = database.show_produtos_cadastrados()
        if produtos_cadastrados == 0:
            print('\nAinda não tem nenhum produto cadastrado... :(')
            try:
                opcao_sair = int(input('\n[0] - Voltar\n\n>> '))
            except ValueError:
                print('\nInválido! Informe corretamente!')
                sleep(1)
                useful.clear()
                continue
            if opcao_sair == 0:
                print()
                useful.end_points('Voltando')
                useful.clear()
                break
            elif opcao_sair != 0:
                print('INVÁLIDO! Informe corretamente!')
                sleep(1)
                useful.clear()
                continue
        else:
            print(produtos_cadastrados)
            try:
                opcao_remover = int(input('\n[0] - Voltar\n\nInforme o identificador(ID) do produto que '
                                          'deseja remover\n\n>> '))
            except ValueError:
                print('\nINVÁLIDO! Informe corretamente!')
                sleep(1)
                useful.clear()
                continue

            if opcao_remover == 0:
                print()
                useful.end_points('Voltando')
                useful.clear()
                break
            elif database.select_produto(opcao_remover) is None:
                print('\nO id desse produto foi removido ou não existe. Informe novamente.')
                sleep(1)
                useful.clear()
                continue
            else:
                while True:
                    opcao_remover_double_check = input(f'\nTem certeza que quer remover o produto '
                                                       f'{database.select_produto(opcao_remover)}? [S/N]: ')\
                                                        .strip().upper()
                    match opcao_remover_double_check:
                        case 'S':
                            print(f'\n{database.select_produto(opcao_remover)} removido! :(')
                            database.delete_produto(opcao_remover)
                            sleep(2)
                            useful.clear()
                            break
                        case 'N':
                            break
                        case _:
                            print('\nINVÁLIDO! Informe apenas S ou N!')
                            sleep(1)
                            continue

                if opcao_remover_double_check == 'N':
                    useful.clear()
                    continue


def ver_produtos_cadastrados():
    while True:
        useful.clear()
        useful.header2('PRODUTOS CADASTRADOS')
        produtos_cadastrados = database.show_produtos_cadastrados()
        if produtos_cadastrados == 0:
            print('\nAinda não tem nenhum produto cadastrado... :(')
            opcao_sair = input('\n[0] - Voltar\n\n>> ')
            match opcao_sair:
                case '0':
                    print()
                    useful.end_points('Voltando')
                    useful.clear()
                    break
        else:
            useful.clear()
            useful.header2('PRODUTOS CADASTRADOS')
            database.show_produtos_e_quem_cadastrou()
            while True:
                opcao_produtos_cadastrados = input('\n[1] - Visualização padrão\n[2] - Ordenar por categoria\n\n[3] - Voltar\n\n>> ')
                match opcao_produtos_cadastrados:
                    case '1':
                        useful.clear()
                        useful.header2('PRODUTOS CADASTRADOS')
                        database.show_produtos_e_quem_cadastrou()
                    case '2':
                        while True:
                            useful.clear()
                            useful.header2('ORDENAR')
                            print()
                            print('Categorias cadastradas:')
                            database.show_categorias()
                            opcao_ordenar = input('\nInforme a categoria que deseja ordenar:\n\n>> ').title()
                            categoria_encontrada = database.ordenar_por_categoria_admin(opcao_ordenar)
                            if categoria_encontrada == 0:
                                print('\nNão existe essa categoria! Informe o que existe na lista!!!')
                                sleep(1)
                                useful.clear()
                                continue
                            else:
                                useful.clear()
                                useful.header2('PRODUTOS CADASTRADOS')
                                categoria_encontrada = database.ordenar_por_categoria_admin(opcao_ordenar)
                                break
                    case '3':
                        print()
                        useful.end_points('Voltando')
                        useful.clear()
                        break
                    case _:
                        print('\nINVÁLIDO! Informe um dos itens da lista.')
                        sleep(1)
                        useful.clear()
                        useful.header2('PRODUTOS CADASTRADOS')
                        produtos_cadastrados = database.show_produtos_cadastrados()
                        print(produtos_cadastrados)                        
                        continue
                    
            if opcao_produtos_cadastrados == '3':
                break


def ver_pessoas_cadastradas():
    useful.clear()
    useful.header2('PESSOAS CADASTRADAS')
    database.show_pessoas_cadastradas()
    while True:
        opcoes_pessoas_cadastradas = input('\n[1] - Visualização mais detalhada\n[2] - Apenas '
                                           'administradores\n[3] - Apenas clientes\n\n[4] - Sair\n\n>> ')
        match opcoes_pessoas_cadastradas:
            case '1':
                useful.clear()
                useful.header2('VISUALIZAÇÃO MAIS DETALHADA')
                database.show_detalhes_pessoas_cadastradas()
            case '2':
                useful.clear()
                useful.header2('APENAS ADMINISTRADORES')
                database.show_apenas_administradores()
            case '3':
                useful.clear()
                useful.header2('APENAS CLIENES')
                if database.show_apenas_clientes() == 0:
                    print('\nAinda não tem nenhum cliente cadastrado... :(')
            case '4':
                print()
                useful.end_points('Saindo')
                useful.clear()
                break
            case _:
                print('\nINVÁLIDO! Informe um dos itens da lista acima')
                sleep(1)
                useful.clear()
                useful.header2('PESSOAS CADASTRADAS')
                database.show_pessoas_cadastradas()
                continue


def pagina_cliente(dados):
    useful.clear()
    while True:
        useful.header1('PÁGINA CLIENTE')
        opcao_cliente = input(f'\nO que deseja fazer {dados[1].split()[0]}?\n'
                              '\n[1] - Comprar produtos'
                              '\n[2] - Informações sobre minha conta'
                              '\n[3] - Meu histórico de compras\n'
                              '\n[4] - Sair\n\n>> ')
        match opcao_cliente:
            case '1':
                loja(dados)
            case '2':
                while True:
                    useful.clear()
                    database.informacoes_cliente_logado(dados)
                    opcao_sair = input('\n[0] - Sair\n\n>> ')
                    
                    match opcao_sair:
                        case '0':
                            print()
                            useful.end_points('Saindo')
                            useful.clear()
                            break
                        case _:
                            print('\nINVÁLIDO! Digite 0 para sair!!!')
                            sleep(1)
                            useful.clear()
                            continue
            case '3':
                produtos_vendidos(dados)
            case '4':
                print()
                useful.end_points('Saindo')
                useful.clear()
                return pagina_login()
            case _:
                print('\nINVÁLIDO! Informe um dos itens acima!')
                sleep(1)
                useful.clear()
                continue
            

def loja(dados):
    soma = 0
    carrinho = []
    produto = []
    total_compra = [['R$0,00']]
    while True:
        produtos_encontrados = database.show_produtos_cadastrados()
        if produtos_encontrados == 0:
            print('\nAinda não tem nenhum produto cadastrado... :('
                  '\nTente novamente mais tarde.')
            sleep(2)
            return pagina_cliente(dados)
        else:
            useful.clear()
            produtos_encontrados = database.show_produtos_cadastrados()
            print(tabulate(total_compra, headers=["TOTAL"], tablefmt="fancy_grid"))
            while True:
                useful.clear()
                useful.header1('PRODUTOS')
                print(produtos_encontrados)
                print(tabulate(total_compra, headers=["TOTAL"], tablefmt="fancy_grid"))
                opcao_loja = input('\nO que deseja fazer?\n'
                                    '\n[1] - Comprar um produto'
                                    '\n[2] - Ver carrinho'
                                    '\n[3] - Ordenar'
                                    '\n[4] - Finalizar Compra\n'
                                    '\n[5] - Sair\n\n>> ')
                match opcao_loja:
                    case '1':
                        try:
                            produto, soma, total_compra = comprar_produto(produtos_encontrados, carrinho, total_compra, soma)
                            carrinho.append(produto[:])
                        except TypeError:
                            continue
                    case '2':
                        carrinho, soma, total_compra = ver_carrinho(carrinho, soma, total_compra, dados)
                    case '3':
                        produtos_encontrados = ordenar_categoria(produtos_encontrados)
                    case '4':
                        database.insert_produtos_vendidos(dados, carrinho)
                        print('\nMuito obrigado por comprar em nossa loja!!!')
                        sleep(1)
                        useful.end_points('Voltando a tela de cliente')
                        return pagina_cliente(dados)
                    case '5':
                        sair_loja(dados, carrinho)
                    case _:
                        print('\nINVÁLIDO! Informe corretamente!!!')
                        sleep(1)
                        continue
                    
                    
def produtos_vendidos(dados):
    while True:
        registro_compras = database.ver_produtos_vendidos(dados)
        
        if len(registro_compras) == 0:
            print('\nVocê é novo por aqui! :)')
            sleep(1)
            print('Que tal fazer umas compras???')
            sleep(2)
            useful.clear()
            break
        else:
            useful.clear()
            while True:
                useful.header2('HISTÓRICO DE COMPRAS')
                print(tabulate(registro_compras, headers=['NOME', 'PRODUTO', 'VALOR UNITÁRIO', 'QUANTIDADE COMPRADA', 'DATA DA COMPRA'], tablefmt='psql'))
                opcao_sair = input('\n[0] - Sair\n\n>> ')
                match opcao_sair:
                    case '0':
                        print()
                        useful.end_points('Saindo')
                        return pagina_cliente(dados)
                    case _:
                        print('\nINVÁLIDO! Informe corretamente!!!')
                        sleep(1)
                        useful.clear()
                        continue


def comprar_produto(produtos, carrinho, total_compra, soma):
    while True:
        useful.clear()
        useful.header2('COMPRA')
        print(produtos)
        try:
            id_produto_compra = int(input('\nInforme o identificador(ID) do produto que deseja comprar\n\n>> '))
        except ValueError:
            print('\nINVÁLIDO! Informe corretamente!!!')
            sleep(1)
            continue
        else:
            if database.select_all_info_produto(id_produto_compra) == None:
                print('\nEsse produto foi excluido ou não existe. Informe novamente.')
                sleep(1)
                continue
            else:
                id_produto = database.select_all_info_produto(id_produto_compra)[0]
                nome_produto = database.select_all_info_produto(id_produto_compra)[1]
                valor_produto = database.select_all_info_produto(id_produto_compra)[2]
                while True:
                    try:
                        quantidade = int(input(f'\nInforme a quantidade de {nome_produto} que deseja comprar\n\n>> '))
                    except ValueError:
                        print('\nINVÁLIDO! Informe corretamente!')
                        sleep(1)
                        continue
                    else:
                        useful.clear()
                        total = useful.format_float(float(database.select_all_info_produto(id_produto_compra)[2][2:].replace(',', '.')) * quantidade)
                        print()
                        useful.header2('INFORMAÇÕES DA COMPRA')
                        lista_produto = [[nome_produto, valor_produto, quantidade, total]]
                        print(tabulate(lista_produto, headers=["NOME", "PREÇO UNIDADE", "QUANTIDADE", "TOTAL"], tablefmt='psql'))
                        while True:
                            confirmar_compra = input('\nDeseja confirmar a compra?\n'
                                                    '\n[1] - Sim'
                                                    f'\n[2] - Mudar a quantidade do produto {nome_produto}'
                                                    '\n[3] - Descartar e escolher outro produto\n'
                                                    '\n[4] - Descartar e sair da escolha de produtos\n\n>> ')
                            match confirmar_compra:
                                case '1':
                                    soma += float(total[2:].replace(',', '.'))
                                    total_compra = [[f'{useful.format_float(soma)}']]
                                    carrinho = [id_produto, nome_produto, valor_produto, quantidade]
                                    print(f'\nProduto {nome_produto} adicionado com sucesso!\nVisualize seu carrinho!')
                                    sleep(2)
                                    useful.end_points('Voltando ao início da loja')
                                    return [carrinho, soma, total_compra]
                                case '2':
                                    print()
                                    useful.end_points(f'Voltando a quantidade do produto {nome_produto}')
                                    break
                                case '3':
                                    print()
                                    useful.end_points(f'Descartado compra do produto {nome_produto}')
                                    useful.end_points('Voltando ao início da escolha de produtos')
                                    break
                                case '4':
                                    print()
                                    useful.end_points(f'Descartado compra do produto {nome_produto}')
                                    useful.end_points('Saindo da escolha de produtos')
                                    return None
                                case _:
                                    print('\nINVÁLIDO! Informe corretamente!!!')
                                    sleep(1)
                                    continue
                                
                        match confirmar_compra:
                            case '3':
                                break
                                                    

def ver_carrinho(carrinho, soma, total_compra, dados):
    if len(carrinho) == 0:
        print('\nAinda não tem nenhum produto no seu carrinho.')
        sleep(1)
        print('\nQue tal adicionar algo? :)')
        sleep(2)
        return loja(dados)
    else:
        while True:
            useful.clear()
            useful.header2(f'CARRINHO DE {dados[1].upper()}')
            print(tabulate(carrinho, headers=["ID", "NOME", "VALOR", "QUANTIDADE"], tablefmt="fancy_grid"))
            print(tabulate(total_compra, headers=["TOTAL"], tablefmt="fancy_grid"))
            opcao_carrinho = input('\nO que deseja fazer?\n'
                                   '\n[1] - Remover produtos\n'
                                   '\n[2] - Sair\n\n>> ')
            match opcao_carrinho:
                case '1':
                    carrinho, soma, total_compra = remover_produto_carrinho(carrinho, soma, total_compra, dados)
                    if len(carrinho) == 0:
                        print('\nSem produtos no carrinho!')
                        useful.end_points('Voltando ao início da loja')
                        break
                case '2':
                    print()
                    useful.end_points('Voltando ao início da loja')
                    break
                case _:
                    print('\nINVÁLIDO! Informe um dos itens acima!!!')
                    sleep(1)
                    continue

        return [carrinho, soma, total_compra]

def remover_produto_carrinho(carrinho, soma, total_compra, dados):
    while True:
        try:
            id_produto = int(input('\nInforme o identificador(ID) do produto para remover\n\n>> '))
        except ValueError:
            print('INVÁLIDO! Informe corretamente!')
            sleep(1)
            continue
        else:
            for produto in range(len(carrinho)):
                if carrinho[produto][0] == id_produto:
                    while True:
                        opcao_remover_do_carrinho = input(f'\nTem certeza que deseja remover o produto {carrinho[produto][1]}? [S/N]: ').upper().strip()[0]
                        match opcao_remover_do_carrinho:
                            case 'S':
                                valor_produto_escolhido = float(carrinho[produto][2][2:].replace(',', '.'))
                                quantidade_produto_escolhido = carrinho[produto][3]
                                soma -= valor_produto_escolhido * quantidade_produto_escolhido
                                total_compra = [[f'{useful.format_float(soma)}']]
                                print(f'{carrinho[produto][1]} removido!')
                                carrinho.remove(carrinho[produto])
                                sleep(1)
                                useful.end_points('Voltando')
                                return [carrinho, soma, total_compra]
                            case 'N':
                                ver_carrinho(carrinho, soma, total_compra, dados)
                            case _:
                                print('INVÁLIDO! Informe apenas S ou N!!!')
                                sleep(1)
                                continue
            else:
                print('\nO produto com esse ID não está no seu carrinho. Informe novamente.')
                sleep(1)
                continue
                    

def ordenar_categoria(produtos_encontrados):
    while True:
        useful.clear()
        useful.header1('ORDENAR')
        print(produtos_encontrados)
        opcao_ordenar_produtos = input('\n[1] - Ordenação padrão\n[2] - Ordenar por categoria\n\n>> ')
        match opcao_ordenar_produtos:
            case '1':
                produtos_encontrados = database.show_produtos_cadastrados()
                useful.clear()
                break
            case '2':
                useful.clear()
                while True:
                    useful.header2('ORDENAR')
                    database.show_categorias()
                    print('\nCategorias cadastradas:\n')
                    nome_categoria = input('\nInforme o nome da categoria que deseja ordenar\n\n>> ').title()
                    
                    tabela_categoria = database.ordenar_por_categoria_cliente(nome_categoria)
                    
                    if tabela_categoria == 0:
                        print('\nEssa categoria não está listada!!! Informe corretamente!')
                        sleep(1)
                        useful.clear()
                        continue
                    else:
                        produtos_encontrados = tabela_categoria
                        break
                break
                    
    return produtos_encontrados


def sair_loja(dados, carrinho):
    if len(carrinho) == 0:
        print('\nSem comprar nada? :(')
        sleep(1)
        print('Tudo bem :) Volte sempre!!!')
        sleep(1)
        return pagina_cliente(dados)
    else:
        while True:
            opc_sair = input('\nSeus produtos no carrinho serão perdidos!!!\nTem certeza disso? [S/N]: ').upper().strip()[0]
            match opc_sair:
                case 'S':
                    print('\nTudo bem :) Volte sempre!!!')
                    sleep(2)
                    return pagina_cliente(dados)
                case 'N':
                    break
                case _:
                    print('\nINVÁLIDO! Informe apenas S ou N!!!')
                    sleep(1)
    

def sair_do_mercado():
    while True:
        sair = input('\nTem certeza? [S/N]: ').strip().upper()

        match sair:
            case 'S':
                useful.header1('VOLTE SEMPRE!')
                sleep(2)
                useful.clear()
                quit()
            case 'N':
                useful.clear()
                break
            case _:
                print('INVÁLIDO! Informe apenas S ou N!!!')


main()
