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
        data_formatada = data_hora_obj.strftime('%d/%m/%Y')

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
        relatorio += f"{'ID':<5}{'Nome':<30}{'Qtd':>10}{'Preço':>10}{'Total':>10}{'Status':>10}\n"
        relatorio += "-" * 75 + "\n"
        total = 0

        for produto in produtos:
            status = "Ativo"
            if produto[4] == 0:
                status = "Inativo"

            relatorio += f"{produto[0]:<5}{produto[1]:<30}{produto[3]:>10}{produto[2]:>10.2f}{(produto[2]*produto[3]):>10.2f}{status:>10}\n"

            total = total + (produto[2] * produto[3])

        relatorio += "-" * 75 + "\n"
        linha = "." * 37
        relatorio += f"{'Total Estoque':<15}{linha:>37}{'R$':>3}{total:>10.2f}\n"

        self.text_relatorio.delete(1.0, tk.END)
        self.text_relatorio.insert(tk.END, relatorio)

    def gerar_relatorio_vendas(self):
        conexao = sqlite3.connect('estoque.db')
        cursor = conexao.cursor()
        cursor.execute('''
        SELECT vendas.id, produtos.nome, vendas.quantidade, vendas.total, vendas.data_venda, vendas.operacao
        FROM vendas 
        JOIN produtos ON vendas.produto_id = produtos.id
        ORDER BY vendas.data_venda
        ''')
        vendas = cursor.fetchall()
        conexao.close()

        relatorio = f"Relatório de Vendas - Gerado em {self.data_atual()}\n\n"
        relatorio += f"{'ID':<5}{'Produto':<30}{'Qtd':>15}{'Total':>10}{'Data':>25}\n"
        relatorio += "-" * 85 + "\n"
        total_venda = 0
        total_estorno = 0
        total = 0

        for venda in vendas:
            relatorio += f"{venda[0]:<5}{venda[1]:<30}{venda[2]:>15}{venda[3]:>10.2f}{self.converter_data(venda[4]):>25}\n"

            if venda[5] == "Venda":
                total_venda = total_venda + venda[3]
            else:
                total_estorno = total_estorno + venda[3]

        total = total_venda + total_estorno

        relatorio += "-" * 85 + "\n"
        linha = "." * 62
        relatorio += f"{'Vendas':<10}{linha:>62}{'R$':>3}{total_venda:>10.2f}\n"
        relatorio += f"{'Estornos':<10}{linha:>62}{'R$':>3}{total_estorno:>10.2f}\n"
        relatorio += f"{'Total':<10}{linha:>62}{'R$':>3}{total:>10.2f}\n"
        # relatorio += "-" * 85 + "\n"

        self.text_relatorio.delete(1.0, tk.END)
        self.text_relatorio.insert(tk.END, relatorio)

    def gerar_relatorio_compras(self):
        conexao = sqlite3.connect('estoque.db')
        cursor = conexao.cursor()
        cursor.execute('''
        SELECT compras.id, produtos.nome, compras.quantidade, compras.total, compras.data_compra, compras.operacao 
        FROM compras 
        JOIN produtos ON compras.produto_id = produtos.id
        ORDER BY compras.data_compra
        ''')
        compras = cursor.fetchall()
        conexao.close()

        relatorio = f"Relatório de Compras - Gerado em {self.data_atual()}\n\n"
        relatorio += f"{'ID':<5}{'Produto':<30}{'Qtd':>15}{'Total':>10}{'Data':>25}\n"
        relatorio += "-" * 85 + "\n"
        total_compra = 0
        total_estorno = 0
        total = 0

        for compra in compras:
            relatorio += f"{compra[0]:<5}{compra[1]:<30}{compra[2]:>15}{compra[3]:>10.2f}{self.converter_data(compra[4]):>25}\n"

            if compra[5] == "Compra":
                total_compra = total_compra + compra[3]
            else:
                total_estorno = total_estorno + compra[3]

        total = total_compra + total_estorno


        relatorio += "-" * 85 + "\n"
        linha = "." * 62
        relatorio += f"{'Compras':<10}{linha:>62}{'R$':>3}{total_compra:>10.2f}\n"
        relatorio += f"{'Estornos':<10}{linha:>62}{'R$':>3}{total_estorno:>10.2f}\n"
        relatorio += f"{'Total':<10}{linha:>62}{'R$':>3}{total:>10.2f}\n"

        self.text_relatorio.delete(1.0, tk.END)
        self.text_relatorio.insert(tk.END, relatorio)
