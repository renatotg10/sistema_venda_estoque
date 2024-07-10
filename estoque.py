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

        # self.label_quantidade = tk.Label(self.frame_produto, text="Quantidade:")
        # self.label_quantidade.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        # self.entry_quantidade = tk.Entry(self.frame_produto, width=10)  # Definindo largura do Entry
        # self.entry_quantidade.grid(row=2, column=1, padx=(0, 10), pady=5, sticky="ew")  # Ajustando padx para separação dos botões

        self.label_status = tk.Label(self.frame_produto, text="Status:")
        self.label_status.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.combobox_status = ttk.Combobox(self.frame_produto, values=["Ativo", "Inativo"])
        self.combobox_status.grid(row=3, column=1, padx=(0, 10), pady=5, sticky="ew")

        self.frame_botoes = tk.Frame(self)
        self.frame_botoes.pack(pady=10)

        self.button_adicionar = tk.Button(self.frame_botoes, text="Adicionar Produto", command=self.adicionar_produto)
        self.button_adicionar.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.button_editar = tk.Button(self.frame_botoes, text="Editar Produto", command=self.editar_produto)
        self.button_editar.grid(row=0, column=1, padx=5, pady=5)

        self.button_salvar = tk.Button(self.frame_botoes, text="Salvar Alterações", command=self.salvar_alteracoes)
        self.button_salvar.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        self.button_salvar["state"] = "disabled"

        # Configurar a coluna 1 do frame_produto para se redimensionar ao redor dos botões
        self.frame_produto.grid_columnconfigure(1, weight=1)

        self.tree_produtos = ttk.Treeview(self, columns=("ID", "Nome", "Preço", "Quantidade", "Status"), show="headings")
        self.tree_produtos.heading("ID", text="ID")
        self.tree_produtos.heading("Nome", text="Nome")
        self.tree_produtos.heading("Preço", text="Preço")
        self.tree_produtos.heading("Quantidade", text="Quantidade")
        self.tree_produtos.heading("Status", text="Status")
        self.tree_produtos.pack(pady=10, fill=tk.BOTH, expand=True)

        self.tree_produtos.column("ID", width=50, anchor="center")
        self.tree_produtos.column("Nome", width=150, anchor="w")
        self.tree_produtos.column("Preço", width=100, anchor="w")
        self.tree_produtos.column("Quantidade", width=100, anchor="center")
        self.tree_produtos.column("Status", width=100, anchor="center")

        self.carregar_produtos()

    def verificar_campos_preenchidos(self):
        nome = self.entry_nome.get().strip()
        preco = self.entry_preco.get().strip()
        status = self.combobox_status.get().strip()

        if not nome:
            messagebox.showerror("Erro", "O campo Nome é obrigatório.")
            return False
        if not preco:
            messagebox.showerror("Erro", "O campo Preço é obrigatório.")
            return False
        if not status:
            messagebox.showerror("Erro", "O campo Status é obrigatório.")
            return False

        try:
            float(preco)
        except ValueError:
            messagebox.showerror("Erro", "O campo Preço deve ser um número.")
            return False

        return True

    def adicionar_produto(self):
        if not self.verificar_campos_preenchidos():
            return
    
        nome = self.entry_nome.get()
        preco = float(self.entry_preco.get())
        # quantidade = int(self.entry_quantidade.get())
        quantidade = 0
        status = 1 if self.combobox_status.get() == "Ativo" else 0

        conexao = sqlite3.connect('estoque.db')
        cursor = conexao.cursor()
        cursor.execute('INSERT INTO produtos (nome, preco, quantidade, ativo) VALUES (?, ?, ?, ?)', (nome, preco, quantidade, status))
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
        # self.entry_quantidade.delete(0, tk.END)
        # self.entry_quantidade.insert(0, produto[3])
        self.combobox_status.set("Ativo" if produto[4] == "Ativo" else "Inativo")  # Atualizando o status do produto

        self.button_adicionar["state"] = "disabled"
        self.button_salvar["state"] = "normal"

    def salvar_alteracoes(self):
        if self.produto_id is None:
            return
        
        if not self.verificar_campos_preenchidos():
            return

        nome = self.entry_nome.get()
        preco = float(self.entry_preco.get())
        # quantidade = int(self.entry_quantidade.get())
        status = 1 if self.combobox_status.get() == "Ativo" else 0

        conexao = sqlite3.connect('estoque.db')
        cursor = conexao.cursor()
        # cursor.execute('UPDATE produtos SET nome = ?, preco = ?, quantidade = ?, ativo = ? WHERE id = ?', (nome, preco, quantidade, status, self.produto_id))
        cursor.execute('UPDATE produtos SET nome = ?, preco = ?, ativo = ? WHERE id = ?', (nome, preco, status, self.produto_id))
        conexao.commit()
        conexao.close()

        self.produto_id = None
        self.carregar_produtos()
        self.limpa_campos()

        messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")

    def limpa_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_preco.delete(0, tk.END)
        # self.entry_quantidade.delete(0, tk.END)
        self.combobox_status.set('')
        self.button_adicionar["state"] = "normal"
        self.button_salvar["state"] = "disabled"

    def carregar_produtos(self):
        for i in self.tree_produtos.get_children():
            self.tree_produtos.delete(i)

        conexao = sqlite3.connect('estoque.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT id, nome, preco, quantidade, ativo FROM produtos')
        produtos = cursor.fetchall()
        conexao.close()

        for produto in produtos:
            status = "Ativo" if produto[4] == 1 else "Inativo"
            self.tree_produtos.insert("", "end", values=(produto[0], produto[1], produto[2], produto[3], status))
