import tkinter as tk
import tkinter.messagebox
import sqlite3
from functools import partial
from typing import Callable


def create_table():
    # Conecta ao banco de dados e cria a tabela de funcionários, se ela não existir
    conn = sqlite3.connect('payroll.db')
    cursor = conn.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, salary REAL)')
    conn.commit()
    conn.close()


def add_employee(name, salary):
    # Conecta ao banco de dados e adiciona um novo funcionário
    conn = sqlite3.connect('payroll.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO employees (name, salary) VALUES (?, ?)', (name, salary))
    conn.commit()
    conn.close()

def calcular_desconto_inss(salario_bruto):
    if salario_bruto <= 1045.00:
        desconto_inss = salario_bruto * 0.075
    elif salario_bruto <= 2089.60:
        desconto_inss = salario_bruto * 0.09
    elif salario_bruto <= 3134.40:
        desconto_inss = salario_bruto * 0.12
    elif salario_bruto <= 6101.06:
        desconto_inss = salario_bruto * 0.14
    else:
        desconto_inss = 6101.06 * 0.14
    return desconto_inss


class PayrollSystem:
    def __init__(self, master):
        self.master = master
        master.title("Sistema de Folha de Pagamento")
        master.configure(bg="#F0F0F0")

        # Cria o menu da barra de menu

        menu_bar = tk.Menu(master)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Sair", command=master.quit)
        menu_bar.add_cascade(label="Arquivo", menu=file_menu)
        master.config(menu=menu_bar)

        salary_menu = tk.Menu(menu_bar, tearoff=0)
        salary_menu.add_command(label="Calcular Salário Líquido", command=self.calculate_salary)
        menu_bar.add_cascade(label="Salário", menu=salary_menu)
        salary_menu.add_command(label="Calcular Salário Líquido (sem cadastro)", command=self.calculate_salary_without_registration)

        # Cria o frame principal
        self.main_frame = tk.Frame(master)
        self.main_frame.pack()

        # Cria o rótulo do título
        tk.Label(self.main_frame, text="Sistema de Folha de Pagamento", font=("Arial", 18)).grid(row=0, column=0,
                                                                                                 columnspan=2, pady=20)
        # Cria os campos de entrada
        tk.Label(self.main_frame, text="Nome:").grid(row=1, column=0, pady=10)
        self.name_entry = tk.Entry(self.main_frame)
        self.name_entry.grid(row=1, column=1, pady=10)
        tk.Label(self.main_frame, text="Salário:").grid(row=2, column=0, pady=10)
        self.salary_entry = tk.Entry(self.main_frame)
        self.salary_entry.grid(row=2, column=1, pady=10)

        # Cria o botão de adicionar funcionário
        tk.Button(self.main_frame, text="Adicionar Funcionário", command=self.add_employee).grid(row=3, column=0,
                                                                                                 pady=10, padx=50)
        # Cria o botão de listar funcionários
        tk.Button(self.main_frame, text="Listar Funcionários", command=self.list_employees).grid(row=3, column=1,
                                                                                                 pady=10, padx=50)

        # Cria o rodapé
        tk.Label(self.main_frame, text="rodapé").grid(row=4, column=0, columnspan=2, pady=20)

    def calculate_salary(self):

        # Cria a janela secundária para calcular o salário líquido
        salary_window = tk.Toplevel(self.master)
        salary_window.title("Calcular Salário Líquido")

        # Cria os campos de entrada para o salário bruto e os descontos
        tk.Label(salary_window, text="Salário Bruto:").grid(row=0, column=0, pady=10)
        self.gross_salary_entry = tk.Entry(salary_window)
        self.gross_salary_entry.grid(row=0, column=1, pady=10)
        tk.Label(salary_window, text="Descontos:").grid(row=1, column=0, pady=10)
        self.deductions_entry = tk.Entry(salary_window)
        self.deductions_entry.grid(row=1, column=1, pady=10)

        # Cria o botão de calcular salário líquido
        tk.Button(salary_window, text="Calcular", command=self.calculate_net_salary).grid(row=2, column=0, pady=10)

        # Cria o campo de exibição do salário líquido
        tk.Label(salary_window, text="Salário Líquido:").grid(row=3, column=0, pady=10)
        self.net_salary_label = tk.Label(salary_window, text="")
        self.net_salary_label.grid(row=3, column=1, pady=10)

    def calculate_net_salary(self):
        # Conecta ao banco de dados e lista os funcionários cadastrados
        conn = sqlite3.connect('payroll.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees')
        employees = cursor.fetchall()
        conn.close()

        # Verifica se existem funcionários cadastrados
        if not employees:
            tk.messagebox.showerror("Erro", "Não há funcionários cadastrados.")
            return

        # Cria a janela secundária para exibir os salários líquidos
        net_salary_window = tk.Toplevel(self.master)
        net_salary_window.title("Salários Líquidos")

        # Cria a tabela para exibir os salários líquidos
        table = tk.Frame(net_salary_window)
        table.pack(padx=10, pady=10)

        # Cria o cabeçalho da tabela
        tk.Label(table, text="ID", font=("Arial", 12, "bold")).grid(row=0, column=0)
        tk.Label(table, text="Nome", font=("Arial", 12, "bold")).grid(row=0, column=1)
        tk.Label(table, text="Salário Bruto", font=("Arial", 12, "bold")).grid(row=0, column=2)
        tk.Label(table, text="Descontos", font=("Arial", 12, "bold")).grid(row=0, column=3)
        tk.Label(table, text="Salário Líquido", font=("Arial", 12, "bold")).grid(row=0, column=4)

        # Preenche a tabela com os salários líquidos
        for i, employee in enumerate(employees, start=1):
            gross_salary = employee[2]
            inss = gross_salary * 0.1
            irrf = (gross_salary - inss) * 0.2
            net_salary = gross_salary - inss - irrf
            tk.Label(table, text=employee[0]).grid(row=i, column=0)
            tk.Label(table, text=employee[1]).grid(row=i, column=1)
            tk.Label(table, text="{:.2f}".format(gross_salary)).grid(row=i, column=2)
            tk.Label(table, text="{:.2f}".format(inss + irrf)).grid(row=i, column=3)
            tk.Label(table, text="{:.2f}".format(net_salary)).grid(row=i, column=4)

    def calculate_salary_without_registration(self):
        def on_calculate():
            try:
                salary = float(self.gross_salary_entry.get())
                inss_deduction = calcular_desconto_inss(salary)
                net_salary = salary - inss_deduction
                self.net_salary_label.config(text="{:.2f}".format(net_salary))
            except ValueError:
                tk.messagebox.showerror("Erro", "Insira um valor válido para o salário bruto.")

        salary_window = tk.Toplevel(self.master)
        salary_window.title("Calcular Salário Líquido (sem cadastro)")

        tk.Label(salary_window, text="Salário Bruto:").grid(row=0, column=0, pady=10)
        self.gross_salary_entry = tk.Entry(salary_window)
        self.gross_salary_entry.grid(row=0, column=1, pady=10)

        tk.Button(salary_window, text="Calcular", command=on_calculate).grid(row=2, column=0, pady=10)

        tk.Label(salary_window, text="Salário Líquido com desconto INSS:").grid(row=3, column=0, pady=10)
        self.net_salary_label = tk.Label(salary_window, text="")
        self.net_salary_label.grid(row=3, column=1, pady=10)

    def add_employee(self):
        name = self.name_entry.get()
        salary = float(self.salary_entry.get())
        add_employee(name, salary)

    def list_employees(self):
        # Conecta ao banco de dados e lista os funcionários cadastrados
        conn = sqlite3.connect('payroll.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees')
        employees = cursor.fetchall()
        conn.close()

        # Verifica se existem funcionários cadastrados
        if not employees:
            tk.messagebox.showerror("Erro", "Não há funcionários cadastrados.")
            return

        # Cria a janela secundária para exibir a lista de funcionários
        list_window = tk.Toplevel(self.master)
        list_window.title("Funcionários")

        tk.Button(list_window, text="Calcular Salário Líquido", command=self.calculate_net_salary).pack(pady=10)

        # Cria a tabela para listar os funcionários
        table = tk.Frame(list_window)
        table.pack(padx=10, pady=10)

        # Cria o cabeçalho da tabela
        tk.Label(table, text="ID", font=("Arial", 12, "bold")).grid(row=0, column=0)
        tk.Label(table, text="Nome", font=("Arial", 12, "bold")).grid(row=0, column=1)
        tk.Label(table, text="Salário", font=("Arial", 12, "bold")).grid(row=0, column=2)

        # Preenche a tabela com os dados dos funcionários
        for i, employee in enumerate(employees, start=1):
            tk.Label(table, text=employee[0]).grid(row=i, column=0)
            tk.Label(table, text=employee[1]).grid(row=i, column=1)
            tk.Label(table, text=employee[2]).grid(row=i, column=2)

create_table()
root = tk.Tk()
root.title("Sistema de Folha de Pagamento")

# Cria o menu
PayrollSystem(root)
# Inicializa o loop da janela principal
root.mainloop()