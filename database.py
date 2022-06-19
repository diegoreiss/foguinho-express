import sqlite3
from tabulate import tabulate
from random import randint
from datetime import date
from useful import * 


def database_connection():
    global conn, cursor
    conn = sqlite3.connect("mercado.db")
    cursor = conn.cursor()


database_connection()


def tb_func():
    query = """
        CREATE TABLE IF NOT EXISTS Funcionario(
            id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT
          , nome_funcionario VARCHAR(60)
          , dt_nasc_funcionario DATE(10)
          , id_gerente FOREIGN KEY (id_gerente) REFERENCES
        );
    """
    with conn:
        try:
            cursor.execute(query)
            print('Registro func Inserido ;)')
        except sqlite3.Error as ex:
            print(ex)


def tb_gerente():
    query = """
        CREATE TABLE IF NOT EXISTS Gerente(
            id_gerente INTEGER PRIMARY KEY AUTOINCREMENT
          , percent_participaca_lucro INTEGER
          , tel_cel VARCHAR
          ) inherits(Funcionario)
    """
    with conn:
        try:
            cursor.execute(query)
            print('Registro gerente inserido ;)')
        except sqlite3.Error as ex:
            print(ex)
            
            
tb_func()
#tb_gerente()