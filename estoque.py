import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

class GerenciamentoEstoque(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.produto_id = None  # Para rastrear o ID do produto que está sendo editado

    def create_widgets(self):
        self.label_titulo = tk.Label(self, text="Gerenciamento de Estoque")
        self.label_titulo.pack(pady=10)

        self.frame_produto = tk.Frame(self)
        self.frame_produto.pack(pady=10)

        self.label_nome = tk.Label(self.frame_produto, text="Nome:")
        self.label_nome.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_nome = tk.Entry(self.frame_produto, width=50)  # Definindo largura do Entry
        self.entry_nome.grid(row=0, column=1, padx=(0, 10), pady=5, sticky="ew")  # Ajustando padx para separação dos botões

        self.label_preco = tk.Label(self.frame_produto, text="Preço:")
        self.label_preco.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_preco = tk.Entry(self.frame_produto, width=20)  # Definindo largura do Entry
        self.entry_preco.grid(row=1, column=1, padx=(0, 10), pady=5, sticky="ew")  # Ajustando padx para separação dos botões

        self.label_quantidade = tk.Label(self.frame_produto, text="Quantidade:")
        self.label_quantidade.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_quantidade = tk.Entry(self.frame_produto, width=10)  # Definindo largura do Entry
        self.entry_quantidade.grid(row=2, column=1, padx=(0, 10), pady=5, sticky="ew")  # Ajustando padx para separação dos botões

        self.frame_botoes = tk.Frame(self)
        self.frame_botoes.pack(pady=10)

        self.button_adicionar = tk.Button(self.frame_botoes, text="Adicionar Produto", command=self.adicionar_produto)
        self.button_adicionar.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.button_editar = tk.Button(self.frame_botoes, text="Editar Produto", command=self.editar_produto)
        self.button_editar.grid(row=0, column=1, padx=5, pady=5)

        self.button_salvar = tk.Button(self.frame_botoes, text="Salvar Alterações", command=self.salvar_alteracoes)
        self.button_salvar.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        self.button_salvar["state"] = "disabled"

        self.button_excluir = tk.Button(self.frame_botoes, text="Excluir Produto", command=self.excluir_produto)
        self.button_excluir.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        self.button_excluidos = tk.Button(self.frame_botoes, text="Produtos Excluídos", command=self.listar_produtos_excluidos)
        self.button_excluidos.grid(row=0, column=4, padx=5, pady=5, sticky="ew")

        self.button_restaurar = tk.Button(self.frame_botoes, text="Restaurar Produto", command=self.restaurar_produto)
        self.button_restaurar.grid(row=0, column=5, padx=5, pady=5, sticky="ew")
        self.button_restaurar["state"] = "disabled"

        # Configurar a coluna 1 do frame_produto para se redimensionar ao redor dos botões
        self.frame_produto.grid_columnconfigure(1, weight=1)

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
        self.limpa_campos()
        messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")

    def editar_produto(self):
        selected_item = self.tree_produtos.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione um produto para editar!")
            return

        item = self.tree_produtos.item(selected_item)
        produto = item['values']
        self.produto_id = produto[0]

        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, produto[1])
        self.entry_preco.delete(0, tk.END)
        self.entry_preco.insert(0, produto[2])
        self.entry_quantidade.delete(0, tk.END)
        self.entry_quantidade.insert(0, produto[3])

        self.button_adicionar["state"] = "disabled"
        self.button_salvar["state"] = "normal"

    def salvar_alteracoes(self):
        if self.produto_id is None:
            return

        nome = self.entry_nome.get()
        preco = float(self.entry_preco.get())
        quantidade = int(self.entry_quantidade.get())

        conexao = sqlite3.connect('estoque_vendas.db')
        cursor = conexao.cursor()
        cursor.execute('UPDATE produtos SET nome = ?, preco = ?, quantidade = ? WHERE id = ?', (nome, preco, quantidade, self.produto_id))
        conexao.commit()
        conexao.close()

        self.produto_id = None
        self.carregar_produtos()
        self.limpa_campos()

        messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")

    def limpa_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_preco.delete(0, tk.END)
        self.entry_quantidade.delete(0, tk.END)
        self.button_adicionar["state"] = "normal"
        self.button_salvar["state"] = "disabled"

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

    def listar_produtos_excluidos(self):
        for i in self.tree_produtos.get_children():
            self.tree_produtos.delete(i)

        conexao = sqlite3.connect('estoque_vendas.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM produtos WHERE ativo = 0')
        produtos = cursor.fetchall()
        conexao.close()

        for produto in produtos:
            self.tree_produtos.insert("", "end", values=produto)

        self.button_restaurar["state"] = "normal"

    def restaurar_produto(self):
        selected_item = self.tree_produtos.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione um produto para restaurar!")
            return

        item = self.tree_produtos.item(selected_item)
        produto_id = item['values'][0]

        resposta = messagebox.askyesno("Confirmar Restauração", "Tem certeza que deseja restaurar este produto?")
        if resposta:
            conexao = sqlite3.connect('estoque_vendas.db')
            cursor = conexao.cursor()
            cursor.execute("UPDATE produtos SET ativo = 1 WHERE id = ?", (produto_id,))
            conexao.commit()
            conexao.close()

            self.carregar_produtos()
            self.button_restaurar["state"] = "disabled"
            messagebox.showinfo("Sucesso", "Produto resturado com sucesso!")