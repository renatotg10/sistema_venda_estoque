from datetime import datetime
from tkinter import messagebox, ttk
import tkinter as tk
import sqlite3
import re

class RegistroVendas(tk.Frame):
    ajuste_quantidade = 0
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.id_venda_editando = None  # Variável de controle para editar vendas
        self.create_widgets()

    def converter_data(self, data_hora_str):
        # Converte a string para um objeto datetime
        data_hora_obj = datetime.strptime(data_hora_str, '%Y-%m-%d %H:%M:%S')
        # Formata o objeto datetime para o formato desejado
        data_formatada = data_hora_obj.strftime('%d/%m/%Y')
        return data_formatada
    
    def converter_datapadrao(self, data):
        # Converte a string para um objeto datetime
        data_hora_obj = datetime.strptime(data, '%d/%m/%Y')

        # Formata o objeto datetime para o formato desejado
        data_formatada = data_hora_obj.strftime('%Y-%m-%d %H:%M:%S')

        return data_formatada

    def converter_data_en(self, data):
        # Converte a string para um objeto datetime
        data_hora_obj = datetime.strptime(data, '%d/%m/%Y')

        # Formata o objeto datetime para o formato desejado
        data_formatada = data_hora_obj.strftime('%Y-%m-%d')

        return data_formatada
    
    def validar_data(self, data):
        
        # Expressão regular para o formato dd/mm/aaaa
        padrao = re.compile(r'^\d{2}/\d{2}/\d{4}$')

        # Verifica se a data corresponde ao padrão
        if not padrao.match(data):
            # messagebox.showerror("Erro de Validação", "A data deve estar no formato dd/mm/aaaa.")
            return False
        
        # Verificar se os valores de dia, mês e ano são válidos
        try:
            dia, mes, ano = map(int, data.split('/'))
            if not (1 <= dia <= 31 and 1 <= mes <= 12 and ano > 0):
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro de Validação", "Data inválida.")
            return False
        
        return True

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

        self.label_datavenda = tk.Label(self.frame_venda, text="Data Venda:")
        self.label_datavenda.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.entry_datavenda = tk.Entry(self.frame_venda, width=50)
        self.entry_datavenda.grid(row=4, column=1, padx=(0, 10), pady=5, sticky="ew")

        # Definir a data atual nos campos de entrada
        # data_atual = datetime.now().strftime("%d/%m/%Y")
        # self.entry_datavenda.insert(0, data_atual)

        self.label_observacao = tk.Label(self.frame_venda, text="Observação:")
        self.label_observacao.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.entry_observacao = tk.Entry(self.frame_venda, width=50)
        self.entry_observacao.grid(row=5, column=1, padx=(0, 10), pady=5, sticky="ew")

        # Criar o frame para os botões
        self.frame_botoes = tk.Frame(self)
        self.frame_botoes.pack(pady=10)

        # Botão Registrar Venda
        self.button_vendar = tk.Button(self.frame_botoes, text="Salvar", command=self.registrar_venda)
        self.button_vendar.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Botão Editar Venda
        self.button_editar = tk.Button(self.frame_botoes, text="Editar Venda", command=self.editar_venda)
        self.button_editar.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Botão Filtrar
        self.button_filtrar = tk.Button(self.frame_botoes, text="Filtrar", command=self.filtrar_vendas)
        self.button_filtrar.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

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
        cursor.execute('SELECT nome FROM produtos WHERE ativo = 1')
        produtos = cursor.fetchall()
        conexao.close()

        self.combo_produto['values'] = [f"{produto[0]}" for produto in produtos]

    def registrar_venda(self):
        global ajuste_quantidade
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
        produto_nome = produto_selecionado  # Usando o nome do produto diretamente
        observacao = self.entry_observacao.get()
        datavenda = self.entry_datavenda.get()

        datavenda_valida = self.validar_data(datavenda)

        if not datavenda:
            messagebox.showerror("Erro", "Informe a data da venda.")
            return
        
        elif not datavenda_valida:
            messagebox.showerror("Erro", "Data da venda inválida. Informe o formato válido dd/mm/aaaa.")
            return

        conexao = sqlite3.connect('estoque.db')
        cursor = conexao.cursor()

        # Recuperar o ID do produto com base no nome selecionado
        cursor.execute('SELECT id, quantidade FROM produtos WHERE nome = ?', (produto_nome,))
        produto = cursor.fetchone()
        
        produto_id = produto[0]
        quantidade_prod = int(produto[1])
        
        if not produto_id:
            messagebox.showerror("Erro", "Produto não encontrado no banco de dados.")
            conexao.close()
            return

        if quantidade > quantidade_prod and operacao == "Venda":
            messagebox.showerror("Erro", "Quantidade em estoque insuficiente!")
            conexao.close()
            return
        
        if operacao == "Estorno":
            total = float(total) * -1

        if self.id_venda_editando:  # Se estiver editando uma venda
            # Atualiza a venda existente
            cursor.execute('''
                UPDATE vendas
                SET produto_id = ?, operacao = ?, quantidade = ?, preco = ?, total = ?, observacao = ?, data_venda = ?
                WHERE id = ?
            ''', (produto_id, operacao, quantidade, preco, total, observacao, self.converter_datapadrao(datavenda), self.id_venda_editando))
            mensagem = "Venda atualizada com sucesso!"
            self.id_venda_editando = None  # Resetar a variável de controle
            quantidade = quantidade - int(ajuste_quantidade)
        else:
            # Inserir uma nova venda
            cursor.execute('INSERT INTO vendas (produto_id, operacao, quantidade, preco, total, observacao, data_venda) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                        (produto_id, operacao, quantidade, preco, total, observacao, self.converter_datapadrao(datavenda)))
            mensagem = "Venda registrada com sucesso!"

        # Atualizar a quantidade no estoque
        cursor.execute('SELECT quantidade FROM produtos WHERE id = ?', (produto_id,))
        produto = cursor.fetchone()
        nova_quantidade = produto[0] - quantidade if operacao == "Venda" else produto[0] + quantidade
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
            observacao = venda[7] if venda[7] else ""

            self.tree_vendas.insert("", "end", values=(venda_id, produto_nome, quantidade, preco, total, data_venda, operacao, observacao))

    def filtrar_vendas(self):
        for i in self.tree_vendas.get_children():
            self.tree_vendas.delete(i)

        # Data atual no formato YYYY-MM-DD
        data = self.converter_data_en(self.entry_datavenda.get()) + '%'

        conexao = sqlite3.connect('estoque.db')
        cursor = conexao.cursor()
        cursor.execute('''
        SELECT vendas.id, produtos.nome, vendas.quantidade, vendas.preco, vendas.total, vendas.data_venda, vendas.operacao, vendas.observacao
        FROM vendas 
        JOIN produtos ON vendas.produto_id = produtos.id
        WHERE DATE(vendas.data_venda) like ?
        ''', (data,))
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
            observacao = venda[7] if venda[7] else ""

            self.tree_vendas.insert("", "end", values=(venda_id, produto_nome, quantidade, preco, total, data_venda, operacao, observacao))

    def atualizar_combo_produto(self):
        self.carregar_produtos_venda()
        self.limpa_campos()

        # Definir a data atual nos campos de entrada
        data_atual = datetime.now().strftime("%d/%m/%Y")
        self.entry_datavenda.delete(0, tk.END)
        self.entry_datavenda.insert(0, data_atual)

    def limpa_campos(self):
        self.entry_quantidade_venda.delete(0, tk.END)
        self.entry_preco_venda.delete(0, tk.END)
        self.entry_observacao.delete(0, tk.END)        
        self.combo_produto.set('')
        self.combo_operacao.set('')

    def atualizar_preco(self, event):
        produto_selecionado = self.combo_produto.get()
        if produto_selecionado:
            conexao = sqlite3.connect('estoque.db')
            cursor = conexao.cursor()

            # Recuperar o preço do produto com base no nome selecionado
            cursor.execute('SELECT preco FROM produtos WHERE nome = ?', (produto_selecionado,))
            produto = cursor.fetchone()
            conexao.close()

            if produto:
                preco = produto[0]
                self.entry_preco_venda.config(state='normal')
                self.entry_preco_venda.delete(0, tk.END)
                self.entry_preco_venda.insert(0, f"{preco:.2f}")


    def editar_venda(self):
        global ajuste_quantidade
        item_selecionado = self.tree_vendas.selection()
        if not item_selecionado:
            messagebox.showerror("Erro", "Selecione uma venda para editar!")
            return

        venda = self.tree_vendas.item(item_selecionado, "values")
        self.id_venda_editando = venda[0]  # Armazena o ID da venda sendo editada

        ajuste_quantidade = venda[2]

        # Preenche os campos com os dados da venda selecionada
        self.combo_produto.set(venda[1])
        self.entry_quantidade_venda.delete(0, tk.END)
        self.entry_quantidade_venda.insert(0, venda[2])
        self.entry_preco_venda.delete(0, tk.END)
        self.entry_preco_venda.insert(0, venda[3])
        self.combo_operacao.set(venda[6])
        self.entry_observacao.delete(0, tk.END)
        self.entry_observacao.insert(0, venda[7])

