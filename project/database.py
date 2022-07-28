import useful
import sqlite3
from sqlite3 import Error
from time import sleep

from tabulate import tabulate


def conexao():
    global conn, cursor
    try:
        conn = sqlite3.connect('marketDatabase.db')
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
            dt_cadastro DATE(10),
            id_pessoa INTEGER REFERENCES pessoa(id_pessoa)
        );
        
        CREATE TABLE IF NOT EXISTS admin(
            id_admin INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula VARCHAR(6),
            dt_cadastro DATE(10),
            id_pessoa INTEGER REFERENCES pessoa(id_pessoa)
        );
        
        CREATE TABLE IF NOT EXISTS login(
            id_login INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(60),
            senha VARCHAR(16),
            perfil VARCHAR(20),
            id_admin INTEGER REFERENCES admin(id_admin),
            id_cliente INTEGER REFERENCES cliente(id_cliente)
        );
        
        CREATE TABLE IF NOT EXISTS produto(
            id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_produto VARCHAR(60),
            valor_produto VARCHAR(10),
            categoria_produto VARCHAR(60)
        );
        
        CREATE TABLE IF NOT EXISTS produtos_cadastrados(
            id_admin INTEGER REFERENCES admin(id_admin),
            id_produto INTEGER REFERENCES produto(id_produto),
            adicionado_por VARCHAR(60),
            dt_cad_produto DATE(10)
        );
        
        CREATE TABLE IF NOT EXISTS produtos_vendidos(
            id_cliente INTEGER REFERENCES cliente(id_cliente),
            id_produto INTEGER REFERENCES produto(id_produto),
            quantidade VARCHAR(60),
            dt_compra DATE(10)
        );
    """
    with conn:
        try:
            cursor.executescript(create_tables)
        except Error as ex:
            print(ex)


def insert_pessoa(nome, data, email):
    dados_pessoa = [nome, data, email]
    query_insert_pessoa = """
        INSERT INTO pessoa(nome_pessoa, dt_nasc_pessoa, email_pessoa)
        VALUES(?, ?, ?)
    """
    with conn:
        try:
            cursor.execute(query_insert_pessoa, dados_pessoa)
        except Error as ex:
            print(ex)


def ultima_pessoa_cadastrada():
    query_ultima_pessoa_cadastrada = """
            SELECT MAX(id_pessoa) FROM pessoa
        """
    with conn:
        cursor.execute(query_ultima_pessoa_cadastrada)
        id_pessoa = cursor.fetchone()[0]

    return id_pessoa


def insert_admin(matricula, data_cadastro):
    id_pessoa = ultima_pessoa_cadastrada()

    dados_admin = [matricula, data_cadastro, id_pessoa]
    query_insert_admin = """
        INSERT INTO admin(matricula, dt_cadastro, id_pessoa)
        VALUES(?, ?, ?)
    """
    with conn:
        try:
            cursor.execute(query_insert_admin, dados_admin)
        except Error as ex:
            print(ex)


def insert_cliente(matricula, data_cadastro):
    id_pessoa = ultima_pessoa_cadastrada()

    dados_cliente = [matricula, data_cadastro, id_pessoa]
    query_insert_cliente = """
        INSERT INTO cliente(matricula, dt_cadastro, id_pessoa)
        VALUES(?, ?, ?)
    """
    with conn:
        try:
            cursor.execute(query_insert_cliente, dados_cliente)
        except Error as ex:
            print(ex)


def ultimo_admin_cadastrado():
    query_ultimo_admin_cadastrado = """
        SELECT MAX(id_admin) FROM admin
    """
    with conn:
        cursor.execute(query_ultimo_admin_cadastrado)
        id_admin = cursor.fetchone()[0]

    return id_admin


def ultimo_cliente_cadastrado():
    query_ultimo_cliente_cadastrado = """
        SELECT MAX(id_cliente) FROM cliente
    """
    with conn:
        cursor.execute(query_ultimo_cliente_cadastrado)
        id_cliente = cursor.fetchone()[0]

    return id_cliente


def insert_admin_login(username, password, perfil):
    id_admin = ultimo_admin_cadastrado()
    dados_login_admin = [username, password, perfil, id_admin]

    query_insert_admin_login = """
        INSERT INTO login(username, senha, perfil, id_admin)
        VALUES(?, ?, ?, ?)
    """
    with conn:
        try:
            cursor.execute(query_insert_admin_login, dados_login_admin)
        except Error as ex:
            print(ex)


def insert_cliente_login(username, password, perfil):
    id_cliente = ultimo_cliente_cadastrado()
    dados_login_cliente = [username, password, perfil, id_cliente]

    query_insert_cliente_login = """
        INSERT INTO login(username, senha, perfil, id_cliente)
        VALUES(?, ?, ?, ?)
    """
    with conn:
        try:
            cursor.execute(query_insert_cliente_login, dados_login_cliente)
        except Error as ex:
            print(ex)


def efetuar_login(username, senha):
    query_efetuar_login = f"""
        SELECT username, senha 
        FROM login
        WHERE username = '{username}' AND senha = '{senha}'
    """
    with conn:
        cursor.execute(query_efetuar_login)
        dado_encontrado = cursor.fetchone()

        if dado_encontrado is None:
            validacao = False
        else:
            validacao = True

    return validacao


def validar_email_cadastro(email):
    query_verificar_email_cadastrado = f"""
        SELECT email_pessoa
        FROM pessoa
        WHERE email_pessoa = '{email}'
    """
    with conn:
        cursor.execute(query_verificar_email_cadastrado)
        email_encontrado = cursor.fetchone()

        if email_encontrado is None:
            validacao = True
        else:
            validacao = False

    return validacao


def validar_username_cadastro(user):
    query_verificar_username_cadastrado = f"""
        SELECT username
        FROM login
        WHERE username = '{user}'
    """
    with conn:
        cursor.execute(query_verificar_username_cadastrado)
        username_encontrado = cursor.fetchone()

        if username_encontrado is None:
            validacao = True
        else:
            validacao = False

    return validacao


def validar_matricula_admin(mat):
    query_verificar_matricula_admin_cadastrado = f"""
        SELECT matricula
        FROM admin
        WHERE matricula = '{mat}'
    """
    with conn:
        cursor.execute(query_verificar_matricula_admin_cadastrado)
        matricula_admin_encontrada = cursor.fetchone()

        if matricula_admin_encontrada is None:
            validacao = True
        else:
            validacao = False

    return validacao


def validar_matricula_cliente(mat):
    query_verificar_matricula_cliente_cadastrado = f"""
        SELECT matricula
        FROM admin
        WHERE matricula = '{mat}'
    """
    with conn:
        cursor.execute(query_verificar_matricula_cliente_cadastrado)
        matricula_cliente_encontrada = cursor.fetchone()

        if matricula_cliente_encontrada is None:
            validacao = True
        else:
            validacao = False

    return validacao


def pegar_dados_login(username, senha):
    query_pegar_dados_login = f"""
        SELECT A.id_admin, P.nome_pessoa, L.perfil
        FROM admin A, pessoa P, login L
        WHERE (P.id_pessoa = A.id_pessoa AND A.id_admin = L.id_admin) AND (L.username = '{username}' AND L.senha = '{senha}')
        UNION
        SELECT C.id_cliente, P.nome_pessoa, L.perfil
        FROM cliente C, pessoa P, login L
        WHERE (P.id_pessoa = C.id_pessoa AND C.id_cliente = L.id_cliente) AND (L.username = '{username}' AND L.senha = '{senha}')
    """
    with conn:
        cursor.execute(query_pegar_dados_login)
        dados_usuario_logado = cursor.fetchone()

    return dados_usuario_logado


def validar_nome_produto(nome):
    query_verificar_produto_cadastrado = f"""
        SELECT nome_produto FROM produto
        WHERE nome_produto = '{nome}'
    """
    with conn:
        cursor.execute(query_verificar_produto_cadastrado)
        produto_encontrado = cursor.fetchone()

    if produto_encontrado is None:
        validacao = True
    else:
        validacao = False
    
    return validacao


def insert_produto(nome, valor, categoria):
    dados_cadastro_produto = [nome, valor, categoria]

    query_insert_produto = """
        INSERT INTO produto(nome_produto, valor_produto, categoria_produto)
        VALUES (?, ?, ?)
    """
    with conn:
        try:
            cursor.execute(query_insert_produto, dados_cadastro_produto)
        except Error as ex:
            print(ex)


def ultimo_produto_cadastrado():
    query_ultimo_produto_cadastrado = """
        SELECT MAX(id_produto) FROM produto
    """
    with conn:
        cursor.execute(query_ultimo_produto_cadastrado)
        id_produto = cursor.fetchone()[0]
    
    return id_produto


def insert_produtos_cadastrados(id_admin, id_produto, adicionado_por, dt_cad_produto):
    dados_insercao = [id_admin, id_produto, adicionado_por, dt_cad_produto] 
    query_insert_produtos_cadastrados = """
        INSERT INTO produtos_cadastrados(id_admin, id_produto, adicionado_por, dt_cad_produto)
        VALUES(?, ?, ?, ?)
    """
    with conn:
        try:
            cursor.execute(query_insert_produtos_cadastrados, dados_insercao)
        except Error as ex:
            print(ex)


def show_pessoas_cadastradas():
    query_pessoas_cadastradas = """
        SELECT P.id_pessoa, P.nome_pessoa, L.perfil
        FROM pessoa P, login L, admin A
        WHERE A.id_pessoa = P.id_pessoa AND A.id_admin = L.id_admin
        UNION
        SELECT P. id_pessoa, P.nome_pessoa, L.perfil
        FROM pessoa P, login L, cliente C
        WHERE C.id_pessoa = P.id_pessoa AND C.id_cliente = L.id_cliente;
    """
    with conn:
        cursor.execute(query_pessoas_cadastradas)
        pessoas_cadastradas = cursor.fetchall()

    print(tabulate(pessoas_cadastradas, headers=['ID', 'NOME', 'PERFIL'], tablefmt='fancy_grid'))


def show_detalhes_pessoas_cadastradas():
    query_detalhes_pessoas_cadastradas = """
        SELECT P.id_pessoa, P.nome_pessoa, P.dt_nasc_pessoa, L.username, L.senha, L.perfil, A.matricula, A.dt_cadastro
        FROM pessoa P, login L, admin A
        WHERE P.id_pessoa = A.id_pessoa AND L.id_admin = A.id_admin
        UNION
        SELECT P.id_pessoa, P.nome_pessoa, P.dt_nasc_pessoa, L.username, L.senha, L.perfil, C.matricula, C.dt_cadastro
        FROM pessoa P, login L, cliente C
        WHERE P.id_pessoa = C.id_pessoa AND L.id_cliente = C.id_cliente;
    """
    with conn:
        cursor.execute(query_detalhes_pessoas_cadastradas)
        dados_detalhados_pessoas = cursor.fetchall()

    print(tabulate(dados_detalhados_pessoas,
                   headers=["ID", "NOME", "DT NASCIMENTO", "LOGIN", "SENHA", "PERFIL", "MATRÍCULA", "DESDE"],
                   tablefmt="fancy_grid"))


def show_apenas_administradores():
    query_apenas_administradores = """
        SELECT P.id_pessoa, P.nome_pessoa, L.username, L.senha, L.perfil, A.matricula, A.dt_cadastro
        FROM pessoa P, login L, admin A
        WHERE P.id_pessoa = A.id_pessoa AND A.id_admin = L.id_admin
    """
    with conn:
        cursor.execute(query_apenas_administradores)
        apenas_administradores = cursor.fetchall()

    print(tabulate(apenas_administradores, headers=["ID", "NOME", "LOGIN", "SENHA", "PERFIL", "MATRÍCULA", "DESDE"],
                   tablefmt='fancy_grid'))


def show_apenas_clientes():
    query_apenas_clientes = """
        SELECT P.id_pessoa, P.nome_pessoa, L.username, L.senha, L.perfil, C.matricula, C.dt_cadastro
        FROM pessoa P, login L, cliente C
        WHERE P.id_pessoa = C.id_pessoa AND C.id_cliente = L.id_cliente
    """
    with conn:
        cursor.execute(query_apenas_clientes)
        apenas_clientes = cursor.fetchall()

    if len(apenas_clientes) == 0:
        return 0
    else:
        print(tabulate(apenas_clientes, headers=["ID", "NOME", "LOGIN", "SENHA", "PERFIL", "MATRÍCULA", "DT_CADASTRO"],
                       tablefmt='fancy_grid'))


def show_produtos_cadastrados():
    query_produtos_cadastrados = """
        SELECT id_produto , nome_produto, valor_produto, categoria_produto FROM produto
    """
    with conn:
        cursor.execute(query_produtos_cadastrados)
        produtos_cadastrados = cursor.fetchall()

    if len(produtos_cadastrados) == 0:
        produtos_cadastrados = 0
    else:
        produtos_cadastrados = tabulate(produtos_cadastrados, headers=['ID', 'NOME', 'VALOR', 'CATEGORIA'],
                       tablefmt='fancy_grid')
    
    return produtos_cadastrados


def show_produtos_e_quem_cadastrou():
    query_quem_cadastrou = """
        SELECT DISTINCT P.id_produto, P.nome_produto, P.valor_produto, P.categoria_produto, PC.adicionado_por, PC.dt_cad_produto 
        FROM produto P, produtos_cadastrados PC
        WHERE P.id_produto = PC.id_produto
    """
    with conn:
        cursor.execute(query_quem_cadastrou)
        registro = cursor.fetchall()
    
    print(tabulate(registro, 
                   headers=['ID', 'NOME', 'VALOR', 'CATEGORIA', 'ADICIONADO POR', 'DATA DO CADASTRO'], 
                   tablefmt='fancy_grid'))


def show_categorias():
    query_categorias = """
        SELECT DISTINCT categoria_produto FROM produto
    """
    with conn:
        cursor.execute(query_categorias)
        categorias = cursor.fetchall()
    
    print(tabulate(categorias, headers=['CATEGORIA'], tablefmt='psql'))
    

def ordenar_por_categoria_admin(nome):
    query_ordenar_categoria = f"""
        SELECT DISTINCT P.id_produto, P.nome_produto, P.valor_produto, P.categoria_produto, PC.adicionado_por, PC.dt_cad_produto 
        FROM produto P, produtos_cadastrados PC
        WHERE P.id_produto = PC.id_produto AND P.categoria_produto = '{nome}'
    """
    with conn:
        cursor.execute(query_ordenar_categoria)
        tabela_categoria_encontrada = cursor.fetchall()

    if len(tabela_categoria_encontrada) == 0:
        return 0
    else:
         print(tabulate(tabela_categoria_encontrada, 
                   headers=['ID', 'NOME', 'VALOR', 'CATEGORIA', 'ADICIONADO POR', 'DATA DO CADASTRO'], 
                   tablefmt='fancy_grid'))


def ordenar_por_categoria_cliente(nome):
    query_ordenar_categoria = f"""
        SELECT * FROM produto WHERE categoria_produto = '{nome}'
    """
    with conn:
        cursor.execute(query_ordenar_categoria)
        tabela_categoria_encontrada = cursor.fetchall()
    
    if len(tabela_categoria_encontrada) == 0:
        tabela_categoria_encontrada = 0
    else:
        tabela_categoria_encontrada = tabulate(tabela_categoria_encontrada, 
                                               headers=["ID", "NOME", "VALOR", "CATEGORIA"], 
                                               tablefmt="fancy_grid")
    
    return tabela_categoria_encontrada


def adicionar_produto_carrinho(identificador, quantidade):
    query_achar_produto = f"""
        SELECT * FROM produto WHERE id_produto = '{identificador}'
    """
    with conn:
        cursor.execute(query_achar_produto)
        produto_encontrado = cursor.fetchone()
    
    if produto_encontrado == None:
        produto_encontrado = None
    else:
        pass
    return produto_encontrado
    


        
def select_produto(num):
    query_select_produto = f"""
        SELECT nome_produto FROM produto
        WHERE id_produto = {num}
    """
    with conn:
        cursor.execute(query_select_produto)

        try:
            produto_encontrado = cursor.fetchone()[0]
        except TypeError:
            return None

    return produto_encontrado


def select_all_info_produto(num):
    query_select_all_info_produto = f"""
        SELECT * FROM produto WHERE id_produto = {num}
    """
    with conn:
        cursor.execute(query_select_all_info_produto)
        info_produto = cursor.fetchone()
    
    if info_produto == None:
        return None
    else:
        return info_produto
        

def delete_produto(id_produto):
    query_delete_produto = f"""
        DELETE FROM produto
        WHERE id_produto = {id_produto}
    """
    with conn:
        cursor.execute(query_delete_produto)
        

def informacoes_cliente_logado(dados):
    query_informacoes_cliente_logado = f"""
        SELECT P.nome_pessoa, L.username, L.senha, L.perfil, C.dt_cadastro, C.matricula
        FROM pessoa P, cliente C, login L
        WHERE (C.id_pessoa = P.id_pessoa AND C.id_cliente = L.id_cliente) AND C.id_cliente = {dados[0]}
    """
    with conn:
        cursor.execute(query_informacoes_cliente_logado)
        cliente_encontrado = cursor.fetchone()
    
    useful.header2(f'CLIENTE {dados[1].split()[0].upper()}')
    print(tabulate([cliente_encontrado], 
                   headers=['NOME', 'USERNAME', 'SENHA', 'PERFIL', 'DATA CADASTRO', 'MATRICULA'], 
                   tablefmt='fancy_grid'))


def insert_produtos_vendidos(dados, carrinho):
    id_cliente = dados[0]
    for produto in range(len(carrinho)):
        id_produto = carrinho[produto][0]
        quantidade = str(carrinho[produto][3])
        dt_compra = useful.date_today()
        lista_registro = [id_cliente, id_produto, quantidade, dt_compra]
        query_inserir_registro = """
            INSERT INTO produtos_vendidos(id_cliente, id_produto, quantidade, dt_compra)
            VALUES(?, ?, ?, ?)
        """
        with conn:
            try:
                cursor.execute(query_inserir_registro, lista_registro)
            except Error as ex:
                print(ex)


def ver_produtos_vendidos(dados):
    id_cliente = dados[0]
    query_produtos_vendidos = f"""
        SELECT PE.nome_pessoa, P.nome_produto, P.valor_produto, PV.quantidade, PV.dt_compra
        FROM pessoa PE, cliente C, produto P, produtos_vendidos PV
        WHERE (PE.id_pessoa = C.id_pessoa AND C.id_cliente = {id_cliente}) AND (PV.id_produto = P.id_produto AND C.id_cliente = PV.id_cliente)
    """
    with conn:
        try:
            cursor.execute(query_produtos_vendidos)
            produtos_vendidos = cursor.fetchall()
        except Error as ex:
            print(ex)
    
    return produtos_vendidos
        
