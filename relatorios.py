import tkinter as tk
import sqlite3
from datetime import datetime

class GeracaoRelatorios(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def converter_data(self, data_hora_str):
        # Converte a string para um objeto datetime
        data_hora_obj = datetime.strptime(data_hora_str, '%Y-%m-%d %H:%M:%S')

        # Formata o objeto datetime para o formato desejado
        data_formatada = data_hora_obj.strftime('%d/%m/%Y %H:%M:%S')

        return data_formatada
    
    def data_atual(self):
        # Obtém a data e hora atuais
        data_hora_atual = datetime.now()

        # Formata a data atual no formato desejado (dia/mês/ano)
        data_formatada = data_hora_atual.strftime('%d/%m/%Y às %H:%M')

        return data_formatada

    def create_widgets(self):
        self.label_titulo_relatorios = tk.Label(self, text="Relatórios")
        self.label_titulo_relatorios.pack(pady=10)

        self.frame_botoes = tk.Frame(self)
        self.frame_botoes.pack(pady=10)

        self.button_relatorio_estoque = tk.Button(self.frame_botoes, text="Relatório de Estoque", command=self.gerar_relatorio_estoque)
        self.button_relatorio_estoque.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.button_relatorio_vendas = tk.Button(self.frame_botoes, text="Relatório de Vendas", command=self.gerar_relatorio_vendas)
        self.button_relatorio_vendas.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.button_relatorio_compras = tk.Button(self.frame_botoes, text="Relatório de Compras", command=self.gerar_relatorio_compras)
        self.button_relatorio_compras.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        self.text_relatorio = tk.Text(self)
        self.text_relatorio.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def gerar_relatorio_estoque(self):
        conexao = sqlite3.connect('estoque.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM produtos WHERE produtos.ativo = 1')
        produtos = cursor.fetchall()
        conexao.close()

        relatorio = f"Relatório de Estoque - Gerado em {self.data_atual()}\n\n"
        relatorio += f"{'ID':<5}{'Nome':<30}{'Preço':>10}{'Qtd':>10}{'Status':>10}\n"
        relatorio += "-" * 65 + "\n"
        total = 0

        for produto in produtos:
            status = "Ativo"
            if produto[4] == 0:
                status = "Inativo"

            relatorio += f"{produto[0]:<5}{produto[1]:<30}{produto[2]:>10.2f}{produto[3]:>10}{status:>10}\n"

            total = total + produto[2]

        relatorio += "-" * 65 + "\n"
        relatorio += f"Total Estoque: R$ {total}\n"
        relatorio += "-" * 65 + "\n"
        self.text_relatorio.delete(1.0, tk.END)
        self.text_relatorio.insert(tk.END, relatorio)

    def gerar_relatorio_vendas(self):
        conexao = sqlite3.connect('estoque.db')
        cursor = conexao.cursor()
        cursor.execute('''
        SELECT vendas.id, produtos.nome, vendas.quantidade, vendas.total, vendas.data_venda 
        FROM vendas 
        JOIN produtos ON vendas.produto_id = produtos.id
        ''')
        vendas = cursor.fetchall()
        conexao.close()

        relatorio = f"Relatório de Vendas - Gerado em {self.data_atual()}\n\n"
        relatorio += f"{'ID':<5}{'Produto':<30}{'Quantidade':<15}{'Total':<10}{'Data':<20}\n"
        relatorio += "-" * 79 + "\n"

        for venda in vendas:
            relatorio += f"{venda[0]:<5}{venda[1]:<30}{venda[2]:<15}{venda[3]:<10}{self.converter_data(venda[4]):<20}\n"

        self.text_relatorio.delete(1.0, tk.END)
        self.text_relatorio.insert(tk.END, relatorio)

    def gerar_relatorio_compras(self):
        conexao = sqlite3.connect('estoque.db')
        cursor = conexao.cursor()
        cursor.execute('''
        SELECT compras.id, produtos.nome, compras.quantidade, compras.total, compras.data_compra 
        FROM compras 
        JOIN produtos ON compras.produto_id = produtos.id
        ''')
        compras = cursor.fetchall()
        conexao.close()

        relatorio = f"Relatório de Compras - Gerado em {self.data_atual()}\n\n"
        relatorio += f"{'ID':<5}{'Produto':<30}{'Quantidade':<15}{'Total':<10}{'Data':<20}\n"
        relatorio += "-" * 79 + "\n"

        for compra in compras:
            relatorio += f"{compra[0]:<5}{compra[1]:<30}{compra[2]:<15}{compra[3]:<10}{self.converter_data(compra[4]):<20}\n"

        self.text_relatorio.delete(1.0, tk.END)
        self.text_relatorio.insert(tk.END, relatorio)
