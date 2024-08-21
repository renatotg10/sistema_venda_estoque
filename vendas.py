import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

class RegistroVendas(tk.Frame):
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
        self.label_titulo_vendas = tk.Label(self, text="Registro de Vendas")
        self.label_titulo_vendas.pack(pady=10)

        self.frame_venda = tk.Frame(self)
        self.frame_venda.pack(pady=10)

        self.label_produto = tk.Label(self.frame_venda, text="Produto:")
        self.label_produto.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.combo_produto = ttk.Combobox(self.frame_venda, width=50, state='readonly')
        self.combo_produto.grid(row=0, column=1, padx=(0, 10), pady=5, sticky="ew")
        self.combo_produto.bind("<<ComboboxSelected>>", self.atualizar_preco)

        self.label_preco_venda = tk.Label(self.frame_venda, text="Preço Unitário:")
        self.label_preco_venda.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_preco_venda = tk.Entry(self.frame_venda, width=50)
        self.entry_preco_venda.grid(row=1, column=1, padx=(0, 10), pady=5, sticky="ew")

        self.label_quantidade_venda = tk.Label(self.frame_venda, text="Quantidade:")
        self.label_quantidade_venda.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_quantidade_venda = tk.Entry(self.frame_venda, width=50)
        self.entry_quantidade_venda.grid(row=2, column=1, padx=(0, 10), pady=5, sticky="ew")

        self.label_operacao = tk.Label(self.frame_venda, text="Operação:")
        self.label_operacao.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.combo_operacao = ttk.Combobox(self.frame_venda, values=["Venda", "Estorno"], state='readonly')
        self.combo_operacao.grid(row=3, column=1, padx=(0, 10), pady=5, sticky="ew")

        self.label_observacao = tk.Label(self.frame_venda, text="Observação:")
        self.label_observacao.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.entry_observacao = tk.Entry(self.frame_venda, width=50)
        self.entry_observacao.grid(row=4, column=1, padx=(0, 10), pady=5, sticky="ew")

        self.frame_botoes = tk.Frame(self)
        self.frame_botoes.pack(pady=10)

        self.button_vendar = tk.Button(self.frame_botoes, text="Registrar Venda", command=self.registrar_venda)
        self.button_vendar.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Configurar a coluna 1 do frame_produto para se redimensionar ao redor dos botões
        self.frame_venda.grid_columnconfigure(1, weight=1)

        self.tree_vendas = ttk.Treeview(self, columns=("ID", "Produto", "Quantidade", "Preco", "Total", "Data", "Operacao", "Observacao"), show="headings")
        self.tree_vendas.heading("ID", text="ID")
        self.tree_vendas.heading("Produto", text="Produto")
        self.tree_vendas.heading("Quantidade", text="Qtd")
        self.tree_vendas.heading("Preco", text="Preço Unit.")
        self.tree_vendas.heading("Total", text="Total")
        self.tree_vendas.heading("Data", text="Data")
        self.tree_vendas.heading("Operacao", text="Operação")
        self.tree_vendas.heading("Observacao", text="Observação")
        self.tree_vendas.pack(pady=10, fill=tk.BOTH, expand=True)

        self.tree_vendas.column("ID", width=10, anchor="center")
        self.tree_vendas.column("Produto", width=150, anchor="w")
        self.tree_vendas.column("Quantidade", width=10, anchor="center")
        self.tree_vendas.column("Preco", width=30, anchor="e")
        self.tree_vendas.column("Total", width=40, anchor="e")
        self.tree_vendas.column("Data", width=50, anchor="center")
        self.tree_vendas.column("Operacao", width=50, anchor="w")
        self.tree_vendas.column("Observacao", width=150, anchor="w")

        self.carregar_vendas()

    def carregar_produtos_venda(self):
        conexao = sqlite3.connect('estoque.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT id, nome FROM produtos WHERE ativo = 1')
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
        
        operacao = self.combo_operacao.get()
        if not operacao:
            messagebox.showerror("Erro", "Selecione uma operação!")
            return

        preco = self.entry_preco_venda.get()
        if not preco:
            messagebox.showerror("Erro", "Digite o preço unitário.")
            return
        
        quantidade = int(quantidade)
        total = float(preco) * quantidade
        produto_id = int(produto_selecionado.split(" - ")[0])
        observacao = self.entry_observacao.get()

        conexao = sqlite3.connect('estoque.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT preco, quantidade FROM produtos WHERE id = ?', (produto_id,))
        produto = cursor.fetchone()

        if quantidade > produto[1] and operacao == "Venda":
            messagebox.showerror("Erro", "Quantidade em estoque insuficiente!")
            return

        nova_quantidade = produto[1] - quantidade
        mensagem = "Venda registrada com sucesso!"

        if operacao == "Estorno":
            total = total * -1
            nova_quantidade = produto[1] + quantidade
            mensagem = "Estorno registrado com sucesso!"

        cursor.execute('INSERT INTO vendas (produto_id, operacao, quantidade, preco, total, observacao) VALUES (?, ?, ?, ?, ?, ?)', (produto_id, operacao, quantidade, preco, total, observacao))
        cursor.execute('UPDATE produtos SET quantidade = ? WHERE id = ?', (nova_quantidade, produto_id))
        conexao.commit()
        conexao.close()

        self.carregar_produtos_venda()
        self.carregar_vendas()
        self.limpa_campos()
        messagebox.showinfo("Sucesso", mensagem)

    def carregar_vendas(self):
        for i in self.tree_vendas.get_children():
            self.tree_vendas.delete(i)

        # Data atual no formato YYYY-MM-DD
        data_atual = datetime.now().strftime('%Y-%m-%d')

        conexao = sqlite3.connect('estoque.db')
        cursor = conexao.cursor()
        cursor.execute('''
        SELECT vendas.id, produtos.nome, vendas.quantidade, vendas.preco, vendas.total, vendas.data_venda, vendas.operacao, vendas.observacao
        FROM vendas 
        JOIN produtos ON vendas.produto_id = produtos.id
        WHERE DATE(vendas.data_venda) = ?
        ''', (data_atual,))
        vendas = cursor.fetchall()
        conexao.close()

        for venda in vendas:
            venda_id = venda[0]
            produto_nome = venda[1]
            quantidade = venda[2]
            preco = venda[3]
            total = venda[4]
            data_venda = self.converter_data(venda[5])
            operacao = venda[6]
            if venda[7]:
                observacao = venda[7]
            else:
                observacao = ""

            self.tree_vendas.insert("", "end", values=(venda_id, produto_nome, quantidade, preco, total, data_venda, operacao, observacao))

    def atualizar_combo_produto(self):
        self.carregar_produtos_venda()
        self.limpa_campos()

    def limpa_campos(self):
            self.entry_quantidade_venda.delete(0, tk.END)
            self.entry_preco_venda.delete(0, tk.END)
            self.entry_observacao.delete(0, tk.END)
            self.combo_produto.set('')
            self.combo_operacao.set('')

    def atualizar_preco(self, event):
        produto_selecionado = self.combo_produto.get()
        if produto_selecionado:
            produto_id = int(produto_selecionado.split(" - ")[0])
            
            conexao = sqlite3.connect('estoque.db')
            cursor = conexao.cursor()
            cursor.execute('SELECT preco FROM produtos WHERE id = ?', (produto_id,))
            produto = cursor.fetchone()
            conexao.close()

            if produto:
                preco = produto[0]
                self.entry_preco_venda.config(state='normal')
                self.entry_preco_venda.delete(0, tk.END)
                self.entry_preco_venda.insert(0, f"{preco:.2f}")
