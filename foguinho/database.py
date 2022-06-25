import sqlite3
from sqlite3 import Error


def conexao():
    global conn, cursor
    try:
        conn = sqlite3.connect("foguinho/banco.db")
        cursor = conn.cursor()
    except Error as ex:
        print(ex)
    

def insert_pessoa():
    query = """
        INSERT INTO pessoa (nome_pessoa, dt_nasc_pessoa, email_pessoa)
        VALUES ('Diego Reis', '17-10-2002', 'diego@gmail.com')
    """
    with conn:
        try:
            cursor.execute()
        


def insert_admin():
    pass


def insert_cliente():
    pass


def validar_login():
    pass


def validar_cadastro():
    pass