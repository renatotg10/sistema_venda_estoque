import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

class RegistroVendas(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.label_titulo_vendas = tk.Label(self, text="Registro de Vendas")
        self.label_titulo_vendas.pack(pady=10)

        self.frame_venda = tk.Frame(self)
        self.frame_venda.pack(pady=10)

        self.label_produto = tk.Label(self.frame_venda, text="Produto:")
        self.label_produto.grid(row=0, column=0)
        self.combo_produto = ttk.Combobox(self.frame_venda)
        self.combo_produto.grid(row=0, column=1)

        self.label_quantidade_venda = tk.Label(self.frame_venda, text="Quantidade:")
        self.label_quantidade_venda.grid(row=1, column=0)
        self.entry_quantidade_venda = tk.Entry(self.frame_venda)
        self.entry_quantidade_venda.grid(row=1, column=1)

        self.button_vender = tk.Button(self.frame_venda, text="Registrar Venda", command=self.registrar_venda)
        self.button_vender.grid(row=2, columnspan=2, pady=5)

        self.tree_vendas = ttk.Treeview(self, columns=("ID", "Produto", "Quantidade", "Total", "Data"), show="headings")
        self.tree_vendas.heading("ID", text="ID")
        self.tree_vendas.heading("Produto", text="Produto")
        self.tree_vendas.heading("Quantidade", text="Quantidade")
        self.tree_vendas.heading("Total", text="Total")
        self.tree_vendas.heading("Data", text="Data")
        self.tree_vendas.pack(pady=10)

        self.carregar_vendas()

    def carregar_produtos_venda(self):
        conexao = sqlite3.connect('estoque_vendas.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT id, nome FROM produtos')
        produtos = cursor.fetchall()
        conexao.close()

        self.combo_produto['values'] = [f"{produto[0]} - {produto[1]}" for produto in produtos]

    def registrar_venda(self):
        produto_selecionado = self.combo_produto.get()
        if not produto_selecionado:
            messagebox.showerror("Erro", "Selecione um produto!")
            return

        quantidade = self.entry_quantidade_venda.get()
        if not quantidade.isdigit():
            messagebox.showerror("Erro", "Digite uma quantidade válida!")
            return

        quantidade = int(quantidade)
        produto_id = int(produto_selecionado.split(" - ")[0])

        conexao = sqlite3.connect('estoque_vendas.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT preco, quantidade FROM produtos WHERE id = ?', (produto_id,))
        produto = cursor.fetchone()

        if quantidade > produto[1]:
            messagebox.showerror("Erro", "Quantidade em estoque insuficiente!")
            return

        total = produto[0] * quantidade
        nova_quantidade = produto[1] - quantidade

        cursor.execute('INSERT INTO vendas (produto_id, quantidade, total) VALUES (?, ?, ?)', (produto_id, quantidade, total))
        cursor.execute('UPDATE produtos SET quantidade = ? WHERE id = ?', (nova_quantidade, produto_id))
        conexao.commit()
        conexao.close()

        self.carregar_produtos_venda()
        self.carregar_vendas()
        messagebox.showinfo("Sucesso", "Venda registrada com sucesso!")

    def carregar_vendas(self):
        for i in self.tree_vendas.get_children():
            self.tree_vendas.delete(i)

        conexao = sqlite3.connect('estoque_vendas.db')
        cursor = conexao.cursor()
        cursor.execute('''
        SELECT vendas.id, produtos.nome, vendas.quantidade, vendas.total, vendas.data_venda 
        FROM vendas 
        JOIN produtos ON vendas.produto_id = produtos.id
        ''')
        vendas = cursor.fetchall()
        conexao.close()

        for venda in vendas:
            self.tree_vendas.insert("", "end", values=venda)

    def atualizar_combo_produto(self):
        self.carregar_produtos_venda()
