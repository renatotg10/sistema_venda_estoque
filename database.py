import sqlite3

def criar_banco_de_dados():
    conexao = sqlite3.connect('estoque.db')
    cursor = conexao.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco REAL NOT NULL,
        quantidade INTEGER NOT NULL,
        ativo INTEGER NOT NULL DEFAULT 1
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS compras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER,
        operacao TEXT NOT NULL,
        quantidade INTEGER,
        total REAL,
        observacao TEXT,
        data_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER,
        operacao TEXT NOT NULL,
        quantidade INTEGER,
        total REAL,
        observacao TEXT,
        data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
    ''')
    
    conexao.commit()
    conexao.close()


criar_banco_de_dados()
