import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

class RegistroCompras(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def converter_data(self, data_hora_str):
        # Converte a string para um objeto datetime
        data_hora_obj = datetime.strptime(data_hora_str, '%Y-%m-%d %H:%M:%S')

        # Formata o objeto datetime para o formato desejado
        data_formatada = data_hora_obj.strftime('%d/%m/%Y')

        return data_formatada

    def create_widgets(self):
        self.label_titulo_compras = tk.Label(self, text="Registro de Compras")
        self.label_titulo_compras.pack(pady=10)

        self.frame_compra = tk.Frame(self)
        self.frame_compra.pack(pady=10)

        self.label_produto = tk.Label(self.frame_compra, text="Produto:")
        self.label_produto.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.combo_produto = ttk.Combobox(self.frame_compra, width=50)
        self.combo_produto.grid(row=0, column=1, padx=(0, 10), pady=5, sticky="ew")

        self.label_quantidade_compra = tk.Label(self.frame_compra, text="Quantidade:")
        self.label_quantidade_compra.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_quantidade_compra = tk.Entry(self.frame_compra, width=50)
        self.entry_quantidade_compra.grid(row=1, column=1, padx=(0, 10), pady=5, sticky="ew")

        self.label_operacao = tk.Label(self.frame_compra, text="Operação:")
        self.label_operacao.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.combo_operacao = ttk.Combobox(self.frame_compra, values=["Compra", "Estorno"])
        self.combo_operacao.grid(row=2, column=1, padx=(0, 10), pady=5, sticky="ew")

        self.label_observacao = tk.Label(self.frame_compra, text="Observação:")
        self.label_observacao.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.entry_observacao = tk.Entry(self.frame_compra, width=50)
        self.entry_observacao.grid(row=3, column=1, padx=(0, 10), pady=5, sticky="ew")

        self.frame_botoes = tk.Frame(self)
        self.frame_botoes.pack(pady=10)

        self.button_comprar = tk.Button(self.frame_botoes, text="Registrar Compra", command=self.registrar_compra)
        self.button_comprar.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Configurar a coluna 1 do frame_produto para se redimensionar ao redor dos botões
        self.frame_compra.grid_columnconfigure(1, weight=1)

        self.tree_compras = ttk.Treeview(self, columns=("ID", "Produto", "Quantidade", "Total", "Data", "Operacao", "Observacao"), show="headings")
        self.tree_compras.heading("ID", text="ID")
        self.tree_compras.heading("Produto", text="Produto")
        self.tree_compras.heading("Quantidade", text="Quantidade")
        self.tree_compras.heading("Total", text="Total")
        self.tree_compras.heading("Data", text="Data")
        self.tree_compras.heading("Operacao", text="Operação")
        self.tree_compras.heading("Observacao", text="Observação")
        self.tree_compras.pack(pady=10, fill=tk.BOTH, expand=True)

        self.tree_compras.column("ID", width=15, anchor="center")
        self.tree_compras.column("Produto", width=150, anchor="w")
        self.tree_compras.column("Quantidade", width=15, anchor="center")
        self.tree_compras.column("Total", width=40, anchor="e")
        self.tree_compras.column("Data", width=50, anchor="center")
        self.tree_compras.column("Operacao", width=50, anchor="w")
        self.tree_compras.column("Observacao", width=150, anchor="w")

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
        
        operacao = self.combo_operacao.get()
        if not operacao:
            messagebox.showerror("Erro", "Selecione uma operação!")
            return

        quantidade = int(quantidade)
        produto_id = int(produto_selecionado.split(" - ")[0])
        observacao = self.entry_observacao.get()

        conexao = sqlite3.connect('estoque.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT preco, quantidade FROM produtos WHERE id = ?', (produto_id,))
        produto = cursor.fetchone()

        total = produto[0] * quantidade
        nova_quantidade = produto[1] + quantidade
        mensagem = "Compra registrada com sucesso!"

        if operacao == "Estorno":
            nova_quantidade = produto[1] - quantidade
            mensagem = "Estorno registrado com sucesso!"

        cursor.execute('INSERT INTO compras (produto_id, operacao, quantidade, total, observacao) VALUES (?, ?, ?, ?, ?)', (produto_id, operacao, quantidade, total, observacao))
        cursor.execute('UPDATE produtos SET quantidade = ? WHERE id = ?', (nova_quantidade, produto_id))
        conexao.commit()
        conexao.close()

        self.carregar_produtos_compra()
        self.carregar_compras()
        self.limpa_campos()
        messagebox.showinfo("Sucesso", mensagem)

    def carregar_compras(self):
        for i in self.tree_compras.get_children():
            self.tree_compras.delete(i)

        conexao = sqlite3.connect('estoque.db')
        cursor = conexao.cursor()
        cursor.execute('''
        SELECT compras.id, produtos.nome, compras.quantidade, compras.total, compras.data_compra, compras.operacao, compras.observacao
        FROM compras 
        JOIN produtos ON compras.produto_id = produtos.id
        ''')
        compras = cursor.fetchall()
        conexao.close()

        for compra in compras:
            compra_id = compra[0]
            produto_nome = compra[1]
            quantidade = compra[2]
            total = compra[3]
            data_compra = self.converter_data(compra[4])
            operacao = compra[5]
            if compra[6]:
                observacao = compra[6]
            else:
                observacao = ""

            self.tree_compras.insert("", "end", values=(compra_id, produto_nome, quantidade, total, data_compra, operacao, observacao))

    def atualizar_combo_produto(self):
        self.carregar_produtos_compra()
        self.limpa_campos()

    def limpa_campos(self):
            self.entry_quantidade_compra.delete(0, tk.END)
            self.entry_observacao.delete(0, tk.END)
            self.combo_produto.set('')
            self.combo_operacao.set('')