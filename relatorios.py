import tkinter as tk
import sqlite3

class GeracaoRelatorios(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.label_titulo_relatorios = tk.Label(self, text="Relatórios")
        self.label_titulo_relatorios.pack(pady=10)

        self.button_relatorio_estoque = tk.Button(self, text="Relatório de Estoque", command=self.gerar_relatorio_estoque)
        self.button_relatorio_estoque.pack(pady=5)

        self.button_relatorio_vendas = tk.Button(self, text="Relatório de Vendas", command=self.gerar_relatorio_vendas)
        self.button_relatorio_vendas.pack(pady=5)

        self.text_relatorio = tk.Text(self)
        self.text_relatorio.pack(pady=10)

    def gerar_relatorio_estoque(self):
        conexao = sqlite3.connect('estoque_vendas.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM produtos')
        produtos = cursor.fetchall()
        conexao.close()

        relatorio = "Relatório de Estoque:\n\n"
        relatorio += f"{'ID':<5}{'Nome':<20}{'Preço':<10}{'Quantidade':<10}\n"
        relatorio += "-" * 50 + "\n"

        for produto in produtos:
            relatorio += f"{produto[0]:<5}{produto[1]:<20}{produto[2]:<10}{produto[3]:<10}\n"

        self.text_relatorio.delete(1.0, tk.END)
        self.text_relatorio.insert(tk.END, relatorio)

    def gerar_relatorio_vendas(self):
        conexao = sqlite3.connect('estoque_vendas.db')
        cursor = conexao.cursor()
        cursor.execute('''
        SELECT vendas.id, produtos.nome, vendas.quantidade, vendas.total, vendas.data_venda 
        FROM vendas 
        JOIN produtos ON vendas.produto_id = produtos.id
        ''')
        vendas = cursor.fetchall()
        conexao.close()

        relatorio = "Relatório de Vendas:\n\n"
        relatorio += f"{'ID':<5}{'Produto':<20}{'Quantidade':<10}{'Total':<10}{'Data':<20}\n"
        relatorio += "-" * 65 + "\n"

        for venda in vendas:
            relatorio += f"{venda[0]:<5}{venda[1]:<20}{venda[2]:<10}{venda[3]:<10}{venda[4]:<20}\n"

        self.text_relatorio.delete(1.0, tk.END)
        self.text_relatorio.insert(tk.END, relatorio)
