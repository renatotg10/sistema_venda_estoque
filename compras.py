import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

class RegistroCompras(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.label_titulo_compras = tk.Label(self, text="Registro de Compras")
        self.label_titulo_compras.pack(pady=10)

        self.frame_compra = tk.Frame(self)
        self.frame_compra.pack(pady=10)

        self.label_produto = tk.Label(self.frame_compra, text="Produto:")
        self.label_produto.grid(row=0, column=0)
        self.combo_produto = ttk.Combobox(self.frame_compra)
        self.combo_produto.grid(row=0, column=1)

        self.label_quantidade_compra = tk.Label(self.frame_compra, text="Quantidade:")
        self.label_quantidade_compra.grid(row=1, column=0)
        self.entry_quantidade_compra = tk.Entry(self.frame_compra)
        self.entry_quantidade_compra.grid(row=1, column=1)

        self.button_vender = tk.Button(self.frame_compra, text="Registrar Compra", command=self.registrar_compra)
        self.button_vender.grid(row=2, columnspan=2, pady=5)

        self.tree_compras = ttk.Treeview(self, columns=("ID", "Produto", "Quantidade", "Total", "Data"), show="headings")
        self.tree_compras.heading("ID", text="ID")
        self.tree_compras.heading("Produto", text="Produto")
        self.tree_compras.heading("Quantidade", text="Quantidade")
        self.tree_compras.heading("Total", text="Total")
        self.tree_compras.heading("Data", text="Data")
        self.tree_compras.pack(pady=10)

        self.carregar_compras()

    def carregar_produtos_compra(self):
        conexao = sqlite3.connect('estoque.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT id, nome FROM produtos WHERE ativo = 1')
        produtos = cursor.fetchall()
        conexao.close()

        self.combo_produto['values'] = [f"{produto[0]} - {produto[1]}" for produto in produtos]

    def registrar_compra(self):
        produto_selecionado = self.combo_produto.get()
        if not produto_selecionado:
            messagebox.showerror("Erro", "Selecione um produto!")
            return

        quantidade = self.entry_quantidade_compra.get()
        if not quantidade.isdigit():
            messagebox.showerror("Erro", "Digite uma quantidade válida!")
            return

        quantidade = int(quantidade)
        produto_id = int(produto_selecionado.split(" - ")[0])

        conexao = sqlite3.connect('estoque.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT preco, quantidade FROM produtos WHERE id = ?', (produto_id,))
        produto = cursor.fetchone()

        if quantidade > produto[1]:
            messagebox.showerror("Erro", "Quantidade em estoque insuficiente!")
            return

        total = produto[0] * quantidade
        nova_quantidade = produto[1] + quantidade

        cursor.execute('INSERT INTO compras (produto_id, quantidade, total) VALUES (?, ?, ?)', (produto_id, quantidade, total))
        cursor.execute('UPDATE produtos SET quantidade = ? WHERE id = ?', (nova_quantidade, produto_id))
        conexao.commit()
        conexao.close()

        self.carregar_produtos_compra()
        self.carregar_compras()
        messagebox.showinfo("Sucesso", "Venda registrada com sucesso!")

    def carregar_compras(self):
        for i in self.tree_compras.get_children():
            self.tree_compras.delete(i)

        conexao = sqlite3.connect('estoque.db')
        cursor = conexao.cursor()
        cursor.execute('''
        SELECT compras.id, produtos.nome, compras.quantidade, compras.total, compras.data_compra 
        FROM compras 
        JOIN produtos ON compras.produto_id = produtos.id
        ''')
        compras = cursor.fetchall()
        conexao.close()

        for compra in compras:
            self.tree_compras.insert("", "end", values=compra)

    def atualizar_combo_produto(self):
        self.carregar_produtos_compra()
