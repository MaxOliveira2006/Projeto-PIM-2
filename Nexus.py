import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import csv
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

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

    # --- Carregar a imagem de fundo (verifica se o arquivo existe) ---
    if os.path.exists("Copilot_20251025_113657-removebg-preview.png"):
        imagem_fundo = Image.open("Copilot_20251025_113657-removebg-preview.png")
        imagem_fundo = imagem_fundo.resize((800, 800))
        imagem_fundo_tk = ImageTk.PhotoImage(imagem_fundo)

        fundo_label = tk.Label(prof_tela, image=imagem_fundo_tk)
        fundo_label.image = imagem_fundo_tk  # mantém a referência
        fundo_label.place(x=0, y=0, relwidth=1, relheight=1)

    # --- Conteúdo sobre o fundo ---
    tk.Label(
        prof_tela,
        text=f"Bem-vindo, Prof. {nome_prof}",
        font=("Arial", 16, "bold"),
        bg="#ffffff"
    ).pack(pady=10)

    # --- Botão para acessar turmas ---
    tk.Button(
        prof_tela, text="Selecionar Turma", width=25,
        bg="#007bff", fg="white",
        command=lambda: abrir_tela_selecao_turma(prof_tela)
    ).pack(pady=10)

    # --- Função para confirmar saída ---
    def sair_professor():
        resposta = messagebox.askyesno("Confirmação", "Deseja realmente sair e voltar à tela de login?")
        if resposta:
            prof_tela.destroy()
            janela.deiconify()

    # --- Botão Sair ---
    tk.Button(
        prof_tela, text="Sair", width=10,
        bg="#dc3545", fg="white",
        command=sair_professor
    ).pack(pady=20)

    # --- Confirmação ao clicar no X da janela ---
    prof_tela.protocol("WM_DELETE_WINDOW", sair_professor)



# ---------------------- ESCOLHER TURMA ----------------------
def abrir_tela_selecao_turma(prof_tela):
    if not os.path.exists("turmas.csv"):
        messagebox.showwarning("Aviso", "Nenhuma turma cadastrada ainda!")
        return

    selec_tela = tk.Toplevel(prof_tela)
    selec_tela.title("Selecionar Turma")
    selec_tela.geometry("600x400")
    selec_tela.configure(bg="#f8f9fa")
    selec_tela.grab_set()

    tk.Label(selec_tela, text="Selecione a Turma:", font=("Arial", 13, "bold"), bg="#f8f9fa").pack(pady=10)

    lista_turmas = []
    with open("turmas.csv", "r", encoding="utf-8") as f:
        leitor = csv.reader(f)
        for linha in leitor:
            if len(linha) >= 1:
                lista_turmas.append(linha[0])

    combo_turmas = ttk.Combobox(selec_tela, values=lista_turmas, width=40)
    combo_turmas.pack(pady=10)

    def abrir_turma():
        turma_sel = combo_turmas.get()
        if not turma_sel:
            messagebox.showwarning("Aviso", "Selecione uma turma!")
            return
        selec_tela.destroy()
        abrir_tela_turma(prof_tela, turma_sel)

    tk.Button(selec_tela, text="Abrir Turma", bg="#28a745", fg="white", command=abrir_turma).pack(pady=10)


# ---------------------- TELA DE TURMA (PROFESSOR) ----------------------
def abrir_tela_turma(prof_tela, turma_nome):
    turma_tela = tk.Toplevel(prof_tela)
    turma_tela.title(f"Turma {turma_nome}")
    turma_tela.geometry("1920x1080")
    turma_tela.configure(bg="#f8f9fa")
    turma_tela.grab_set()

    tk.Label(turma_tela, text=f"Turma: {turma_nome}", font=("Arial", 16, "bold"), bg="#f8f9fa").pack(pady=10)

    tk.Button(turma_tela, text="Disciplinas", bg="#007bff", fg="white", width=25,
              command=lambda: abrir_frame_disciplinas(turma_tela, turma_nome)).pack(pady=10)


# ---------------------- FRAME DE DISCIPLINAS ----------------------
def abrir_frame_disciplinas(parent, turma_nome):
    frame = tk.Frame(parent, bg="#f8f9fa")
    frame.pack(pady=10, fill="x")

    tk.Label(frame, text="Selecione uma Disciplina:", bg="#f8f9fa", font=("Arial", 10, "bold")).pack(side="top", pady=5)

    lista_disciplinas = tk.Listbox(frame, height=6, width=40)
    lista_disciplinas.pack(padx=10, pady=5)

    # Carregar disciplinas salvas
    disciplinas = []
    if os.path.exists("disciplinas.csv"):
        with open("disciplinas.csv", "r", encoding="utf-8") as f:
            leitor = csv.reader(f)
            for linha in leitor:
                if len(linha) > 0:
                    disciplinas.append(linha[0])
                    lista_disciplinas.insert(tk.END, linha[0])
    else:
        messagebox.showinfo("Informação", "Nenhuma disciplina cadastrada ainda!")

    def selecionar_disciplina():
        selecionada = lista_disciplinas.curselection()
        if not selecionada:
            messagebox.showwarning("Aviso", "Selecione uma disciplina!")
            return
        nome_disciplina = lista_disciplinas.get(selecionada)
        abrir_alunos_disciplina(parent, turma_nome, nome_disciplina)

    tk.Button(frame, text="Selecionar disciplina", bg="#007bff", fg="white", command=selecionar_disciplina).pack(pady=5)



# ---------------------- LANÇAR NOTAS POR DISCIPLINA ----------------------
def abrir_alunos_disciplina(parent, turma_nome, disciplina):
    alunos_tela = tk.Toplevel(parent)
    alunos_tela.title(f"{disciplina} - Turma {turma_nome}")
    alunos_tela.geometry("1920x1080")
    alunos_tela.configure(bg="#f8f9fa")
    alunos_tela.grab_set()

    tk.Label(alunos_tela, text=f"Disciplina: {disciplina} | Turma: {turma_nome}", font=("Arial", 14, "bold"), bg="#f8f9fa").pack(pady=10)

    colunas = ("Nome", "Email", "Nota1", "Nota2", "Trabalho", "Faltas", "Média", "Situação")
    tree = ttk.Treeview(alunos_tela, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")
    tree.pack(fill="both", expand=True, pady=10)

    # Ler alunos da turma
    alunos_turma = []
    if os.path.exists("turma_alunos.csv"):
        with open("turma_alunos.csv", "r", encoding="utf-8") as f:
            leitor = csv.reader(f)
            for linha in leitor:
                if len(linha) >= 2 and linha[1] == turma_nome:
                    alunos_turma.append(linha[0])

    # Adicionar alunos à tabela (com e-mails vindos de alunos.csv)
    alunos_email = {}
    if os.path.exists("alunos.csv"):
        with open("alunos.csv", "r", encoding="utf-8") as f:
            for nome, email, *resto in csv.reader(f):
                alunos_email[nome] = email

    for nome in alunos_turma:
        email = alunos_email.get(nome, "")
        tree.insert("", "end", values=(nome, email, "", "", "", "", "", ""))

    # Carregar notas anteriores (se houver)
    filename = f"notas_{turma_nome}_{disciplina}.csv"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            leitor = csv.reader(f)
            for linha in leitor:
                if len(linha) >= len(colunas):
                    tree.insert("", "end", values=linha)

    # Frame para lançar notas
    frame = tk.Frame(alunos_tela, bg="#f8f9fa")
    frame.pack(pady=10)

    campos = {"Nota1": None, "Nota2": None, "Trabalho": None, "Faltas": None}
    for i, nome_campo in enumerate(campos.keys(), start=1):
        tk.Label(frame, text=f"{nome_campo}:", bg="#f8f9fa").grid(row=i, column=0)
        campos[nome_campo] = tk.Entry(frame, width=6)
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

        media = round((n1 + n2 + nt) / 3, 2)
        situacao = "Aprovado" if media >= 7 and f <= 10 else ("Exame" if 3 <= media < 7 else "Reprovado")

        item = tree.item(selecionado)
        valores = list(item["values"])
        valores[2:] = [n1, n2, nt, f, media, situacao]
        tree.item(selecionado, values=valores)

        # Salvar notas por turma e disciplina
        dados = [tree.item(i)["values"] for i in tree.get_children()]
        with open(filename, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerows(dados)

        messagebox.showinfo("Sucesso", f"Notas lançadas para {disciplina} - {turma_nome}!")
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
    aluno_tela.configure(bg="#ffffff")
    aluno_tela.grab_set()

    # --- Carregar a imagem de fundo (com verificação de existência) ---
    if os.path.exists("Copilot_20251025_113657-removebg-preview.png"):
        imagem_fundo = Image.open("Copilot_20251025_113657-removebg-preview.png")
        imagem_fundo = imagem_fundo.resize((800, 800))
        imagem_fundo_tk = ImageTk.PhotoImage(imagem_fundo)

        fundo_label = tk.Label(aluno_tela, image=imagem_fundo_tk)
        fundo_label.image = imagem_fundo_tk  # mantém referência
        fundo_label.place(x=0, y=0, relwidth=1, relheight=1)

    # --- Saudação ---
    tk.Label(
        aluno_tela,
        text=f"Bem-vindo(a), {nome_aluno}",
        font=("Arial", 16, "bold"),
        bg="#ffffff"
    ).pack(pady=20)

    # --- Frame principal com botões ---
    botoes_frame = tk.Frame(aluno_tela, bg="#ffffff")
    botoes_frame.pack(pady=40)

    tk.Button(
        botoes_frame, text="📘 Ver meu boletim", font=("Arial", 12, "bold"),
        bg="#007bff", fg="white", width=25, height=2,
        command=lambda: mostrar_boletim(aluno_tela, nome_aluno, email)
    ).grid(row=0, column=0, padx=20, pady=10)

    tk.Button(
        botoes_frame, text="🧾 Documento do aluno", font=("Arial", 12, "bold"),
        bg="#17a2b8", fg="white", width=25, height=2,
        command=lambda: mostrar_documento_aluno(aluno_tela, nome_aluno, email)
    ).grid(row=0, column=1, padx=20, pady=10)

    tk.Button(
        botoes_frame, text="❓ Perguntas frequentes", font=("Arial", 12, "bold"),
        bg="#ffc107", fg="black", width=25, height=2,
        command=lambda: abrir_faq(aluno_tela)
    ).grid(row=0, column=2, padx=20, pady=10)

    # --- Função para confirmar saída ---
    def sair_aluno():
        resposta = messagebox.askyesno("Confirmação", "Deseja realmente sair e voltar à tela de login?")
        if resposta:
            aluno_tela.destroy()
            janela.deiconify()

    # --- Botão Sair ---
    tk.Button(
        aluno_tela, text="Sair", width=12, height=2,
        bg="#dc3545", fg="white",
        command=sair_aluno
    ).pack(pady=30)

    # --- Confirmação ao clicar no 'X' da janela ---
    aluno_tela.protocol("WM_DELETE_WINDOW", sair_aluno)




# ---------------------- MOSTRAR BOLETIM ----------------------
def mostrar_boletim(parent, nome_aluno, email):
    boletim_tela = tk.Toplevel(parent)
    boletim_tela.title("Boletim do Aluno")
    boletim_tela.geometry("1200x700")
    boletim_tela.configure(bg="#f8f9fa")
    boletim_tela.grab_set()

    tk.Label(
        boletim_tela,
        text=f"Boletim de {nome_aluno}",
        font=("Arial", 16, "bold"),
        bg="#f8f9fa"
    ).pack(pady=10)

    frame = tk.Frame(boletim_tela, bg="#f8f9fa")
    frame.pack(pady=10, fill="both", expand=True)

    colunas = ("Disciplina", "Nota1", "Nota2", "Trabalho", "Faltas", "Média", "Situação")
    tree = ttk.Treeview(frame, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")
    tree.pack(fill="both", expand=True, padx=20, pady=20)

    # --- Buscar turma ---
    turma_aluno = None
    if os.path.exists("turma_alunos.csv"):
        with open("turma_alunos.csv", "r", encoding="utf-8") as f:
            leitor = csv.reader(f)
            for linha in leitor:
                if len(linha) >= 2 and linha[0] == nome_aluno:
                    turma_aluno = linha[1]
                    break

    if not turma_aluno:
        tk.Label(frame, text="⚠️ Nenhuma turma encontrada para este aluno.",
                 font=("Arial", 12), bg="#f8f9fa", fg="red").pack(pady=10)
        return

    # --- Buscar disciplinas ---
    disciplinas = []
    if os.path.exists("disciplinas.csv"):
        with open("disciplinas.csv", "r", encoding="utf-8") as f:
            leitor = csv.reader(f)
            disciplinas = [linha[0] for linha in leitor if linha]

    # --- Adicionar dados na Treeview ---
    dados_boletim = []
    for d in disciplinas:
        arquivo_notas = f"notas_{turma_aluno}_{d}.csv"
        if os.path.exists(arquivo_notas):
            with open(arquivo_notas, "r", encoding="utf-8") as f:
                leitor = csv.reader(f)
                for linha in leitor:
                    if len(linha) >= 8 and linha[1] == email:
                        valores = (d, linha[2], linha[3], linha[4], linha[5], linha[6], linha[7])
                        tree.insert("", "end", values=valores)
                        dados_boletim.append(valores)
                        break

    if not tree.get_children():
        tk.Label(frame, text="Nenhuma nota lançada ainda.",
                 font=("Arial", 12), bg="#f8f9fa", fg="gray").pack(pady=10)

    # ---------------------- FUNÇÃO PARA GERAR PDF ----------------------
    def gerar_pdf():
        if not dados_boletim:
            messagebox.showwarning("Aviso", "Não há notas para gerar o boletim.")
            return

        nome_arquivo = f"Boletim_{nome_aluno.replace(' ', '_')}.pdf"
        doc = SimpleDocTemplate(nome_arquivo, pagesize=A4)
        styles = getSampleStyleSheet()
        elementos = []

        titulo = Paragraph(f"<b>Boletim do Aluno</b>", styles["Title"])
        subtitulo = Paragraph(f"<b>Nome:</b> {nome_aluno}<br/><b>Email:</b> {email}", styles["Normal"])
        elementos.append(titulo)
        elementos.append(Spacer(1, 12))
        elementos.append(subtitulo)
        elementos.append(Spacer(1, 20))

        # Tabela com as notas
        dados_tabela = [colunas] + dados_boletim
        tabela = Table(dados_tabela, colWidths=[80, 60, 60, 80, 60, 60, 80])
        tabela.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
            ("TEXTCOLOR", (0, 0), (0, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.gray),
            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
        ]))
        elementos.append(tabela)
        elementos.append(Spacer(1, 20))

        doc.build(elementos)
        messagebox.showinfo("PDF Gerado", f"Boletim salvo como '{nome_arquivo}'")

        # --- ABRIR PDF AUTOMATICAMENTE NO NAVEGADOR ---
        try:
            os.startfile(nome_arquivo)  # Abre com o programa padrão (normalmente navegador ou leitor de PDF)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o PDF:\n{e}")

    # ---------------------- BOTÃO GERAR PDF ----------------------
    btn_pdf = tk.Button(
        boletim_tela,
        text="📄 Gerar PDF do Boletim",
        font=("Arial", 12, "bold"),
        bg="#007bff",
        fg="white",
        padx=20,
        pady=10,
        relief="raised",
        command=gerar_pdf
    )
    btn_pdf.pack(pady=15)

# ---------------------- DOCUMENTO DO ALUNO ----------------------
def mostrar_documento_aluno(parent, nome_aluno, email):
    doc_tela = tk.Toplevel(parent)
    doc_tela.title("Documento do Aluno")
    doc_tela.geometry("600x450")
    doc_tela.configure(bg="#f8f9fa")
    doc_tela.grab_set()

    tk.Label(doc_tela, text="Documento do Aluno", font=("Arial", 16, "bold"), bg="#f8f9fa").pack(pady=20)

    # Buscar RA do aluno (assumindo CSV: Nome, Email, Senha, RA)
    ra_aluno = "N/A"
    if os.path.exists("alunos.csv"):
        with open("alunos.csv", "r", encoding="utf-8") as f:
            leitor = csv.reader(f)
            for linha in leitor:
                if len(linha) >= 4 and linha[1] == email:
                    ra_aluno = linha[3]  # coluna 3 = RA
                    break

    # Buscar turma do aluno
    turma_aluno = "N/A"
    if os.path.exists("turma_alunos.csv"):
        with open("turma_alunos.csv", "r", encoding="utf-8") as f:
            leitor = csv.reader(f)
            for linha in leitor:
                if len(linha) >= 2 and linha[0] == nome_aluno:
                    turma_aluno = linha[1]
                    break

    # Exibir dados
    info_frame = tk.Frame(doc_tela, bg="#ffffff", bd=2, relief="groove")
    info_frame.pack(padx=40, pady=20, fill="x")

    dados = {
        "Nome": nome_aluno,
        "Email": email,
        "RA": ra_aluno,
        "Turma": turma_aluno
    }

    for chave, valor in dados.items():
        linha = tk.Frame(info_frame, bg="#ffffff")
        linha.pack(anchor="w", padx=20, pady=8)
        tk.Label(linha, text=f"{chave}:", font=("Arial", 12, "bold"), bg="#ffffff").pack(side="left")
        tk.Label(linha, text=valor, font=("Arial", 12), bg="#ffffff").pack(side="left", padx=10)


      # ---------------------- FAQ com perguntas prontas ----------------------
def abrir_faq(parent):
    faq_tela = tk.Toplevel(parent)
    faq_tela.title("FAQ Interativo")
    faq_tela.geometry("600x500")
    faq_tela.configure(bg="#f8f9fa")
    faq_tela.grab_set()

    tk.Label(faq_tela, text="Pergntas frequentes", font=("Arial", 16, "bold"), bg="#f8f9fa").pack(pady=10)

    # Frame das perguntas
    perguntas_frame = tk.Frame(faq_tela, bg="#f8f9fa")
    perguntas_frame.pack(pady=20)

    # Dicionário de perguntas e respostas
    faq_dict = {
        
        "Como vejo minhas notas?": "Para ver suas notas, clique em 'Ver meu boletim'.",
        "Como vejo meu documento?": "você pode acessar seu documento em documento do aluno.",
        "Qual é minha turma?": "Você pode ver sua turma no docomento do aluno ou perguntar ao coordenador.",
        "O que é recuperação?": "Se a média estiver entre 3 e 6,99, você deve fazer exame.",
        "Como sei se estou reprovado?": "Se a média < 3 ou faltas > 10, você está reprovado.",
        "Como é calculada minha média? ": "A média é calculada com nota 1 + nota 2 + trabalho e dividia por 3",
       
    }

    # Função para mostrar resposta
    def mostrar_resposta(resposta):
        resposta_label.config(text=resposta)

    # Criar botões para cada pergunta
    for i, (pergunta, resposta) in enumerate(faq_dict.items()):
        tk.Button(perguntas_frame, text=pergunta, font=("Arial", 12), bg="#007bff", fg="white",
                  width=40, height=2, wraplength=400,
                  command=lambda r=resposta: mostrar_resposta(r)).pack(pady=5)

    # Label para exibir a resposta
    resposta_label = tk.Label(faq_tela, text="", font=("Arial", 12), bg="#f0f2f5", fg="black",
                              wraplength=500, justify="left")
    resposta_label.pack(pady=20, padx=20)




# ---------------------- TELA DO ADMINISTRADOR ----------------------
def abrir_tela_admin(nome_adm):
    janela.withdraw()
    adm_tela = tk.Toplevel()
    adm_tela.title(f"Sistema Acadêmico - Administrador {nome_adm}")
    adm_tela.geometry("1920x1080")
    adm_tela.configure(bg="#ffffff")
    adm_tela.grab_set()

    # --- Carregar e redimensionar a imagem de fundo ---
    if os.path.exists("Copilot_20251025_113657-removebg-preview.png"):
        imagem_fundo = Image.open("Copilot_20251025_113657-removebg-preview.png")
        imagem_fundo = imagem_fundo.resize((800, 800))
        imagem_fundo_tk = ImageTk.PhotoImage(imagem_fundo)

        fundo_label = tk.Label(adm_tela, image=imagem_fundo_tk)
        fundo_label.image = imagem_fundo_tk  # mantém referência
        fundo_label.place(x=0, y=0, relwidth=1, relheight=1)

    # --- Título ---
    tk.Label(
        adm_tela,
        text=f"Bem-vindo, ADM {nome_adm}",
        font=("Arial", 16, "bold"),
        bg="#ffffff"
    ).pack(pady=20)

    # --- Botões principais ---
    tk.Button(
        adm_tela, text="Ver Alunos", width=20, height=2,
        bg="#007bff", fg="white",
        command=lambda: abrir_lista_usuarios(adm_tela, "Aluno")
    ).pack(pady=10)

    tk.Button(
        adm_tela, text="Ver Professores", width=20, height=2,
        bg="#007bff", fg="white",
        command=lambda: abrir_lista_usuarios(adm_tela, "Professor")
    ).pack(pady=10)

    # --- Função de sair com confirmação ---
    def sair_admin():
        resposta = messagebox.askyesno("Confirmação", "Deseja realmente sair e voltar à tela de login?")
        if resposta:
            adm_tela.destroy()
            janela.deiconify()

    # --- Botão de sair ---
    tk.Button(
        adm_tela, text="Sair", width=20, height=2,
        bg="#dc3545", fg="white",
        command=sair_admin
    ).pack(pady=20)

    # --- Confirmação ao clicar no X ---
    adm_tela.protocol("WM_DELETE_WINDOW", sair_admin)



def abrir_tela_coordenador(nome_coord):
    janela.withdraw()
    coord_tela = tk.Toplevel()
    coord_tela.title(f"Sistema Acadêmico - Coordenador {nome_coord}")
    coord_tela.geometry("1920x1080")
    coord_tela.configure(bg="#ffffff")
    coord_tela.grab_set()

    # ---------------------- IMAGEM DE FUNDO ----------------------
    try:
        resample_method = Image.Resampling.LANCZOS
    except AttributeError:
        resample_method = Image.ANTIALIAS

    if os.path.exists("Copilot_20251025_113657-removebg-preview.png"):
        imagem_fundo = Image.open("Copilot_20251025_113657-removebg-preview.png")
        imagem_fundo = imagem_fundo.resize((800, 800), resample_method)
        fundo = ImageTk.PhotoImage(imagem_fundo)
        label_fundo = tk.Label(coord_tela, image=fundo)
        label_fundo.image = fundo  # mantém referência
        label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

    # ---------------------- CONTEÚDO SOBRE O FUNDO ----------------------
    tk.Label(
        coord_tela,
        text=f"Bem-vindo(a), Coordenador {nome_coord}",
        font=("Arial", 18, "bold"),
        bg="#ffffff"
    ).pack(pady=30)

    botoes_frame = tk.Frame(coord_tela, bg="#ffffff")
    botoes_frame.pack(pady=40)

    tk.Button(
        botoes_frame, text="👨‍🏫 Ver Professores", font=("Arial", 12, "bold"),
        bg="#007bff", fg="white", width=22, height=2,
        command=lambda: abrir_lista_usuarios(coord_tela, "Professor")
    ).grid(row=0, column=0, padx=15, pady=15)

    tk.Button(
        botoes_frame, text="🎓 Ver Alunos", font=("Arial", 12, "bold"),
        bg="#007bff", fg="white", width=22, height=2,
        command=lambda: abrir_lista_usuarios(coord_tela, "Aluno")
    ).grid(row=0, column=1, padx=15, pady=15)

    tk.Button(
        botoes_frame, text="📚 Ver Disciplinas", font=("Arial", 12, "bold"),
        bg="#17a2b8", fg="white", width=22, height=2,
        command=mostrar_disciplinas
    ).grid(row=0, column=2, padx=15, pady=15)

    tk.Button(
        botoes_frame, text="🏫 Gerenciar Turmas", font=("Arial", 12, "bold"),
        bg="#28a745", fg="white", width=22, height=2,
        command=lambda: abrir_tela_turmas(coord_tela)
    ).grid(row=0, column=3, padx=15, pady=15)

    # ---------------------- BOTÃO SAIR E CONFIRMAÇÃO ----------------------
    def sair_coordenador():
        resposta = messagebox.askyesno("Confirmação", "Deseja realmente sair e voltar à tela de login?")
        if resposta:
            coord_tela.destroy()
            janela.deiconify()

    tk.Button(
        coord_tela, text="Sair", font=("Arial", 12, "bold"),
        bg="#dc3545", fg="white", width=12, height=2,
        command=sair_coordenador
    ).pack(pady=40)

    # Intercepta o clique no X
    coord_tela.protocol("WM_DELETE_WINDOW", sair_coordenador)





# ---------------------- GERENCIAR TURMAS ----------------------
def abrir_tela_turmas(parent):
    turma_tela = tk.Toplevel(parent)
    turma_tela.title("Gerenciamento de Turmas")
    turma_tela.geometry("800x500")
    turma_tela.configure(bg="#f8f9fa")
    turma_tela.grab_set()

    tree = ttk.Treeview(turma_tela, columns=("Nome", "Descrição"), show="headings")
    tree.heading("Nome", text="Nome da Turma")
    tree.heading("Descrição", text="Descrição")
    tree.pack(fill="both", expand=True, pady=10)

    # Carrega turmas do CSV
    if os.path.exists("turmas.csv"):
        with open("turmas.csv", "r", encoding="utf-8") as f:
            leitor = csv.reader(f)
            for linha in leitor:
                if len(linha) >= 2:
                    tree.insert("", "end", values=(linha[0], linha[1]))

    def cadastrar_turma():
        cad_tela = tk.Toplevel(turma_tela)
        cad_tela.title("Cadastrar Nova Turma")
        cad_tela.geometry("400x250")
        cad_tela.grab_set()

        tk.Label(cad_tela, text="Nome da Turma:").pack(pady=5)
        entrada_nome = tk.Entry(cad_tela, width=30)
        entrada_nome.pack(pady=5)

        tk.Label(cad_tela, text="Descrição:").pack(pady=5)
        entrada_desc = tk.Entry(cad_tela, width=30)
        entrada_desc.pack(pady=5)

        def salvar_turma():
            nome = entrada_nome.get().strip()
            desc = entrada_desc.get().strip()

            if not nome:
                messagebox.showwarning("Aviso", "O nome da turma não pode estar vazio!")
                return

            # Verifica duplicidade
            if os.path.exists("turmas.csv"):
                with open("turmas.csv", "r", encoding="utf-8") as f:
                    for linha in csv.reader(f):
                        if len(linha) >= 1 and linha[0] == nome:
                            messagebox.showerror("Erro", "Esta turma já existe!")
                            return

            # Salva no CSV
            with open("turmas.csv", "a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow([nome, desc])

            tree.insert("", "end", values=(nome, desc))
            messagebox.showinfo("Sucesso", "Turma cadastrada com sucesso!")
            cad_tela.destroy()

        tk.Button(cad_tela, text="Salvar", bg="#28a745", fg="white", command=salvar_turma).pack(pady=10)

    def gerenciar_alunos():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma turma!")
            return
        turma_nome = tree.item(selecionado)["values"][0]
        gerenciar_alunos_turma(turma_tela, turma_nome)

    tk.Button(turma_tela, text="Cadastrar Turma", bg="#28a745", fg="white", command=cadastrar_turma).pack(pady=5)
    tk.Button(turma_tela, text="Gerenciar Alunos da Turma", bg="#007bff", fg="white", command=gerenciar_alunos).pack(pady=5)

# ---------------------- GERENCIAR ALUNOS DA TURMA ----------------------
def gerenciar_alunos_turma(parent, turma_nome):
    ger_tela = tk.Toplevel(parent)
    ger_tela.title(f"Alunos da Turma: {turma_nome}")
    ger_tela.geometry("800x500")
    ger_tela.configure(bg="#f8f9fa")
    ger_tela.grab_set()

    tk.Label(ger_tela, text=f"Turma: {turma_nome}", font=("Arial", 12, "bold"), bg="#f8f9fa").pack(pady=10)

    frame = tk.Frame(ger_tela, bg="#f8f9fa")
    frame.pack(fill="both", expand=True, pady=10)

    lista_alunos = tk.Listbox(frame, width=40)
    lista_alunos.pack(side="left", fill="both", expand=True, padx=10)

    # Carregar alunos da turma
    alunos_turma = []
    if os.path.exists("turma_alunos.csv"):
        with open("turma_alunos.csv", "r", encoding="utf-8") as f:
            for nome, turma in csv.reader(f):
                if turma == turma_nome:
                    alunos_turma.append(nome)
                    lista_alunos.insert("end", nome)

    # Carregar todos os alunos
    alunos_totais = []
    if os.path.exists("alunos.csv"):
        with open("alunos.csv", "r", encoding="utf-8") as f:
            for linha in csv.reader(f):
                if len(linha) >= 1:
                    alunos_totais.append(linha[0])

    # Selecionar aluno para adicionar
    def adicionar_aluno():
        add_tela = tk.Toplevel(ger_tela)
        add_tela.title("Adicionar Aluno à Turma")
        add_tela.geometry("400x300")
        add_tela.grab_set()

        tk.Label(add_tela, text="Selecione o Aluno:").pack(pady=5)
        combo = ttk.Combobox(add_tela, values=[a for a in alunos_totais if a not in alunos_turma], width=30)
        combo.pack(pady=10)

        def salvar_aluno():
            nome = combo.get()
            if not nome:
                messagebox.showwarning("Aviso", "Selecione um aluno!")
                return

            with open("turma_alunos.csv", "a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow([nome, turma_nome])

            alunos_turma.append(nome)
            lista_alunos.insert("end", nome)
            messagebox.showinfo("Sucesso", f"{nome} adicionado à turma {turma_nome}!")
            add_tela.destroy()

        tk.Button(add_tela, text="Adicionar", bg="#28a745", fg="white", command=salvar_aluno).pack(pady=10)

    def remover_aluno():
        selecionado = lista_alunos.curselection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um aluno para remover!")
            return
        nome = lista_alunos.get(selecionado)
        lista_alunos.delete(selecionado)
        alunos_turma.remove(nome)

        # Atualiza CSV
        novos_dados = []
        if os.path.exists("turma_alunos.csv"):
            with open("turma_alunos.csv", "r", encoding="utf-8") as f:
                for linha in csv.reader(f):
                    if len(linha) >= 2 and not (linha[0] == nome and linha[1] == turma_nome):
                        novos_dados.append(linha)
        with open("turma_alunos.csv", "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerows(novos_dados)

        messagebox.showinfo("Removido", f"{nome} foi removido da turma {turma_nome}!")

    tk.Button(ger_tela, text="Adicionar Aluno", bg="#28a745", fg="white", command=adicionar_aluno).pack(pady=5)
    tk.Button(ger_tela, text="Remover Aluno", bg="#dc3545", fg="white", command=remover_aluno).pack(pady=5)

# ---------------------- FUNÇÕES EXISTENTES ----------------------
def mostrar_disciplinas():
    try:
        with open("disciplinas.csv", "r", encoding="utf-8") as f:
            disciplinas = [linha[0] for linha in csv.reader(f)]
        messagebox.showinfo("Disciplinas", "\n".join(disciplinas) if disciplinas else "Nenhuma disciplina cadastrada.")
    except:
        messagebox.showinfo("Disciplinas", "Nenhuma disciplina cadastrada.")

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

    # ---------------------- EDITAR ----------------------
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

    # ---------------------- EXCLUIR ----------------------
    def excluir_usuario():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um usuário para excluir!")
            return

        if not messagebox.askyesno("Confirmação", "Deseja realmente excluir este usuário?"):
            return

        item = tree.item(selecionado)
        email_atual = item["values"][1]

        # Atualiza CSV removendo o usuário
        dados = []
        with open(arquivo, "r", encoding="utf-8") as f:
            leitor = csv.reader(f)
            for linha in leitor:
                if len(linha) >= 2 and linha[1] != email_atual:
                    dados.append(linha)
        with open(arquivo, "w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerows(dados)

        # Remove do Treeview
        tree.delete(selecionado)
        messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")

    # Botões Editar e Excluir
    tk.Button(lista_tela, text="Editar", bg="#ffc107", fg="black", command=editar_usuario).pack(pady=5)
    tk.Button(lista_tela, text="Excluir", bg="#dc3545", fg="white", command=excluir_usuario).pack(pady=5)


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

# ---------------------- FRAME PRINCIPAL ----------------------
frame_principal = tk.Frame(janela, bg="#055bb8")
frame_principal.place(relx=0.5, rely=0.5, anchor="center")

# ---------------------- LOGO NO TOPO ----------------------
if os.path.exists("Copilot_20251025_113657-removebg-preview.png"):
    logo_img = Image.open("Copilot_20251025_113657-removebg-preview.png")
    logo_img = logo_img.resize((250, 250), resample_method)
    logo = ImageTk.PhotoImage(logo_img)
    label_logo = tk.Label(frame_principal, image=logo, bg="#055bb8")
    label_logo.grid(row=0, column=0, pady=(0, 20))  # Espaço entre logo e login

# ---------------------- FRAME DE LOGIN ----------------------
frame_login = tk.Frame(frame_principal, bg="#055bb8", bd=50)
frame_login.grid(row=1, column=0)

tk.Label(frame_login, text="Email:", fg="white", font=("Arial", 15), bg="#055bb8").grid(row=0, column=0, sticky="w", pady=5)
entrada_email = tk.Entry(frame_login, width=30)
entrada_email.grid(row=0, column=1, pady=5)

tk.Label(frame_login, text="Senha:", fg="white", font=("Arial", 15), bg="#055bb8").grid(row=1, column=0, sticky="w", pady=5)
entrada_senha = tk.Entry(frame_login, show="*", width=30)
entrada_senha.grid(row=1, column=1, pady=5)

tk.Label(frame_login, text="Tipo de usuário:", fg="white", font=("Arial", 15), bg="#055bb8").grid(row=2, column=0, sticky="w", pady=5)

var_tipo = tk.StringVar(value="Aluno")

tk.Radiobutton(frame_login, text="Aluno",  font=("Arial", 13), variable=var_tipo, value="Aluno", bg="#055bb8").grid(row=3, column=1, sticky="w", pady=2)
tk.Radiobutton(frame_login, text="Professor", font=("Arial", 13), variable=var_tipo, value="Professor", bg="#055bb8").grid(row=4, column=1, sticky="w", pady=2)
tk.Radiobutton(frame_login, text="Administrador", font=("Arial", 13), variable=var_tipo, value="Administrador", bg="#055bb8").grid(row=5, column=1, sticky="w", pady=2)
tk.Radiobutton(frame_login, text="Coordenador", font=("Arial", 13), variable=var_tipo, value="Coordenador", bg="#055bb8").grid(row=6, column=1, sticky="w", pady=2)

botao_login = tk.Button(frame_login, text="ENTRAR", font=("Arial", 15), bg="#15ff00", fg="white", width=15, command=verificar_login)
botao_login.grid(row=7, column=0, columnspan=3, pady=10)

# ---------------------- BOTÃO ESQUECI MINHA SENHA ----------------------
def esqueci_senha():
    messagebox.showinfo("Recuperar Senha", "Por favor, entre em contato com o coordenador para redefinir sua senha.")

botao_esqueci = tk.Button(frame_login, text="Esqueci minha senha", font=("Arial", 12, "underline"), fg="white", bg="#055bb8",
                          bd=0, cursor="hand2", command=esqueci_senha)
botao_esqueci.grid(row=8, column=0, columnspan=3, pady=5)

# ---------------------- CONFIRMAÇÃO AO FECHAR ----------------------
def confirmar_saida():
    resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja sair do sistema?")
    if resposta:
        janela.destroy()

janela.protocol("WM_DELETE_WINDOW", confirmar_saida)


janela.mainloop()
