import tkinter as tk
import tkinter.messagebox
import sqlite3

def create_table():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, discount REAL)')
    conn.commit()
    conn.close()

def add_product(name, price, discount):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO products (name, price, discount) VALUES (?, ?, ?)', (name, price, discount))
    conn.commit()
    conn.close()

class InventorySystem:
    def __init__(self, master):
        self.master = master
        master.title("Sistema de Almoxarifado")
        master.configure(bg="#F0F0F0")

        menu_bar = tk.Menu(master)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Sair", command=master.quit)
        menu_bar.add_cascade(label="Arquivo", menu=file_menu)
        master.config(menu=menu_bar)
        
        delete_menu = tk.Menu(menu_bar, tearoff=0)
        delete_menu.add_command(label="Excluir Produtos", command=self.delete_products)
        menu_bar.add_cascade(label="Produtos", menu=delete_menu)
        
        self.main_frame = tk.Frame(master)
        self.main_frame.pack()

        tk.Label(self.main_frame, text="Sistema de Estoque", font=("Arial", 18)).grid(row=0, column=0,
                                                                                      columnspan=2, pady=20)

        tk.Label(self.main_frame, text="Nome do produto:").grid(row=1, column=0, pady=10)
        self.name_entry = tk.Entry(self.main_frame)
        self.name_entry.grid(row=1, column=1, pady=10)

        tk.Label(self.main_frame, text="Preço:").grid(row=2, column=0, pady=10)
        self.price_entry = tk.Entry(self.main_frame)
        self.price_entry.grid(row=2, column=1, pady=10)

        tk.Label(self.main_frame, text="Desconto (0 a 1):").grid(row=3, column=0, pady=10)
        self.discount_entry = tk.Entry(self.main_frame)
        self.discount_entry.grid(row=3, column=1, pady=10)

        tk.Button(self.main_frame, text="Adicionar Produto", command=self.add_product).grid(row=4, column=0,
                                                                                            pady=10, padx=50)
        tk.Button(self.main_frame, text="Listar Produtos", command=self.list_products).grid(row=4, column=1,
                                                                                            pady=10, padx=50)

        tk.Label(self.main_frame, text="rodapé").grid(row=5, column=0, columnspan=2, pady=20)

    def add_product(self):
        name = self.name_entry.get()
        price = float(self.price_entry.get())
        discount = float(self.discount_entry.get())
        if 0 <= discount <= 1:
            add_product(name, price, discount)
        else:
            tk.messagebox.showerror("Erro", "O desconto deve estar entre 0 e 1.")
    
    def delete_products(self):
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()
        conn.close()

        if not products:
            tk.messagebox.showerror("Erro", "Não há produtos cadastrados.")
            return

        delete_window = tk.Toplevel(self.master)
        delete_window.title("Excluir Produtos")

        tk.Label(delete_window, text="Selecione o produto para excluir:").pack(pady=10)

        list_box = tk.Listbox(delete_window, width=40, height=10, font=("Arial", 12))
        list_box.pack()

        for product in products:
            list_box.insert(tk.END, f"{product[0]} - {product[1]}")

        def delete_product():
            selected_index = list_box.curselection()
            if selected_index:
                product_id = products[selected_index[0]][0]
                conn = sqlite3.connect('inventory.db')
                cursor = conn.cursor()
                cursor.execute('DELETE FROM products WHERE id=?', (product_id,))
                conn.commit()
                conn.close()
                list_box.delete(selected_index)
                tk.messagebox.showinfo("Sucesso", "Produto excluído com sucesso.")
            else:
                tk.messagebox.showerror("Erro", "Nenhum produto selecionado.")

        delete_button = tk.Button(delete_window, text="Excluir", command=delete_product)
        delete_button.pack(pady=10)

    def list_products(self):
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()
        conn.close()

        if not products:
            tk.messagebox.showerror("Erro", "Não há produtos cadastrados.")
            return

        list_window = tk.Toplevel(self.master)
        list_window.title("Produtos")

        table = tk.Frame(list_window)
        table.pack()

        header = ["ID", "Nome", "Preço", "Desconto"]
        for i, h in enumerate(header):
            tk.Label(table, text=h, font=("Arial", 12, "bold"), pady=5).grid(row=0, column=i)

        for row, product in enumerate(products, start=1):
            id_, name, price, discount = product
            formatted_price = f"{price:.2f}"
            formatted_discount = f"{discount:.2%}"

            tk.Label(table, text=id_).grid(row=row, column=0)
            tk.Label(table, text=name).grid(row=row, column=1)
            tk.Label(table, text=formatted_price).grid(row=row, column=2)
            tk.Label(table, text=formatted_discount).grid(row=row, column=3)

        list_window.mainloop()

create_table()
root = tk.Tk()
root.title("Sistema de Estoque")

# Cria o menu
InventorySystem(root)
# Inicializa o loop da janela principal
root.mainloop()
