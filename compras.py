from datetime import datetime
from tkinter import messagebox, ttk
import tkinter as tk
import sqlite3
import re

class RegistroCompras(tk.Frame):
    ajuste_quantidade = 0

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.id_compra_editando = None
        self.create_widgets()

    def converter_data(self, data_hora_str):
        # Converte a string para um objeto datetime
        data_hora_obj = datetime.strptime(data_hora_str, '%Y-%m-%d %H:%M:%S')

        # Formata o objeto datetime para o formato desejado
        data_formatada = data_hora_obj.strftime('%d/%m/%Y')

        return data_formatada
    
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
        self.label_titulo_compras = tk.Label(self, text="Registro de Compras")
        self.label_titulo_compras.pack(pady=10)

        self.frame_compra = tk.Frame(self)
        self.frame_compra.pack(pady=10)

        self.label_produto = tk.Label(self.frame_compra, text="Produto:")
        self.label_produto.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.combo_produto = ttk.Combobox(self.frame_compra, width=50, state='readonly')
        self.combo_produto.grid(row=0, column=1, padx=(0, 10), pady=5, sticky="ew")

        self.label_quantidade_compra = tk.Label(self.frame_compra, text="Quantidade:")
        self.label_quantidade_compra.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_quantidade_compra = tk.Entry(self.frame_compra, width=50)
        self.entry_quantidade_compra.grid(row=1, column=1, padx=(0, 10), pady=5, sticky="ew")

        self.label_total_compra = tk.Label(self.frame_compra, text="Valor Total:")
        self.label_total_compra.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_total_compra = tk.Entry(self.frame_compra, width=50)
        self.entry_total_compra.grid(row=2, column=1, padx=(0, 10), pady=5, sticky="ew")

        self.label_operacao = tk.Label(self.frame_compra, text="Operação:")
        self.label_operacao.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.combo_operacao = ttk.Combobox(self.frame_compra, values=["Compra", "Estorno"], state='readonly')
        self.combo_operacao.grid(row=3, column=1, padx=(0, 10), pady=5, sticky="ew")

        self.label_datacompra = tk.Label(self.frame_compra, text="Data Compra:")
        self.label_datacompra.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.entry_datacompra = tk.Entry(self.frame_compra, width=50)
        self.entry_datacompra.grid(row=4, column=1, padx=(0, 10), pady=5, sticky="ew")

        # Definir a data atual nos campos de entrada
        # data_atual = datetime.now().strftime("%d/%m/%Y")
        # self.entry_datacompra.insert(0, data_atual)

        self.label_observacao = tk.Label(self.frame_compra, text="Observação:")
        self.label_observacao.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.entry_observacao = tk.Entry(self.frame_compra, width=50)
        self.entry_observacao.grid(row=5, column=1, padx=(0, 10), pady=5, sticky="ew")

        # Criar o frame para os botões
        self.frame_botoes = tk.Frame(self)
        self.frame_botoes.pack(pady=10)

        # Botão Registrar Compra
        self.button_comprar = tk.Button(self.frame_botoes, text="Salvar", command=self.registrar_compra)
        self.button_comprar.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Botão Editar Compra
        self.button_editar = tk.Button(self.frame_botoes, text="Editar Compra", command=self.editar_compra)
        self.button_editar.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Botão Filtrar
        self.button_filtrar = tk.Button(self.frame_botoes, text="Filtrar", command=self.filtrar_compras)
        self.button_filtrar.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Configurar a coluna 1 do frame_produto para se redimensionar ao redor dos botões
        self.frame_compra.grid_columnconfigure(1, weight=1)

        self.tree_compras = ttk.Treeview(self, columns=("ID", "Produto", "Quantidade", "Preco", "Total", "Data", "Operacao", "Observacao"), show="headings")
        self.tree_compras.heading("ID", text="ID")
        self.tree_compras.heading("Produto", text="Produto")
        self.tree_compras.heading("Quantidade", text="Qtd")
        self.tree_compras.heading("Preco", text="Preço Unit.")
        self.tree_compras.heading("Total", text="Total")
        self.tree_compras.heading("Data", text="Data")
        self.tree_compras.heading("Operacao", text="Operação")
        self.tree_compras.heading("Observacao", text="Observação")
        self.tree_compras.pack(pady=10, fill=tk.BOTH, expand=True)

        self.tree_compras.column("ID", width=10, anchor="center")
        self.tree_compras.column("Produto", width=150, anchor="w")
        self.tree_compras.column("Quantidade", width=10, anchor="center")
        self.tree_compras.column("Preco", width=30, anchor="e")
        self.tree_compras.column("Total", width=40, anchor="e")
        self.tree_compras.column("Data", width=50, anchor="center")
        self.tree_compras.column("Operacao", width=50, anchor="w")
        self.tree_compras.column("Observacao", width=150, anchor="w")

        self.carregar_compras()

    def carregar_produtos_compra(self):
        conexao = sqlite3.connect('estoque.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT nome FROM produtos WHERE ativo = 1')
        produtos = cursor.fetchall()
        conexao.close()

        self.combo_produto['values'] = [f"{produto[0]}" for produto in produtos]

    def registrar_compra(self):
        global ajuste_quantidade
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

        total = self.entry_total_compra.get()
        if not total:
            messagebox.showerror("Erro", "Informe o valor total da compra.")
            return

        total = float(total)
        quantidade = int(quantidade)
        preco = total / quantidade
        produto_nome = produto_selecionado
        observacao = self.entry_observacao.get()
        datacompra = self.entry_datacompra.get()

        datacompra_valida = self.validar_data(datacompra)

        if not datacompra:
            messagebox.showerror("Erro", "Informe a data da compra.")
            return
        
        elif not datacompra_valida:
            messagebox.showerror("Erro", "Data da compra inválida. Informe o formato válido dd/mm/aaaa.")
            return

        conexao = sqlite3.connect('estoque.db')
        cursor = conexao.cursor()

        # Recuperar o ID do produto com base no nome selecionado
        cursor.execute('SELECT id FROM produtos WHERE nome = ?', (produto_nome,))
        produto = cursor.fetchone()

        produto_id = produto[0]
        
        if not produto_id:
            messagebox.showerror("Erro", "Produto não encontrado no banco de dados.")
            conexao.close()
            return

        if operacao == "Estorno":
            total = float(total) * -1

        if self.id_compra_editando:  # Se estiver editando uma compra
            # Atualiza a compra existente
            cursor.execute('''
                UPDATE compras
                SET produto_id = ?, operacao = ?, quantidade = ?, preco = ?, total = ?, observacao = ?, data_compra = ?
                WHERE id = ?
            ''', (produto_id, operacao, quantidade, preco, total, observacao, self.converter_datapadrao(datacompra), self.id_compra_editando))
            mensagem = "Compra atualizada com sucesso!"
            self.id_compra_editando = None  # Resetar a variável de controle
            quantidade = quantidade - int(ajuste_quantidade)
        else:
            # Inserir uma nova compra
            cursor.execute('INSERT INTO compras (produto_id, operacao, quantidade, preco, total, observacao, data_compra) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                        (produto_id, operacao, quantidade, preco, total, observacao, self.converter_datapadrao(datacompra)))
            mensagem = "Compra registrada com sucesso!"

        # Atualizar a quantidade no estoque
        cursor.execute('SELECT quantidade FROM produtos WHERE id = ?', (produto_id,))
        produto = cursor.fetchone()
        nova_quantidade = produto[0] + quantidade if operacao == "Compra" else produto[0] - quantidade
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

        # Data atual no formato YYYY-MM-DD
        data_atual = datetime.now().strftime('%Y-%m-%d')

        conexao = sqlite3.connect('estoque.db')
        cursor = conexao.cursor()
        cursor.execute('''
        SELECT compras.id, produtos.nome, compras.quantidade, compras.preco, compras.total, compras.data_compra, compras.operacao, compras.observacao
        FROM compras 
        JOIN produtos ON compras.produto_id = produtos.id
        WHERE DATE(compras.data_compra) = ?
        ''', (data_atual,))
        compras = cursor.fetchall()
        conexao.close()

        for compra in compras:
            compra_id = compra[0]
            produto_nome = compra[1]
            quantidade = compra[2]
            preco = compra[3]
            total = compra[4]
            data_compra = self.converter_data(compra[5])
            operacao = compra[6]
            observacao = compra[7] if compra[7] else ""

            self.tree_compras.insert("", "end", values=(compra_id, produto_nome, quantidade, preco, total, data_compra, operacao, observacao))

    def filtrar_compras(self):
        for i in self.tree_compras.get_children():
            self.tree_compras.delete(i)

        # Data atual no formato YYYY-MM-DD
        data = self.converter_data_en(self.entry_datacompra.get()) + '%'

        conexao = sqlite3.connect('estoque.db')
        cursor = conexao.cursor()
        cursor.execute('''
        SELECT compras.id, produtos.nome, compras.quantidade, compras.preco, compras.total, compras.data_compra, compras.operacao, compras.observacao
        FROM compras 
        JOIN produtos ON compras.produto_id = produtos.id
        WHERE DATE(compras.data_compra) like ?
        ''', (data,))
        compras = cursor.fetchall()
        conexao.close()

        for compra in compras:
            compra_id = compra[0]
            produto_nome = compra[1]
            quantidade = compra[2]
            preco = compra[3]
            total = compra[4]
            data_compra = self.converter_data(compra[5])
            operacao = compra[6]
            observacao = compra[7] if compra[7] else ""

            self.tree_compras.insert("", "end", values=(compra_id, produto_nome, quantidade, preco, total, data_compra, operacao, observacao))

    def atualizar_combo_produto(self):
        self.carregar_produtos_compra()
        self.limpa_campos()
        
        # Definir a data atual nos campos de entrada
        data_atual = datetime.now().strftime("%d/%m/%Y")
        self.entry_datacompra.delete(0, tk.END)
        self.entry_datacompra.insert(0, data_atual)

    def limpa_campos(self):
        self.entry_quantidade_compra.delete(0, tk.END)
        self.entry_total_compra.delete(0, tk.END)
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
                self.entry_total_compra.config(state='normal')
                self.entry_total_compra.delete(0, tk.END)
                self.entry_total_compra.insert(0, f"{preco:.2f}")


    def editar_compra(self):
        global ajuste_quantidade
        item_selecionado = self.tree_compras.selection()
        if not item_selecionado:
            messagebox.showerror("Erro", "Selecione uma compra para editar!")
            return

        compra = self.tree_compras.item(item_selecionado, "values")
        self.id_compra_editando = compra[0]  # Armazena o ID da compra sendo editada

        ajuste_quantidade = compra[2]

        # Preenche os campos com os dados da compra selecionada
        self.combo_produto.set(compra[1])
        self.entry_quantidade_compra.delete(0, tk.END)
        self.entry_quantidade_compra.insert(0, compra[2])
        self.entry_total_compra.delete(0, tk.END)
        
        if compra[6] == "Estorno":
            self.entry_total_compra.insert(0, float(compra[4]) * -1)
        else:
            self.entry_total_compra.insert(0, compra[4])

        self.combo_operacao.set(compra[6])
        self.entry_observacao.delete(0, tk.END)
        self.entry_observacao.insert(0, compra[7])