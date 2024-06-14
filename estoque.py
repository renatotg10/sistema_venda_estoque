import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

class GerenciamentoEstoque(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.label_titulo = tk.Label(self, text="Gerenciamento de Estoque")
        self.label_titulo.pack(pady=10)

        self.frame_produto = tk.Frame(self)
        self.frame_produto.pack(pady=10)

        self.label_nome = tk.Label(self.frame_produto, text="Nome:")
        self.label_nome.grid(row=0, column=0)
        self.entry_nome = tk.Entry(self.frame_produto)
        self.entry_nome.grid(row=0, column=1)

        self.label_preco = tk.Label(self.frame_produto, text="Preço:")
        self.label_preco.grid(row=1, column=0)
        self.entry_preco = tk.Entry(self.frame_produto)
        self.entry_preco.grid(row=1, column=1)

        self.label_quantidade = tk.Label(self.frame_produto, text="Quantidade:")
        self.label_quantidade.grid(row=2, column=0)
        self.entry_quantidade = tk.Entry(self.frame_produto)
        self.entry_quantidade.grid(row=2, column=1)

        self.button_adicionar = tk.Button(self.frame_produto, text="Adicionar Produto", command=self.adicionar_produto)
        self.button_adicionar.grid(row=3, columnspan=2, pady=5)

        self.button_excluir = tk.Button(self.frame_produto, text="Excluir Produto", command=self.excluir_produto)
        self.button_excluir.grid(row=4, columnspan=2, pady=5)

        self.tree_produtos = ttk.Treeview(self, columns=("ID", "Nome", "Preço", "Quantidade"), show="headings")
        self.tree_produtos.heading("ID", text="ID")
        self.tree_produtos.heading("Nome", text="Nome")
        self.tree_produtos.heading("Preço", text="Preço")
        self.tree_produtos.heading("Quantidade", text="Quantidade")
        self.tree_produtos.pack(pady=10)

        self.carregar_produtos()

    def adicionar_produto(self):
        nome = self.entry_nome.get()
        preco = float(self.entry_preco.get())
        quantidade = int(self.entry_quantidade.get())

        conexao = sqlite3.connect('estoque_vendas.db')
        cursor = conexao.cursor()
        cursor.execute('INSERT INTO produtos (nome, preco, quantidade, ativo) VALUES (?, ?, ?, 1)', (nome, preco, quantidade))
        conexao.commit()
        conexao.close()

        self.carregar_produtos()
        messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")

    def excluir_produto(self):
        selected_item = self.tree_produtos.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione um produto para excluir!")
            return

        item = self.tree_produtos.item(selected_item)
        produto_id = item['values'][0]

        resposta = messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir este produto?")
        if resposta:
            conexao = sqlite3.connect('estoque_vendas.db')
            cursor = conexao.cursor()
            cursor.execute("UPDATE produtos SET ativo = 0 WHERE id = ?", (produto_id,))
            conexao.commit()
            conexao.close()

            self.carregar_produtos()
            messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")

    def carregar_produtos(self):
        for i in self.tree_produtos.get_children():
            self.tree_produtos.delete(i)

        conexao = sqlite3.connect('estoque_vendas.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM produtos WHERE ativo = 1')
        produtos = cursor.fetchall()
        conexao.close()

        for produto in produtos:
            self.tree_produtos.insert("", "end", values=produto)
