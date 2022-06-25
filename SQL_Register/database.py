import sqlite3


def Database(): 
    global conn, cursor
    conn = sqlite3.connect("SQL_Register/cadastro.db") # Conexão com o banco de dados
    with conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS `usuarios` (id_usuarios INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, nomeUsuario TEXT, senha TEXT)") # Cria uma tabela


def insert(n, s): # Adicionando valores a tabela
    valores = [n, s]
    with conn:
        query = ("INSERT INTO `usuarios` (nomeUsuario, senha) VALUES (?, ?)")
        cursor.execute(query, valores)


def view(): # Mostra os conteúdos da tabela
    print('-' * 50)
    print ("{:<8} {:<15} {:<10}".format('id','nomeUsuario','senha'))
    print('-' * 50)
    with conn:
        cursor.execute("SELECT * FROM `usuarios`")
        data = cursor.fetchall()
        for i in range(len(data)):
            identificador = data[i][0]
            nomeUsuario = data[i][1]
            senha = data[i][2]
            print ("{:<8} {:<15} {:<10}".format(identificador, nomeUsuario, senha))
    print('=' * 50)
    

def validate():
    while True:
        nome = input('Nome de Usuário: ')
        senha = input('Senha: ')
        valores = [nome, senha]
        while True:
            with conn:
                cursor.execute("SELECT * FROM `usuarios` WHERE nomeUsuario=? and senha=?", valores)

            if cursor.fetchone() == None:
                result = False
            else:
                result = True
            break
        
        if result == True:
            print('Login efetuado com sucesso!')
            break
        else:
            print('Nome de Usuário ou senhas incorretas. Informe novamente.')
            continue