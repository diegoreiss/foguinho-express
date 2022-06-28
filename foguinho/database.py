from multiprocessing import connection
import sqlite3
from sqlite3 import Error
from tabulate import tabulate
from useful import *

def conexao():
    global conn, cursor
    try:
        conn = sqlite3.connect("foguinho/banco.db")
        cursor = conn.cursor()
    except Error as ex:
        print(ex)


conexao()


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
    print(f'{"ID":>3}{"NOME":>6}{"PERFIL":>26}')
    print(tabulate(dados, tablefmt="fancy_grid"))
    
    while True:
        opc = input('[1] - Visualização mais detalhada\n[2] - Apenas Administradores\n[3] - Apenas Clientes\n\n[4] - Sair\n-> ')
        
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
                print(f'{"ID":>3}{"NOME":>6}{"PERFIL":>53}')
                print(tabulate(dados2, tablefmt="fancy_grid"))
                
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
                print(tabulate(dados3, tablefmt="fancy_grid"))
                
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
                print(tabulate(dados4, tablefmt="fancy_grid"))
            
            case '4':
                end_points('Saindo')
                break
        

def insert_produto(n, v, c, a, id):
    valores = [n, v, c, a, id]
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
    query = """
        DELETE FROM produto 
        WHERE 
    """
    pass


def produtos_cadastrados(l, s):
    query = """
        SELECT * FROM produto
    """
    with conn:
        try:
            cursor.execute(query)
            dados = cursor.fetchall()
            print(tabulate(dados, tablefmt="fancy_grid"))
        except Error as ex:
            print(ex)

    while True:
        opc = input('\n[1] - Voltar\n\n-> ')
        
        match opc:
            case '1':
                clear()
                break
    
    

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


