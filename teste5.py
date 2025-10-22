import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
from PIL import Image, ImageTk

# ---------------------- DADOS GLOBAIS ----------------------
disciplinas = []  # lista global de disciplinas

# ---------------------- FUNÇÕES DE LOGIN ----------------------
def verificar_login():
    email = entrada_email.get().strip()
    senha = entrada_senha.get().strip()
    tipo_usuario = var_tipo.get()

    if not email or not senha:
        messagebox.showwarning("Aviso", "Preencha todos os campos!")
        return

    if tipo_usuario == "Aluno":
        arquivo = "alunos.csv"
    elif tipo_usuario == "Professor":
        arquivo = "professores.csv"
    elif tipo_usuario == "Administrador":
        arquivo = "administradores.csv"
    else:  # Coordenador
        arquivo = "coordenadores.csv"

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
                    elif tipo_usuario == "Aluno":
                        abrir_tela_aluno(nome, email)
                    elif tipo_usuario == "Administrador":
                        abrir_tela_admin(nome)
                    else:
                        abrir_tela_coordenador(nome)
                    return

    messagebox.showerror("Erro", "Email ou senha incorretos!")

# ---------------------- FUNÇÃO PARA CARREGAR DISCIPLINAS ----------------------
def carregar_disciplinas():
    global disciplinas
    disciplinas.clear()
    if os.path.exists("disciplinas.csv"):
        with open("disciplinas.csv", "r", encoding="utf-8") as f:
            leitor = csv.reader(f)
            disciplinas.extend([linha[0] for linha in leitor if linha])

# ---------------------- FUNÇÃO PARA SALVAR DISCIPLINAS ----------------------
def salvar_disciplinas():
    with open("disciplinas.csv", "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        for d in disciplinas:
            escritor.writerow([d])

# ---------------------- TELA DO PROFESSOR ----------------------
def abrir_tela_professor(nome_prof):
    janela.withdraw()
    prof_tela = tk.Toplevel()
    prof_tela.title(f"Sistema Acadêmico - Professor {nome_prof}")
    prof_tela.geometry("1920x1080")
    prof_tela.configure(bg="#e9ecef")
    prof_tela.grab_set()

    tk.Label(prof_tela, text=f"Bem-vindo, Prof. {nome_prof}", font=("Arial", 14, "bold"), bg="#e9ecef").pack(pady=10)

    # Botão para acessar turmas
    tk.Button(prof_tela, text="Turmas", width=20, bg="#007bff", fg="white",
              command=lambda: abrir_tela_turma(prof_tela)).pack(pady=10)

    tk.Button(prof_tela, text="Sair", width=10, command=lambda: (prof_tela.destroy(), janela.deiconify())).pack(pady=20)

# ---------------------- TELA DE TURMAS (PROFESSOR) ----------------------
def abrir_tela_turma(prof_tela):
    turma_tela = tk.Toplevel(prof_tela)
    turma_tela.title("Turma 1A")
    turma_tela.geometry("1920x1080")
    turma_tela.configure(bg="#f8f9fa")
    turma_tela.grab_set()

    tk.Label(turma_tela, text="Turma: 1A", font=("Arial", 14, "bold"), bg="#f8f9fa").pack(pady=5)

    # Botão de Disciplinas
    tk.Button(turma_tela, text="Disciplinas", bg="#007bff", fg="white", width=20,
              command=lambda: abrir_frame_disciplinas(turma_tela)).pack(pady=10)

# ---------------------- FRAME DE DISCIPLINAS ----------------------
def abrir_frame_disciplinas(parent):
    frame = tk.Frame(parent, bg="#f8f9fa")
    frame.pack(pady=10, fill="x")

    tk.Label(frame, text="Cadastrar disciplina:", bg="#f8f9fa").pack(side="left", padx=5)
    entrada_disciplina = tk.Entry(frame, width=25)
    entrada_disciplina.pack(side="left", padx=5)

    lista_disciplinas = tk.Listbox(frame, height=5)
    lista_disciplinas.pack(side="left", padx=10)

    # Preencher lista já cadastrada
    for d in disciplinas:
        lista_disciplinas.insert(tk.END, d)

    def adicionar_disciplina():
        nome = entrada_disciplina.get().strip()
        if nome and nome not in disciplinas:
            disciplinas.append(nome)
            lista_disciplinas.insert(tk.END, nome)
            entrada_disciplina.delete(0, tk.END)
            salvar_disciplinas()
        else:
            messagebox.showwarning("Aviso", "Nome inválido ou já cadastrado!")

    tk.Button(frame, text="Adicionar", bg="#28a745", fg="white", command=adicionar_disciplina).pack(side="left", padx=5)

    # Botão para selecionar disciplina
    def selecionar_disciplina():
        selecionada = lista_disciplinas.curselection()
        if not selecionada:
            messagebox.showwarning("Aviso", "Selecione uma disciplina!")
            return
        nome_disciplina = lista_disciplinas.get(selecionada)
        abrir_alunos_disciplina(parent, nome_disciplina)

    tk.Button(frame, text="Selecionar disciplina", bg="#007bff", fg="white", command=selecionar_disciplina).pack(side="left", padx=5)

# ---------------------- LANÇAR NOTAS POR DISCIPLINA ----------------------
def abrir_alunos_disciplina(parent, disciplina):
    alunos_tela = tk.Toplevel(parent)
    alunos_tela.title(f"Disciplina: {disciplina}")
    alunos_tela.geometry("1920x1080")
    alunos_tela.configure(bg="#f8f9fa")
    alunos_tela.grab_set()

    tk.Label(alunos_tela, text=f"Disciplina: {disciplina}", font=("Arial", 14, "bold"), bg="#f8f9fa").pack(pady=10)

    colunas = ("Nome", "Email", "Nota1", "Nota2", "Trabalho", "Faltas", "Média", "Situação")
    tree = ttk.Treeview(alunos_tela, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=90, anchor="center")
    tree.pack(fill="both", expand=True, pady=10)

    # Ler alunos do arquivo alunos.csv
    if os.path.exists("alunos.csv"):
        with open("alunos.csv", "r", encoding="utf-8") as f:
            leitor = csv.reader(f)
            for linha in leitor:
                if len(linha) >= 2:
                    tree.insert("", "end", values=(linha[0], linha[1], "", "", "", "", "", ""))

    # Frame para lançar notas
    frame = tk.Frame(alunos_tela, bg="#f8f9fa")
    frame.pack(pady=10)

    campos = {"Nota1": None, "Nota2": None, "Trabalho": None, "Faltas": None}
    for i, nome_campo in enumerate(campos.keys(), start=1):
        tk.Label(frame, text=f"{nome_campo}:", bg="#f8f9fa").grid(row=i, column=0)
        campos[nome_campo] = tk.Entry(frame, width=5)
        campos[nome_campo].grid(row=i, column=1)

    def lancar_notas_disciplina():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um aluno!")
            return
        try:
            n1 = float(campos["Nota1"].get())
            n2 = float(campos["Nota2"].get())
            nt = float(campos["Trabalho"].get())
            f = int(campos["Faltas"].get())
        except ValueError:
            messagebox.showerror("Erro", "Insira valores válidos!")
            return

        media = (n1 + n2 + nt) / 3
        situacao = "Aprovado" if media >= 7 and f <= 10 else ("Exame" if 3 <= media < 7 else "Reprovado")

        item = tree.item(selecionado)
        valores = list(item["values"])
        valores[2:] = [n1, n2, nt, f, round(media, 2), situacao]
        tree.item(selecionado, values=valores)

        # Salvar notas por disciplina
        filename = f"notas_{disciplina}.csv"
        dados = [tree.item(i)["values"] for i in tree.get_children()]
        with open(filename, "w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerows(dados)

        messagebox.showinfo("Sucesso", f"Notas lançadas para a disciplina {disciplina}!")

        for campo in campos.values():
            campo.delete(0, tk.END)

    tk.Button(frame, text="Lançar Notas", bg="#28a745", fg="white", width=15,
              command=lancar_notas_disciplina).grid(row=5, column=0, columnspan=2, pady=10)

# ---------------------- TELA DO ALUNO ----------------------
def abrir_tela_aluno(nome_aluno, email):
    janela.withdraw()
    aluno_tela = tk.Toplevel()
    aluno_tela.title(f"Área do Aluno - {nome_aluno}")
    aluno_tela.geometry("1920x1080")
    aluno_tela.configure(bg="#f0f2f5")
    aluno_tela.grab_set()

    tk.Label(aluno_tela, text=f"Bem-vindo(a), {nome_aluno}", font=("Arial", 14, "bold"), bg="#f0f2f5").pack(pady=10)

    frame = tk.Frame(aluno_tela, bg="#f0f2f5")
    frame.pack(pady=10, fill="both", expand=True)

    colunas = ("Disciplina", "Nota1", "Nota2", "Trabalho", "Faltas", "Média", "Situação")
    tree = ttk.Treeview(frame, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=80, anchor="center")
    tree.pack(fill="both", expand=True)

    carregar_disciplinas()

    for d in disciplinas:
        arquivo_notas = f"notas_{d}.csv"
        if os.path.exists(arquivo_notas):
            with open(arquivo_notas, "r", encoding="utf-8") as f:
                leitor = csv.reader(f)
                for linha in leitor:
                    # linha contém: Nome, Email, Nota1, Nota2, Trabalho, Faltas, Média, Situação
                    if len(linha) >= 8 and linha[1] == email:
                        tree.insert("", "end", values=(d, linha[2], linha[3], linha[4], linha[5], linha[6], linha[7]))
                        break

    tk.Button(aluno_tela, text="Sair", width=10, command=lambda: (aluno_tela.destroy(), janela.deiconify())).pack(pady=20)

# ---------------------- TELA DO ADMINISTRADOR ----------------------
def abrir_tela_admin(nome_adm):
    janela.withdraw()
    adm_tela = tk.Toplevel()
    adm_tela.title(f"Sistema Acadêmico - Administrador {nome_adm}")
    adm_tela.geometry("1920x1080")
    adm_tela.configure(bg="#e9ecef")
    adm_tela.grab_set()

    tk.Label(adm_tela, text=f"Bem-vindo, ADM {nome_adm}", font=("Arial", 14, "bold"), bg="#e9ecef").pack(pady=10)

    tk.Button(adm_tela, text="Ver Alunos", width=20, bg="#007bff", fg="white",
              command=lambda: abrir_lista_usuarios(adm_tela, "Aluno")).pack(pady=5)
    tk.Button(adm_tela, text="Ver Professores", width=20, bg="#007bff", fg="white",
              command=lambda: abrir_lista_usuarios(adm_tela, "Professor")).pack(pady=5)

    tk.Button(adm_tela, text="Sair", width=10, command=lambda: (adm_tela.destroy(), janela.deiconify())).pack(pady=20)

# ---------------------- NOVA TELA DO COORDENADOR ----------------------
def abrir_tela_coordenador(nome_coord):
    janela.withdraw()
    coord_tela = tk.Toplevel()
    coord_tela.title(f"Sistema Acadêmico - Coordenador {nome_coord}")
    coord_tela.geometry("1920x1080")
    coord_tela.configure(bg="#dee2e6")
    coord_tela.grab_set()

    tk.Label(coord_tela, text=f"Bem-vindo, Coordenador {nome_coord}", font=("Arial", 14, "bold"), bg="#dee2e6").pack(pady=10)

    tk.Button(coord_tela, text="Ver Professores", width=20, bg="#007bff", fg="white",
              command=lambda: abrir_lista_usuarios(coord_tela, "Professor")).pack(pady=5)
    tk.Button(coord_tela, text="Ver Alunos", width=20, bg="#007bff", fg="white",
              command=lambda: abrir_lista_usuarios(coord_tela, "Aluno")).pack(pady=5)
    tk.Button(coord_tela, text="Ver Disciplinas", width=20, bg="#007bff", fg="white",
              command=mostrar_disciplinas).pack(pady=5)

    tk.Button(coord_tela, text="Sair", width=10, command=lambda: (coord_tela.destroy(), janela.deiconify())).pack(pady=20)

def mostrar_disciplinas():
    carregar_disciplinas()
    messagebox.showinfo("Disciplinas", "\n".join(disciplinas) if disciplinas else "Nenhuma disciplina cadastrada.")

# ---------------------- FUNÇÃO PARA LISTAR USUÁRIOS ----------------------
def abrir_lista_usuarios(parent, tipo):
    arquivo = "alunos.csv" if tipo == "Aluno" else "professores.csv"
    if not os.path.exists(arquivo):
        messagebox.showerror("Erro", f"Arquivo '{arquivo}' não encontrado!")
        return

    lista_tela = tk.Toplevel(parent)
    lista_tela.title(f"{tipo}s Cadastrados")
    lista_tela.geometry("800x500")
    lista_tela.configure(bg="#f8f9fa")
    lista_tela.grab_set()

    tree = ttk.Treeview(lista_tela, columns=("Nome", "Email"), show="headings")
    tree.heading("Nome", text="Nome")
    tree.heading("Email", text="Email")
    tree.pack(fill="both", expand=True, pady=10)

    with open(arquivo, "r", encoding="utf-8") as f:
        leitor = csv.reader(f)
        for linha in leitor:
            if len(linha) >= 2:
                tree.insert("", "end", values=(linha[0], linha[1]))

    # Botão para editar aluno/professor
    def editar_usuario():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um usuário!")
            return
        item = tree.item(selecionado)
        nome_atual, email_atual = item["values"]

        edit_tela = tk.Toplevel(lista_tela)
        edit_tela.title("Editar Usuário")
        edit_tela.geometry("400x200")
        edit_tela.grab_set()

        tk.Label(edit_tela, text="Nome:").pack(pady=5)
        entrada_nome = tk.Entry(edit_tela, width=30)
        entrada_nome.pack(pady=5)
        entrada_nome.insert(0, nome_atual)

        tk.Label(edit_tela, text="Email:").pack(pady=5)
        entrada_email = tk.Entry(edit_tela, width=30)
        entrada_email.pack(pady=5)
        entrada_email.insert(0, email_atual)

        def salvar_usuario():
            novo_nome = entrada_nome.get().strip()
            novo_email = entrada_email.get().strip()

            if not novo_nome or not novo_email:
                messagebox.showwarning("Aviso", "Nome e email não podem ser vazios!")
                return

            # Verificar se email já existe
            with open(arquivo, "r", encoding="utf-8") as f:
                leitor = csv.reader(f)
                for linha in leitor:
                    if len(linha) >= 2 and linha[1] == novo_email and novo_email != email_atual:
                        messagebox.showerror("Erro", "Este email já está cadastrado!")
                        return

            # Atualizar Treeview
            tree.item(selecionado, values=(novo_nome, novo_email))

            # Atualizar CSV
            dados = []
            with open(arquivo, "r", encoding="utf-8") as f:
                leitor = csv.reader(f)
                for linha in leitor:
                    if len(linha) >= 2:
                        if linha[1] == email_atual:
                            linha[0] = novo_nome
                            linha[1] = novo_email
                        dados.append(linha)
            with open(arquivo, "w", newline="", encoding="utf-8") as f:
                escritor = csv.writer(f)
                escritor.writerows(dados)

            messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
            edit_tela.destroy()

        tk.Button(edit_tela, text="Salvar", bg="#28a745", fg="white", command=salvar_usuario).pack(pady=10)

    tk.Button(lista_tela, text="Editar", bg="#ffc107", fg="black", command=editar_usuario).pack(pady=10)

# ---------------------- CONFIGURAÇÃO DA JANELA DE LOGIN ----------------------
janela = tk.Tk()
janela.title("Sistema Acadêmico - Login")
janela.geometry("1920x1080")

carregar_disciplinas()

# Imagem de fundo
try:
    resample_method = Image.Resampling.LANCZOS
except AttributeError:
    resample_method = Image.ANTIALIAS

if os.path.exists("c53ce503-8657-4b62-9bce-36a7a3633526.png"):
    imagem_fundo = Image.open("c53ce503-8657-4b62-9bce-36a7a3633526.png")
    imagem_fundo = imagem_fundo.resize((1920, 1080), resample_method)
    fundo = ImageTk.PhotoImage(imagem_fundo)
    label_fundo = tk.Label(janela, image=fundo)
    label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

# Frame login
frame_login = tk.Frame(janela, bg="#055bb8", bd=50)
frame_login.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(frame_login, text="Email:", font=("Arial", 15), bg="#055bb8").grid(row=0, column=0, sticky="w", pady=5)
entrada_email = tk.Entry(frame_login, width=30)
entrada_email.grid(row=0, column=1, pady=5)

tk.Label(frame_login, text="Senha:", font=("Arial", 15), bg="#055bb8").grid(row=1, column=0, sticky="w", pady=5)
entrada_senha = tk.Entry(frame_login, show="*", width=30)
entrada_senha.grid(row=1, column=1, pady=5)

tk.Label(frame_login, text="Tipo de usuário:", font=("Arial", 15), bg="#055bb8").grid(row=2, column=0, sticky="w", pady=5)

var_tipo = tk.StringVar(value="Aluno")

tk.Radiobutton(frame_login, text="Aluno", font=("Arial", 13), variable=var_tipo, value="Aluno", bg="#055bb8").grid(row=3, column=1, sticky="w", pady=2)
tk.Radiobutton(frame_login, text="Professor", font=("Arial", 13), variable=var_tipo, value="Professor", bg="#055bb8").grid(row=4, column=1, sticky="w", pady=2)
tk.Radiobutton(frame_login, text="Administrador", font=("Arial", 13), variable=var_tipo, value="Administrador", bg="#055bb8").grid(row=5, column=1, sticky="w", pady=2)
tk.Radiobutton(frame_login, text="Coordenador", font=("Arial", 13), variable=var_tipo, value="Coordenador", bg="#055bb8").grid(row=6, column=1, sticky="w", pady=2)

botao_login = tk.Button(frame_login, text="ENTRAR", font=("Arial", 15), bg="#15ff00", fg="white", width=15, command=verificar_login)
botao_login.grid(row=7, column=0, columnspan=3, pady=10)

janela.mainloop()
