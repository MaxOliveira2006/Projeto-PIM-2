#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_NOME 100
#define MAX_EMAIL 100
#define MAX_SENHA 50
#define ARQ_ALUNOS "alunos.csv"
#define ARQ_PROFESSORES "professores.csv"
#define ARQ_ADMIN "administradores.csv"
#define ARQ_COORDENADORES "coordenadores.csv"

// Estruturas
typedef struct {
    char nome[MAX_NOME];
    char email[MAX_EMAIL];
    char senha[MAX_SENHA];
    int ra;
} Aluno;

typedef struct {
    char nome[MAX_NOME];
    char email[MAX_EMAIL];
    char senha[MAX_SENHA];
    int rp;
} Professor;

typedef struct {
    char nome[MAX_NOME];
    char email[MAX_EMAIL];
    char senha[MAX_SENHA];
    int id;
} Administrador;

typedef struct {
    char nome[MAX_NOME];
    char email[MAX_EMAIL];
    char senha[MAX_SENHA];
    int rc;
} Coordenador;

// Funções de ID
int gerarRA() { return 10000 + rand() % 90000; }
int gerarRP() { return 50000 + rand() % 90000; }
int gerarIDAdmin() { return 90000 + rand() % 10000; }
int gerarRC() { return 70000 + rand() % 10000; } // ID para coordenador

// Funções para salvar dados
void salvarAluno(Aluno a) {
    FILE *f = fopen(ARQ_ALUNOS, "a");
    if (!f) { printf("Erro ao abrir arquivo de alunos!\n"); return; }
    fprintf(f, "%s,%s,%s,A%d\n", a.nome, a.email, a.senha, a.ra);
    fclose(f);
}

void salvarProfessor(Professor p) {
    FILE *f = fopen(ARQ_PROFESSORES, "a");
    if (!f) { printf("Erro ao abrir arquivo de professores!\n"); return; }
    fprintf(f, "%s,%s,%s,P%d\n", p.nome, p.email, p.senha, p.rp);
    fclose(f);
}

void salvarAdmin(Administrador ad) {
    FILE *f = fopen(ARQ_ADMIN, "a");
    if (!f) { printf("Erro ao abrir arquivo de administradores!\n"); return; }
    fprintf(f, "%s,%s,%s,ADM%d\n", ad.nome, ad.email, ad.senha, ad.id);
    fclose(f);
}

void salvarCoordenador(Coordenador c) {
    FILE *f = fopen(ARQ_COORDENADORES, "a");
    if (!f) { printf("Erro ao abrir arquivo de coordenadores!\n"); return; }
    fprintf(f, "%s,%s,%s,C%d\n", c.nome, c.email, c.senha, c.rc);
    fclose(f);
}

int main() {
    srand(time(NULL));
    int opcao;

    printf("=== SISTEMA DE CADASTRO ===\n");
    printf("1 - Cadastrar Aluno\n");
    printf("2 - Cadastrar Professor\n");
    printf("3 - Cadastrar Administrador\n");
    printf("4 - Cadastrar Coordenador\n");
    printf("Escolha: ");
    scanf("%d", &opcao);
    getchar(); // limpar buffer

    if (opcao == 1) {
        Aluno aluno;

        printf("\nNome: ");
        fgets(aluno.nome, MAX_NOME, stdin);
        aluno.nome[strcspn(aluno.nome, "\n")] = 0;

        printf("Email: ");
        fgets(aluno.email, MAX_EMAIL, stdin);
        aluno.email[strcspn(aluno.email, "\n")] = 0;

        printf("Senha: ");
        fgets(aluno.senha, MAX_SENHA, stdin);
        aluno.senha[strcspn(aluno.senha, "\n")] = 0;

        aluno.ra = gerarRA();
        salvarAluno(aluno);

        printf("\nAluno cadastrado com sucesso!\nRA: A%d\n", aluno.ra);

    } else if (opcao == 2) {
        Professor prof;

        printf("\nNome: ");
        fgets(prof.nome, MAX_NOME, stdin);
        prof.nome[strcspn(prof.nome, "\n")] = 0;

        printf("Email: ");
        fgets(prof.email, MAX_EMAIL, stdin);
        prof.email[strcspn(prof.email, "\n")] = 0;

        printf("Senha: ");
        fgets(prof.senha, MAX_SENHA, stdin);
        prof.senha[strcspn(prof.senha, "\n")] = 0;

        prof.rp = gerarRP();
        salvarProfessor(prof);

        printf("\nProfessor cadastrado com sucesso!\nRP: P%d\n", prof.rp);

    } else if (opcao == 3) {
        Administrador ad;

        printf("\nNome: ");
        fgets(ad.nome, MAX_NOME, stdin);
        ad.nome[strcspn(ad.nome, "\n")] = 0;

        printf("Email: ");
        fgets(ad.email, MAX_EMAIL, stdin);
        ad.email[strcspn(ad.email, "\n")] = 0;

        printf("Senha: ");
        fgets(ad.senha, MAX_SENHA, stdin);
        ad.senha[strcspn(ad.senha, "\n")] = 0;

        ad.id = gerarIDAdmin();
        salvarAdmin(ad);

        printf("\nAdministrador cadastrado com sucesso!\nID: ADM%d\n", ad.id);

    } else if (opcao == 4) {
        Coordenador coord;

        printf("\nNome: ");
        fgets(coord.nome, MAX_NOME, stdin);
        coord.nome[strcspn(coord.nome, "\n")] = 0;

        printf("Email: ");
        fgets(coord.email, MAX_EMAIL, stdin);
        coord.email[strcspn(coord.email, "\n")] = 0;

        printf("Senha: ");
        fgets(coord.senha, MAX_SENHA, stdin);
        coord.senha[strcspn(coord.senha, "\n")] = 0;

        coord.rc = gerarRC();
        salvarCoordenador(coord);

        printf("\nCoordenador cadastrado com sucesso!\nRC: C%d\n", coord.rc);

    } else {
        printf("\nOpcao invalida!\n");
    }

    return 0;
}
