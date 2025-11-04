import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os

# ---------------------- FUNÇÕES DE LOGIN ----------------------
def verificar_login():
    email = entrada_email.get().strip()
    senha = entrada_senha.get().strip()
    tipo_usuario = var_tipo.get()

    if not email or not senha:
        messagebox.showwarning("Aviso", "Preencha todos os campos!")
        return

    arquivo = "alunos.csv" if tipo_usuario == "Aluno" else "professores.csv"

    if not os.path.exists(arquivo):
        messagebox.showerror("Erro", f"Arquivo '{arquivo}' não encontrado!")
        return

    with open(arquivo, "r", encoding="utf-8") as f:
        leitor = csv.reader(f)
        for linha in leitor:
            if len(linha) >= 3:
                nome, email_csv, senha_csv = linha[0], linha[1], linha[2]
                if email == email_csv and senha == senha_csv:
                    if tipo_usuario == "Professor":
                        abrir_tela_professor(nome)
                    else:
                        messagebox.showinfo("Login bem-sucedido", f"Bem-vindo, {nome} (Aluno)")
                    return

    messagebox.showerror("Erro", "Email ou senha incorretos!")

# ---------------------- TELA DO PROFESSOR ----------------------
def abrir_tela_professor(nome_prof):
    janela.withdraw()  # esconde a tela de login
    prof_tela = tk.Toplevel()
    prof_tela.title(f"Sistema Acadêmico - Professor {nome_prof}")
    prof_tela.geometry("500x400")
    prof_tela.configure(bg="#e9ecef")

    tk.Label(prof_tela, text=f"Bem-vindo, Prof. {nome_prof}", font=("Arial", 14, "bold"), bg="#e9ecef").pack(pady=20)

    btn_turmas = tk.Button(prof_tela, text="Turmas", width=15, bg="#007bff", fg="white", command=abrir_tela_turma)
    btn_turmas.pack(pady=10)

    tk.Button(prof_tela, text="Sair", width=10, command=lambda: (prof_tela.destroy(), janela.deiconify())).pack(pady=20)

# ---------------------- TELA DE TURMAS ----------------------
def abrir_tela_turma():
    turma_tela = tk.Toplevel()
    turma_tela.title("Turmas - ADS 2025")
    turma_tela.geometry("700x500")
    turma_tela.configure(bg="#f8f9fa")

    tk.Label(turma_tela, text="Turma: ADS 2025", font=("Arial", 14, "bold"), bg="#f8f9fa").pack(pady=10)

    # Tabela de alunos
    colunas = ("Nome", "Email", "Nota1", "Nota2", "Trabalho", "Faltas", "Média", "Situação")
    tree = ttk.Treeview(turma_tela, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=90, anchor="center")
    tree.pack(fill="both", expand=True, pady=10)

    # Ler alunos do arquivo
    if os.path.exists("alunos.csv"):
        with open("alunos.csv", "r", encoding="utf-8") as f:
            leitor = csv.reader(f)
            for linha in leitor:
                if len(linha) >= 2:
                    tree.insert("", "end", values=(linha[0], linha[1], "", "", "", "", "", ""))

    # Frame de lançamento de notas
    frame = tk.Frame(turma_tela, bg="#f8f9fa")
    frame.pack(pady=10)

    tk.Label(frame, text="Selecione um aluno na tabela e insira as notas:", bg="#f8f9fa").grid(row=0, column=0, columnspan=4, pady=5)

    tk.Label(frame, text="Nota 1:", bg="#f8f9fa").grid(row=1, column=0)
    nota1 = tk.Entry(frame, width=5)
    nota1.grid(row=1, column=1)

    tk.Label(frame, text="Nota 2:", bg="#f8f9fa").grid(row=1, column=2)
    nota2 = tk.Entry(frame, width=5)
    nota2.grid(row=1, column=3)

    tk.Label(frame, text="Trabalho:", bg="#f8f9fa").grid(row=2, column=0)
    trab = tk.Entry(frame, width=5)
    trab.grid(row=2, column=1)

    tk.Label(frame, text="Faltas:", bg="#f8f9fa").grid(row=2, column=2)
    faltas = tk.Entry(frame, width=5)
    faltas.grid(row=2, column=3)

    def lancar_notas():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um aluno!")
            return

        try:
            n1 = float(nota1.get())
            n2 = float(nota2.get())
            nt = float(trab.get())
            f = int(faltas.get())
        except ValueError:
            messagebox.showerror("Erro", "Insira valores válidos!")
            return

        media = (n1 + n2 + nt) / 3
        situacao = "Aprovado" if media >= 7 and f <= 10 else ("Exame" if media < 7 and media >= 3 else "Reprovado")

        tree.set(selecionado, "Nota1", n1)
        tree.set(selecionado, "Nota2", n2)
        tree.set(selecionado, "Trabalho", nt)
        tree.set(selecionado, "Faltas", f)
        tree.set(selecionado, "Média", round(media, 2))
        tree.set(selecionado, "Situação", situacao)

        messagebox.showinfo("Sucesso", f"Notas lançadas!\nMédia: {media:.2f}\nSituação: {situacao}")

        # limpar campos
        nota1.delete(0, tk.END)
        nota2.delete(0, tk.END)
        trab.delete(0, tk.END)
        faltas.delete(0, tk.END)

    tk.Button(frame, text="Lançar Notas", bg="#28a745", fg="white", width=15, command=lancar_notas).grid(row=3, column=0, columnspan=4, pady=10)

# ---------------------- INTERFACE DE LOGIN ----------------------
janela = tk.Tk()
janela.title("Login Acadêmico")
janela.geometry("350x320")
janela.resizable(False, False)
janela.configure(bg="#e9ecef")

tk.Label(janela, text="Sistema de Login Acadêmico", font=("Arial", 15, "bold"), bg="#e9ecef").pack(pady=15)

var_tipo = tk.StringVar(value="Aluno")
frame_tipo = tk.Frame(janela, bg="#e9ecef")
frame_tipo.pack(pady=5)
tk.Radiobutton(frame_tipo, text="Aluno", variable=var_tipo, value="Aluno", bg="#e9ecef").pack(side=tk.LEFT, padx=10)
tk.Radiobutton(frame_tipo, text="Professor", variable=var_tipo, value="Professor", bg="#e9ecef").pack(side=tk.LEFT, padx=10)

tk.Label(janela, text="Email:", bg="#e9ecef").pack(pady=(10, 0))
entrada_email = tk.Entry(janela, width=30)
entrada_email.pack(pady=5)

tk.Label(janela, text="Senha:", bg="#e9ecef").pack(pady=(10, 0))
entrada_senha = tk.Entry(janela, width=30, show="*")
entrada_senha.pack(pady=5)

tk.Button(janela, text="Entrar", width=15, bg="#007bff", fg="white", command=verificar_login).pack(pady=20)

tk.Label(janela, text="© 2025 - Sistema Acadêmico", bg="#e9ecef", fg="gray").pack(side=tk.BOTTOM, pady=5)

janela.mainloop()
