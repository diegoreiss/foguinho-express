import sqlite3
from tabulate import tabulate
from random import randint
from datetime import date
from useful import * 


def database():
    global conn, cursor
    conn = sqlite3.connect('mercado.db')
    cursor = conn.cursor()




database()



#nome = input('Nome: ')
while True:
    dt_nasc = format_date(input('Data de Nascimento (dd-mm-aaaa): '))
    if len(dt_nasc) == 10:
        break
    else:
        print("Inválido! Informe corretamente! exemplo -> (dd-mm-aaaa)")

#email = input('Email: ')

print(dt_nasc)
# login_admin = input('login: ')
# senha_admin = input('senha: ')


# func_desde = date.today().strftime('%d-%m-%Y')
# mat_funcionario = randint(100000, 999999)



def insert_pessoa(n, d, e):
    valores = [n, d, e]
    with conn:
        try:
            query = """
                INSERT INTO Pessoas (
                    nome_pessoa,
                    dt_nasc_pessoa,
                    email_pessoa
                )
                VALUES (?, ?, ?)
            """
            cursor.execute(query, valores)
            print('Registro Inserido ;)')
        except sqlite3.Error as ex:
            print(ex)


def insert_admin():
    pass




#nsert_pessoa(nome, dt_nasc, email)