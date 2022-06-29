import sqlite3
from sqlite3 import Error
from tabulate import tabulate
from useful import *
from datetime import datetime

def conexao():
    global conn, cursor
    try:
        conn = sqlite3.connect("foguinho/banco.db")
        cursor = conn.cursor()
    except Error as ex:
        print(ex)
        

def tabelas():
    create_tables = """
        CREATE TABLE IF NOT EXISTS pessoa(
            id_pessoa INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_pessoa VARCHAR(60),
            dt_nasc_pessoa DATE(10),
            email_pessoa VARCHAR(60)
        );
        
        CREATE TABLE IF NOT EXISTS cliente(
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula VARCHAR(6),
            desde DATE(10),
            id_pessoa INTEGER REFERENCES pessoa(id_pessoa)
        );
        
        CREATE TABLE IF NOT EXISTS admin(
            id_admin INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula VARCHAR(6),
            desde DATE(10),
            id_pessoa INTEGER REFERENCES pessoa(id_pessoa)
        );
        
        CREATE TABLE IF NOT EXISTS login(
            id_login INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(60),
            senha VARCHAR(60),
            perfil VARCHAR(20),
            id_admin INTEGER REFERENCES admin(id_admin),
            id_cliente INTEGER REFERENCES cliente(id_cliente)
        );
        
        CREATE TABLE IF NOT EXISTS produto(
            id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_produto VARCHAR(60),
            valor_produto VARCHAR(6),
            categoria_produto VARCHAR(60),
            adicionado_por VARCHAR(60),
            id_admin INTEGER REFERENCES admin(id_admin)  
        );
        
        CREATE TABLE IF NOT EXISTS produtos_vendidos(
            id_cliente INTEGER REFERENCES cliente(id_cliente),
            id_produto INTEGER REFERENCES produto(id_prouto),
            quantidade INTEGER(6),
            dt_compra DATE(10)
        );
    """
    with conn:
        try:
            cursor.executescript(create_tables)
        except Error as ex:
            print(ex)


def insert_pessoa(n, d, e):
    dados_pessoa = [n, d, e]
    query = """
        INSERT INTO pessoa (nome_pessoa, dt_nasc_pessoa, email_pessoa)
        VALUES (?, ?, ?)
    """
    with conn:
        try:
            cursor.execute(query, dados_pessoa)
        except Error as ex:
            print(ex)
        

def insert_admin(m, d):
    query = """
        SELECT MAX(id_pessoa) FROM pessoa
    """
    with conn:
        cursor.execute(query)
        id_pessoa = cursor.fetchone()[0]
    
    dados_admin = [m, d, id_pessoa]
    query2 = f"""
        INSERT INTO admin (matricula, desde, id_pessoa)
        VALUES (?, ?, ?)
    """
    with conn:
        try:
            cursor.execute(query2, dados_admin)
        except Error as ex:
            print(ex)


def insert_cliente(m, d):
    query1 = """
        SELECT MAX(id_pessoa) FROM pessoa
    """
    with conn:
        cursor.execute(query1)
        id_pessoa = cursor.fetchone()[0]
    
    dados_cliente = [m, d, id_pessoa]
    query2 = """
        INSERT INTO cliente (matricula, desde, id_pessoa)
        VALUES (?, ?, ?)
    """
    with conn:
        try:
            cursor.execute(query2, dados_cliente)
        except Error as ex:
            print(ex)
            

def insert_admin_login(u, s, p):
    query1 = """
        SELECT MAX(id_admin) FROM admin
    """
    with conn:
        cursor.execute(query1)
        id_admin = cursor.fetchone()[0]
    
    login_admin = [u, s, p, id_admin]    
    query2 = """
        INSERT INTO login (username, senha, perfil, id_admin)
        VALUES(?, ?, ?, ?)
    """
    with conn:
        try:
            cursor.execute(query2, login_admin)
            print('Conta criada com sucesso!')
        except Error as ex:
            print(ex)
    

def insert_cliente_login(u, s, p):
    query1 = """
        SELECT MAX(id_cliente) FROM cliente
    """
    with conn:
        cursor.execute(query1)
        id_cliente = cursor.fetchone()[0]
    
    login_cliente = [u, s, p, id_cliente]    
    query2 = """
        INSERT INTO login (username, senha, perfil, id_cliente)
        VALUES (?, ?, ?, ?)
    """
    with conn:
        try:
            cursor.execute(query2, login_cliente)
            print('Conta criada com sucesso!')
        except Error as ex:
            print(ex)
            
    


def validar_login(u, s):
    query = f"""
        SELECT username, senha FROM login 
        WHERE username = '{u}' AND senha = '{s}'
    """
    with conn:
        cursor.execute(query)
        dados = cursor.fetchone()
        if dados == None:
            result = False
        else:
            result = True 
            
    return result


def pegar_dados(u, s):
    query = f"""
        SELECT P.id_pessoa, A.id_admin, P.nome_pessoa, L.username, L.senha, L.perfil
        FROM pessoa P, login L, admin A
        WHERE (P.id_pessoa = A.id_pessoa AND A.id_admin = L.id_admin) AND (L.username = '{u}' AND L.senha = '{s}')
        UNION
        SELECT P.id_pessoa, C.id_cliente, P.nome_pessoa, L.username, L.senha, L.perfil
        FROM pessoa P, login L, cliente C
        WHERE (P.id_pessoa = C.id_pessoa AND C.id_cliente = L.id_cliente) AND (L.username = '{u}' AND L.senha = '{s}')
    """
    with conn:
        cursor.execute(query)
        dados = cursor.fetchone()
        
        match dados[5]:
            case 'Administrador':
                id_admin = dados[1]
                nome = dados[2]
                primeiro_nome = dados[2].split()
                perfil = dados[5]
                lista_dados_admin = [id_admin, nome, primeiro_nome[0], perfil]
                return lista_dados_admin
            case 'Cliente':
                id_cliente = dados[1]
                nome = dados[2]
                primeiro_nome = dados[2].split()
                perfil = dados[5]
                lista_dados_cliente = [id_cliente, nome, primeiro_nome[0], perfil]
                return lista_dados_cliente


def pessoas_cadastradas():
    clear()
    query1 = """
        SELECT P.id_pessoa, P.nome_pessoa, L.perfil
        FROM pessoa P, login L, admin A
        WHERE A.id_pessoa = P.id_pessoa AND A.id_admin = L.id_admin
        UNION
        SELECT P. id_pessoa, P.nome_pessoa, L.perfil
        FROM pessoa P, login L, cliente C
        WHERE C.id_pessoa = P.id_pessoa AND C.id_cliente = L.id_cliente;
    """
    
    with conn:
        cursor.execute(query1)
        dados = cursor.fetchall()
        
    header1('PESSOAS CADASTRADAS')
    print(tabulate(dados, headers=["ID", "NOME", "PERFIL"], tablefmt="fancy_grid"))
    
    while True:
        opc = input('[1] - Visualização mais detalhada\n[2] - Apenas Administradores\n[3] - Apenas Clientes\n\n[4] - Sair\n\n-> ')
        
        match opc:
            
            case '1':
                clear()
                query2 = """
                    SELECT P.id_pessoa, P.nome_pessoa, P.dt_nasc_pessoa, L.username, L.senha, L.perfil, A.matricula, A.desde
                    FROM pessoa P, login L, admin A
                    WHERE P.id_pessoa = A.id_pessoa AND L.id_admin = A.id_admin
                    UNION
                    SELECT P.id_pessoa, P.nome_pessoa, P.dt_nasc_pessoa, L.username, L.senha, L.perfil, C.matricula, C.desde
                    FROM pessoa P, login L, cliente C
                    WHERE P.id_pessoa = C.id_pessoa AND L.id_cliente = C.id_cliente;
                """
                with conn:
                    cursor.execute(query2)
                    dados2 = cursor.fetchall()
                    
                header1('PESSOAS CADASTRADAS')
                print(tabulate(dados2, headers=["ID", "NOME", "DT NASCIMENTO", "LOGIN", "SENHA", "PERFIL", "MATRÍCULA", "DESDE"],tablefmt="fancy_grid"))
                
            case '2':
                clear()
                query3 = """
                    SELECT P.id_pessoa, P.nome_pessoa, L.username, L.senha, L.perfil, A.matricula, A.desde
                    FROM pessoa P, login L, admin A
                    WHERE P.id_pessoa = A.id_pessoa AND A.id_admin = L.id_admin
                """
                with conn:
                    cursor.execute(query3)
                    dados3 = cursor.fetchall() 
                header1('APENAS ADMINISTRADORES')
                print(tabulate(dados3, headers=["ID", "NOME", "LOGIN", "SENHA", "PERFIL", "MATRÍCULA", "DESDE"],tablefmt="fancy_grid"))
                
            case '3':
                clear()
                query4 = """
                SELECT P.id_pessoa, P.nome_pessoa, L.username, L.senha, L.perfil, C.matricula, C.desde
                FROM pessoa P, login L, cliente C
                WHERE P.id_pessoa = C.id_pessoa AND C.id_cliente = L.id_cliente
                """
                with conn:
                    cursor.execute(query4)
                    dados4 = cursor.fetchall()
                
                header1('APENAS CLIENTES')
                print(tabulate(dados4, headers=["ID", "NOME", "LOGIN", "SENHA", "PERFIL", "MATRÍCULA", "DESDE"],tablefmt="fancy_grid"))
            
            case '4':
                end_points('Saindo')
                break
        

def insert_produto(n, v, c, a, id_admin):
    valores = [n, v, c, a, id_admin]
    query = """
        INSERT INTO produto (nome_produto, valor_produto, categoria_produto, adicionado_por, id_admin)
        VALUES (?, ?, ?, ?, ?)
    """
    with conn:
        try:
            cursor.execute(query, valores)
        except Error as ex:
            print(ex)
        
        
def remover_produto(l, s):
    query_produtos = """
        SELECT id_produto, nome_produto, valor_produto, categoria_produto FROM produto
    """
    with conn:
        cursor.execute(query_produtos)
        produtos = cursor.fetchall()
    
    query_quant_produtos = """
        SELECT MAX(id_produto) FROM produto
    """
    with conn:
        cursor.execute(query_quant_produtos)
        quant = cursor.fetchone()[0]
        
    while True:
        header1('REMOVER PRODUTOS')
        print(tabulate(produtos, headers=["ID", "NOME PRODUTO", "PREÇO", "CATEGORIA"],tablefmt="fancy_grid"))
        try:
            opc = int(input('\n[0] - Voltar\nInforme o identificador do produto(ID) que deseja remover\n\n-> '))
        except ValueError:
            print('Inválido! Informe corretamente')
            sleep(1)
            clear()
            continue
        if opc == 0:
            end_points('Voltando')
            break
        elif opc > quant:
            print(f'Não existe produto com o id {opc}, informe novamente.')
            sleep(2)
            clear()
            continue
        else:
            while True:
                query_escolher_produto = f"""
                    SELECT nome_produto FROM produto WHERE id_produto = {opc}
                """
                with conn:
                    cursor.execute(query_escolher_produto)
                    try:
                        produto_escolhido = cursor.fetchone()[0]
                    except TypeError:
                        print('Esse id foi removido. Informe novamente.')
                        sleep(1)
                        clear()
                        break
                    
                dec = input(f'Tem certeza que quer remover o produto {produto_escolhido}? [S/N]: ').strip().upper()[0]
                match dec:
                    case 'S':
                        query_deletar_produto = f"""
                            DELETE FROM produto 
                            WHERE id_produto = {opc}
                        """
                        with conn:
                            cursor.execute(query_deletar_produto)
                            sleep(1)
                            print(f'O produto {produto_escolhido} removido ;(')
                            sleep(1)
                            cursor.execute(query_produtos)
                            produtos = cursor.fetchall()
                            clear()
                            break
                    case 'N':
                        clear()
                        break
                    case _:
                        print('Inválido! Informe corretamente!!')
                        continue
    
    


def produtos_cadastrados(l, s):
    query = """
        SELECT * FROM produto
    """
    with conn:
        try:
            cursor.execute(query)
            dados = cursor.fetchall()
            print(tabulate(dados, headers=["ID", "NOME PRODUTO", "PREÇO", "CATEGORIA", "ADICIONADO POR", "ID ADMIN"], tablefmt="fancy_grid"))
        except Error as ex:
            print(ex)

    while True:
        opc = input('\n[1] - Voltar\n\n-> ')
        
        match opc:
            case '1':
                clear()
                break
    

def loja(l, s):
    dados_cliente = pegar_dados(l, s)
    carrinho_cliente = []
    total = 0
    soma = 0
    total_sub = 0
    sub = 0
    id_pedido = 1
    total_compra = [['R$0,00']]
    query_produtos = """
        SELECT id_produto, nome_produto, valor_produto, categoria_produto FROM produto
    """
    with conn:
        cursor.execute(query_produtos)
        produtos = cursor.fetchall()
    
    while True:
        header1('PRODUTOS')
        print(tabulate(produtos, headers=["ID", "NOME PRODUTO", "PREÇO", "CATEGORIA"], tablefmt="psql"))
            
        print(tabulate(total_compra, headers=["TOTAL"], tablefmt="fancy_grid"))
        
        opc = input(f'\n\n[0] - Voltar\n\n[1] - Escolher Produto\n[2] - Ver Carrinho\n[3] - Ordenar\n\n[4] - Finalizar compra\n\n-> ').upper()
        
        match opc:
            case '0':
                end_points('Voltando')
                clear()
                break
            case '1':
              while True:
                    try:
                        opc2 = int(input('\nInforme o identificador(ID) do produto que deseja comprar:\n\n-> '))
                        query_produto_escolhido = f"""
                            SELECT id_produto, nome_produto, valor_produto FROM produto WHERE id_produto = {opc2}
                        """
                        with conn:
                            cursor.execute(query_produto_escolhido)
                            produto_escolhido = cursor.fetchone()
                            
                        quantidade = int(input(f'Informe a quantidade de {produto_escolhido[1]} que deseja comprar\n\n-> '))
                        
                        total = float(produto_escolhido[2].replace(',', '.')) * quantidade
                        soma += total
                        total_compra = [[f'{format_float(soma)}']]
                        dt_compra = datetime.today().strftime('%d-%m-%Y')
                        id_produto = produto_escolhido[0]
                        nome_produto = produto_escolhido[1]
                        valor_produto = produto_escolhido[2]
                        carrinho_cliente.append([id_pedido, id_produto, nome_produto, valor_produto, quantidade])
                        id_pedido += 1
                        print(f'{quantidade} {produto_escolhido[1]} comprado!')
                        end_points('Voltando')
                        clear()
                        break
                        
                    except TypeError:
                        print(f'O produto com o id {opc2} não existe. Informe novamente.')
                        sleep(1)
                        continue
              
            case '2':
                header2('CARRINHO')
                print(tabulate(carrinho_cliente, headers=["ID PEDIDO", "ID PRODUTO", "NOME PRODUTO", "VALOR PRODUTO", "QUANTIDADE"], tablefmt="fancy_grid"))
                opc_carrinho = input('\n[0] - Voltar\n\n[1] - Remover itens\n\n-> ')
                match opc_carrinho:
                    case '0':
                        end_points('Voltando')
                        clear()
                    case '1':
                        while True:
                            opc_remover = int(input('Informe o ID do pedido para remover ele do seu carrinho\n\n-> ')) - 1
                            
                            if opc_remover > len(carrinho_cliente):
                                print('Isso não consta no seu carrinho. Informe novamente.')
                                continue
                            else:
                                break
                        
                        total_sub = float(carrinho_cliente[opc_remover][3].replace(',', '.')) * carrinho_cliente[opc_remover][4]
                        soma -= total_sub
                        total_compra = [[f'{format_float(soma)}']]
                        print(f'Produto {carrinho_cliente[opc_remover][2]} removido!!')
                        carrinho_cliente.pop(opc_remover)
                        sleep(1)
                        end_points('Voltando')
                        clear()
                            
                            
                        
                        
                        
            case '3':
                query_itens = """
                    SELECT DISTINCT categoria_produto FROM produto
                """
                with conn:
                    cursor.execute(query_itens)
                    categorias = cursor.fetchall()
                    
                while True:
                    header2('ORDENAR')
                    opc3 = input('\n[0] - Voltar\n[1] - Ordenação Padrão\n[2] - Ordenar por categoria\n\n-> ').title()
                    
                    match opc3:
                        case '0':
                            end_points('Voltando')
                            break    
                        case '1':
                            query_produtos = """
                                SELECT id_produto, nome_produto, valor_produto, categoria_produto FROM produto
                                """
                            with conn:
                                cursor.execute(query_produtos)
                                produtos = cursor.fetchall()
                            clear()
                            break
                        case '2':
                                while True:
                                    print(tabulate(categorias, headers=["LISTA DE ITENS PARA ORDENAR"], tablefmt="fancy_grid"))
                                    opc4 = input('Informe um dos itens da lista para ordenar\n\n-> ').title()
                                    query_ordenar_itens = f"""
                                        SELECT id_produto, nome_produto, valor_produto, categoria_produto 
                                        FROM produto
                                        WHERE categoria_produto = '{opc4}';
                                    """
                                    with conn:
                                        cursor.execute(query_ordenar_itens)
                                        produtos = cursor.fetchall()
                                    
                                    clear()
                                    break
                    break
            case '4':
                pass
            case _:
                print('Inválido! Informe corretamente!!!')
                sleep(1)
                clear()
                continue





def validar_cadastro(u):
    query = f"""
        SELECT username FROM login 
        WHERE username = '{u}'
    """
    with conn:
        cursor.execute(query)
        dados = cursor.fetchone()
    
    if dados == None:
        return True
    else:
        return False        


