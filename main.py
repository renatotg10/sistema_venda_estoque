import tkinter as tk
from tkinter import ttk
from database import criar_banco_de_dados
from estoque import GerenciamentoEstoque
from vendas import RegistroVendas
from relatorios import GeracaoRelatorios

class SistemaEstoqueVendas(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Estoque e Vendas")
        self.geometry("800x600")

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(expand=1, fill="both")

        self.tab_estoque = GerenciamentoEstoque(self.tabs)
        self.tab_vendas = RegistroVendas(self.tabs)
        self.tab_relatorios = GeracaoRelatorios(self.tabs)

        self.tabs.add(self.tab_estoque, text="Gerenciamento de Estoque")
        self.tabs.add(self.tab_vendas, text="Registro de Vendas")
        self.tabs.add(self.tab_relatorios, text="Relatórios")

if __name__ == "__main__":
    criar_banco_de_dados()
    app = SistemaEstoqueVendas()
    app.mainloop()
