import sqlite3

def criar_banco_de_dados():
    conexao = sqlite3.connect('estoque_vendas.db')
    cursor = conexao.cursor()

    # Criação da tabela de produtos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco REAL NOT NULL,
        quantidade INTEGER NOT NULL
    )
    ''')

    # Criação da tabela de vendas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER,
        quantidade INTEGER NOT NULL,
        total REAL NOT NULL,
        data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
    ''')

    conexao.commit()
    conexao.close()

criar_banco_de_dados()
