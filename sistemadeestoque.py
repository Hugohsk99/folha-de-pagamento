import tkinter as tk
import sqlite3
from datetime import datetime
from tkinter import messagebox
from tkinter import simpledialog

def fazer_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    conn = sqlite3.connect("almoxarifado.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE nome=? AND senha=?", (usuario, senha))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
        frame_login.pack_forget()
        if user[3] == 1:
            frame_administrativo.pack()
            listar_produtos_admin()
        else:
            frame_usuario.pack()

        listar_produtos()
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos.")
        entry_usuario.delete(0, tk.END)
        entry_senha.delete(0, tk.END)

    conn.close()

def mostrar_login():
    frame_administrativo.pack_forget()
    frame_usuario.pack_forget()
    frame_login.pack()

    entry_usuario.delete(0, tk.END)
    entry_senha.delete(0, tk.END)

def criar_tabelas():
    conn = sqlite3.connect("almoxarifado.db")
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS produtos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, quantidade INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, senha TEXT, admin INTEGER)")

    conn.commit()
    conn.close()

def cadastrar_produto():
    nome_produto = entry_nome.get()
    quantidade = entry_quantidade.get()

    conn = sqlite3.connect("almoxarifado.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO produtos (nome, quantidade) VALUES (?, ?)", (nome_produto, quantidade))

    conn.commit()
    conn.close()

    entry_nome.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)

    listar_produtos()  # Atualiza a lista de produtos

    if frame_administrativo.winfo_ismapped():
        listar_produtos_admin()

def listar_produtos():
    conn = sqlite3.connect("almoxarifado.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM produtos")
    rows = cursor.fetchall()

    listbox_itens.delete(0, tk.END)
    for row in rows:
        listbox_itens.insert(tk.END, f"{row[1]} - Quantidade: {row[2]}")

    conn.close()

def listar_produtos_admin():
    conn = sqlite3.connect("almoxarifado.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM produtos")
    rows = cursor.fetchall()

    listbox_itens.delete(0, tk.END)
    for row in rows:
        listbox_itens.insert(tk.END, f"{row[0]} - {row[1]} - Quantidade: {row[2]}")

    conn.close()

def remover_produto():
    selected_product = listbox_itens.curselection()
    if selected_product:
        product = listbox_itens.get(selected_product)
        product_name = product.split(" - ")[0]

        conn = sqlite3.connect("almoxarifado.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM produtos WHERE nome=?", (product_name,))
        messagebox.showinfo("Sucesso", "Produto removido com sucesso!")
        
        conn.commit()
        conn.close()

        listar_produtos()
        if frame_administrativo.winfo_ismapped():
            listar_produtos_admin()


def listar_produtos_admin():
    conn = sqlite3.connect("almoxarifado.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM produtos")
    rows = cursor.fetchall()

    listbox_itens.delete(0, tk.END)
    for row in rows:
        listbox_itens.insert(tk.END, f"{row[0]} - {row[1]} - Quantidade: {row[2]}")

    conn.close()


def fazer_logout():
    frame_usuario.pack_forget()
    frame_administrativo.pack_forget()
    mostrar_login()
    messagebox.showinfo("Sucesso", "Logout realizado com sucesso!")

def cadastrar_usuario():
    nome_usuario = entry_nome_usuario.get()
    senha = entry_senha_usuario.get()
    admin = int(var_admin.get())

    conn = sqlite3.connect("almoxarifado.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO usuarios (nome, senha, admin) VALUES (?, ?, ?)", (nome_usuario, senha, admin))

    conn.commit()
    conn.close()

    entry_nome_usuario.delete(0, tk.END)
    entry_senha_usuario.delete(0, tk.END)
    var_admin.set(0)

    messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")

def remover_usuario():
    selected_user = listbox_usuarios.curselection()
    if selected_user:
        user_id = listbox_usuarios.get(selected_user).split(" - ")[0]

        conn = sqlite3.connect("almoxarifado.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM usuarios WHERE id=?", (user_id,))

        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Usuário removido com sucesso!")
        listar_usuarios()

def listar_usuarios():
    conn = sqlite3.connect("almoxarifado.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios")
    rows = cursor.fetchall()

    listbox_usuarios.delete(0, tk.END)
    for row in rows:
        user_info = f"{row[0]} - {row[1]}"
        if row[3] == 1:
            user_info += " (Admin)"
        listbox_usuarios.insert(tk.END, user_info)

    conn.close()
root = tk.Tk()
root.title("Sistema de Estoque")
root.geometry("300x250")
root.configure(bg='lightgrey')

frame_login = tk.Frame(root, bg='lightgrey')
frame_administrativo = tk.Frame(root, bg='lightgrey')
frame_usuario = tk.Frame(root, bg='lightgrey')

label_usuario = tk.Label(frame_login, text="Usuário:", bg='lightgrey')
label_usuario.pack()

entry_usuario = tk.Entry(frame_login)
entry_usuario.pack(pady=5)

label_senha = tk.Label(frame_login, text="Senha:", bg='lightgrey')
label_senha.pack()

entry_senha = tk.Entry(frame_login, show="*")
entry_senha.pack(pady=5)

button_login = tk.Button(frame_login, text="Login", command=fazer_login, bg='skyblue', fg='white')
button_login.pack(pady=5)

label_nome = tk.Label(frame_usuario, text="Nome do Produto:", bg='lightgrey')
label_nome.pack()

entry_nome = tk.Entry(frame_usuario)
entry_nome.pack(pady=5)

label_quantidade = tk.Label(frame_usuario, text="Quantidade:", bg='lightgrey')
label_quantidade.pack()

entry_quantidade = tk.Entry(frame_usuario)
entry_quantidade.pack(pady=5)

button_cadastrar_produto = tk.Button(frame_usuario, text="Cadastrar Produto", command=cadastrar_produto, bg='skyblue', fg='white')
button_cadastrar_produto.pack(pady=5)

button_fazer_logout = tk.Button(frame_usuario, text="Logout", command=fazer_logout, bg='skyblue', fg='white')
button_fazer_logout.pack(pady=5)

listbox_itens = tk.Listbox(frame_usuario, width=50)
listbox_itens.pack(pady=5)

button_remover_produto = tk.Button(frame_usuario, text="Remover Produto", command=remover_produto, bg='skyblue', fg='white')
button_remover_produto.pack(pady=5)

button_fazer_logout = tk.Button(frame_administrativo, text="Logout", command=fazer_logout, bg='skyblue', fg='white')
button_fazer_logout.pack(pady=5)

label_nome_usuario = tk.Label(frame_administrativo, text="Nome do Usuário:", bg='lightgrey')
label_nome_usuario.pack()

entry_nome_usuario = tk.Entry(frame_administrativo)
entry_nome_usuario.pack(pady=5)

label_senha_usuario = tk.Label(frame_administrativo, text="Senha:", bg='lightgrey')
label_senha_usuario.pack()

entry_senha_usuario = tk.Entry(frame_administrativo, show="*")
entry_senha_usuario.pack(pady=5)

label_admin = tk.Label(frame_administrativo, text="Admin:", bg='lightgrey')
label_admin.pack()

var_admin = tk.IntVar()
check_admin = tk.Checkbutton(frame_administrativo, text="Administrador", variable=var_admin, bg='lightgrey')
check_admin.pack(pady=5)

button_cadastrar_usuario = tk.Button(frame_administrativo, text="Cadastrar Usuário", command=cadastrar_usuario, bg='skyblue', fg='white')
button_cadastrar_usuario.pack(pady=5)

listbox_usuarios = tk.Listbox(frame_administrativo, width=40)
listbox_usuarios.pack(pady=5)

button_remover_usuario = tk.Button(frame_administrativo, text="Remover Usuário", command=remover_usuario, bg='skyblue', fg='white')
button_remover_usuario.pack(pady=5)

criar_tabelas()

mostrar_login()

def atualizar_janela():
    listar_produtos()
    if frame_administrativo.winfo_ismapped():
        listar_produtos_admin()
        listar_usuarios()
    root.after(10000, atualizar_janela)
listar_produtos()
root.after(10000, listar_produtos)
root.after(10000, atualizar_janela)

root.mainloop()
