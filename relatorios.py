from tkinter import messagebox
from tkinter import filedialog
from datetime import datetime
import tkinter as tk
import sqlite3
import re


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
    
    def converter_datapadrao(self, data):
        # Converte a string para um objeto datetime
        data_hora_obj = datetime.strptime(data, '%d/%m/%Y')

        # Formata o objeto datetime para o formato desejado
        data_formatada = data_hora_obj.strftime('%Y-%m-%d')

        return data_formatada
    
    def data_atual(self):
        # Obtém a data e hora atuais
        data_hora_atual = datetime.now()

        # Formata a data atual no formato desejado (dia/mês/ano)
        data_formatada = data_hora_atual.strftime('%d/%m/%Y às %H:%M')

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

        self.button_gerar_txt = tk.Button(self.frame_botoes, text="Salvar Relatório", command=self.salvar_relatorio)
        self.button_gerar_txt.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        self.label_periodo = tk.Label(self, text="Informe o Período para Consulta das Compras e Vendas")
        self.label_periodo.pack(pady=2)

        self.frame_opcoes = tk.Frame(self)
        self.frame_opcoes.pack(pady=5)

        self.label_datainicial = tk.Label(self.frame_opcoes, text="Data Inicial:")
        self.label_datainicial.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_datainicial = tk.Entry(self.frame_opcoes, width=15)
        self.entry_datainicial.grid(row=0, column=1, padx=(0, 10), pady=5, sticky="ew")

        self.label_datafinal = tk.Label(self.frame_opcoes, text="Data Final:")
        self.label_datafinal.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.entry_datafinal = tk.Entry(self.frame_opcoes, width=15)
        self.entry_datafinal.grid(row=0, column=3, padx=(0, 10), pady=5, sticky="ew")

        # Definir a data atual nos campos de entrada
        data_atual = datetime.now().strftime("%d/%m/%Y")
        self.entry_datainicial.insert(0, data_atual)
        self.entry_datafinal.insert(0, data_atual)


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
        self.text_relatorio.delete(1.0, tk.END)

        data_inicial = self.entry_datainicial.get()
        data_final = self.entry_datafinal.get()
        datainicial_valida = self.validar_data(data_inicial)
        datafinal_valida = self.validar_data(data_final)

        if not data_inicial or not data_final:
            messagebox.showerror("Erro", "Informe a data inicial e final.")
            return
        
        elif not datainicial_valida:
            messagebox.showerror("Erro", "Data Inicial Inválida. Informe o formato válido dd/mm/aaaa.")
            return
        
        elif not datafinal_valida:
            messagebox.showerror("Erro", "Data Final Inválida. Informe o formato válido dd/mm/aaaa.")
            return

        if datainicial_valida and datafinal_valida:
            conexao = sqlite3.connect('estoque.db')
            cursor = conexao.cursor()
            cursor.execute('''
            SELECT vendas.id, produtos.nome, vendas.quantidade, vendas.total, vendas.data_venda, vendas.operacao
            FROM vendas 
            JOIN produtos ON vendas.produto_id = produtos.id
            WHERE DATE(vendas.data_venda) BETWEEN ? AND ?
            ORDER BY vendas.data_venda
            ''', (self.converter_datapadrao(data_inicial), self.converter_datapadrao(data_final)))
            vendas = cursor.fetchall()
            conexao.close()

            relatorio = f"Relatório de Vendas - Gerado em {self.data_atual()}\n\n"
            relatorio += f"Período de {data_inicial} à {data_final}\n\n"
            relatorio += f"{'Data':<12}{'Produto':<48}{'Qtd':>4}{'Total':>12}{'Operação':>9}\n"
            relatorio += "-" * 85 + "\n"
            total_venda = 0
            total_estorno = 0
            total = 0

            for venda in vendas:
                relatorio += f"{self.converter_data(venda[4]):<12}{venda[1]:<48}{venda[2]:>4}{venda[3]:>12.2f}{venda[5]:>9}\n"

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

            self.text_relatorio.insert(tk.END, relatorio)

    def gerar_relatorio_compras(self):
        self.text_relatorio.delete(1.0, tk.END)

        data_inicial = self.entry_datainicial.get()
        data_final = self.entry_datafinal.get()
        datainicial_valida = self.validar_data(data_inicial)        
        datafinal_valida = self.validar_data(data_final)

        if not data_inicial or not data_final:
            messagebox.showerror("Erro", "Informe a data inicial e final.")
            return
        
        elif not datainicial_valida:
            messagebox.showerror("Erro", "Data Inicial Inválida. Informe o formato válido dd/mm/aaaa.")
            return
        
        elif not datafinal_valida:
            messagebox.showerror("Erro", "Data Final Inválida. Informe o formato válido dd/mm/aaaa.")
            return

        if datainicial_valida and datafinal_valida:
            conexao = sqlite3.connect('estoque.db')
            cursor = conexao.cursor()
            cursor.execute('''
            SELECT compras.id, produtos.nome, compras.quantidade, compras.total, compras.data_compra, compras.operacao 
            FROM compras 
            JOIN produtos ON compras.produto_id = produtos.id
            WHERE DATE(compras.data_compra) BETWEEN ? AND ?
            ORDER BY compras.data_compra
            ''', (self.converter_datapadrao(data_inicial), self.converter_datapadrao(data_final)))
            compras = cursor.fetchall()
            conexao.close()

            relatorio = f"Relatório de Compras - Gerado em {self.data_atual()}\n\n"
            relatorio += f"Período de {data_inicial} à {data_final}\n\n"
            relatorio += f"{'Data':<12}{'Produto':<48}{'Qtd':>4}{'Total':>12}{'Operação':>9}\n"
            relatorio += "-" * 85 + "\n"
            total_compra = 0
            total_estorno = 0
            total = 0

            for compra in compras:
                relatorio += f"{self.converter_data(compra[4]):<12}{compra[1]:<48}{compra[2]:>4}{compra[3]:>12.2f}{compra[5]:>9}\n"

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

            self.text_relatorio.insert(tk.END, relatorio)

    def salvar_relatorio(self):
        # Gerando um nome padrão de arquivo com base na data e hora atuais
        nome_padrao = f"relatorio_estoque_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Abrir a janela de diálogo "Salvar como" com o nome padrão preenchido
        nome_arquivo = filedialog.asksaveasfilename(
            defaultextension=".txt", 
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=nome_padrao  # Nome do arquivo padrão
        )

        # Verifica se um nome de arquivo foi selecionado
        if nome_arquivo:
            # Salvando o conteúdo do relatório no arquivo escolhido pelo usuário
            with open(nome_arquivo, 'w', encoding='utf-8') as file:
                file.write(self.text_relatorio.get(1.0, tk.END))

            print(f"Relatório salvo como: {nome_arquivo}")