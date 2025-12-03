#!/usr/bin/env python3
"""
crud_console.py
Esqueleto de CRUD em console usando PostgreSQL.
Sistema de relatos cívicos e pontos de benefícios.
"""

import psycopg2
import datetime
import os
from dataclasses import dataclass
from typing import Optional, List

# PostgreSQL connection configuration (Docker container)
DB_CONFIG = {
    'dbname': 'trabalho_db',
    'user': 'trabalho_user',
    'password': 'trabalho_pass',
    'host': 'localhost',
    'port': 5432
}

@dataclass
class Usuario:
    CPF: str
    name: str
    email: str
    dataNasc: datetime.date
    role: str

@dataclass
class Funcionario:
    CPF: str
    setor: str
    cidade: str

@dataclass
class Cidadao:
    CPF: str
    pontos: int

@dataclass
class Beneficios:
    nome_benficio: str
    pontos: int
    descricao: str

@dataclass
class Interacao:
    idInteracao: str
    CPF: str
    tipo: str
    data: datetime.date
    idReport: str

@dataclass
class Comentario:
    idInteracao: str
    texto: str
    data: datetime.date

@dataclass
class Avaliacao:
    idInteracao: str
    data: datetime.date
    nota: str
    cometario: str

@dataclass
class Report:
    idReport: str
    titulo: str
    localizacao: str
    data: datetime.date
    status: str
    idCategoriaReport: str
    descricao: str


@dataclass
class Midia:
    link: str
    idReport: str
    dataUpload: datetime.date

@dataclass
class CategoriaReport:
    idCategoriaReport: str
    nome: str
    pontos: int

@dataclass
class HistoricoAtualizado:
    funcionario: str
    idReport: str
    dataUpload: datetime.date
    atributoAtualizado: str


@dataclass
class CidadaoBeneficio:
    cpf: str
    nomeBeneficio: str
    data: datetime.date

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    with get_connection() as conn:
        cur = conn.cursor()
        # SQL DE CREATE TABLES(aqui tbm é o Fábio)
        cur.execute("""
            
        """)
        conn.commit()

# -------------------------
# Adicionando dados(é o Fábio escrevendo nao o gepeto)
# -------------------------
def inserir_usuario() -> int:
    with get_connection() as conn:
        clear_console()
        print("Inserindo usuario")
        user = Usuario()
        user.CPF = input("CPF: ").strip()
        user.name = input("Nome: ").strip()
        user.email = input("Email: ").strip()
        user.dataNasc = input("Data de Nascimento: ").strip()
        user.role = input("Role: ").strip()
        cur = conn.cursor()
        cur.execute("INSERT INTO Usuario (CAMPOS) VALUES (%s, %s, %s, %s, %s)",
                    (user.CPF, user.name, user.email, user.dataNasc, user.role))
        conn.commit()
        return cur.lastrowid

def inserir_funcionario() -> int:
    with get_connection() as conn:
        clear_console()
        print("Inserindo funcionario")

        func = Funcionario()
        func.CPF = input("CPF: ").strip()
        func.setor = input("Setor: ").strip()
        func.cidade = input("Cidade: ").strip()
        cur = conn.cursor()
        cur.execute("INSERT INTO Funcionario VALUES (%s, %s, %s)",
                    (func.CPF, func.setor, func.cidade))
        conn.commit()
        return cur.lastrowid


def inserir_cidadao() -> int:
    with get_connection() as conn:
        clear_console()
        print("Inserindo cidadao")

        cidadao = Cidadao()
        cidadao.CPF = input("CPF: ").strip()
        cidadao.pontos = input("Pontos: ").strip()
        cur = conn.cursor()
        cur.execute("INSERT INTO Cidadao VALUES (%s, %s)",
                    (cidadao.CPF, cidadao.pontos))
        conn.commit()
        return cur.lastrowid


def inserir_beneficios() -> int:
    with get_connection() as conn:
        clear_console()
        print("Inserindo beneficio")

        beneficio = Beneficios()
        beneficio.nome_benficio = input("Nome: ").strip()
        beneficio.pontos = input("Pontos: ").strip()
        beneficio.descricao = input("Descricao: ").strip()

        cur = conn.cursor()
        cur.execute("INSERT INTO Beneficios VALUES (%s, %s, %s)",
                    (beneficio.nome_benficio, beneficio.pontos, beneficio.descricao))
        conn.commit()
        return cur.lastrowid

def inserir_interacao() -> int:
    with get_connection() as conn:
        clear_console()
        print("Inserindo interacao")

        interacao = Interacao()
        interacao.CPF = input("Pontos: ").strip()
        interacao.tipo = input("Descricao: ").strip()
        interacao.data = datetime.now()
        interacao.idReport = input("idReport: ").strip()

        cur = conn.cursor()
        cur.execute("INSERT INTO Interacao VALUES (%s, %s, %s, %s, %s)",
                    ( interacao.CPF, interacao.tipo, interacao.data, interacao.idReport))
        conn.commit()
        return cur.lastrowid

def inserir_comentario() -> int:
    with get_connection() as conn:
        clear_console()
        print("Inserindo comentario")

        comentario = Comentario()
        comentario.idInteracao = input("Id: ").strip()
        comentario.texto = input("Texto: ").strip()
        comentario.data = datetime.now()

        cur = conn.cursor()
        cur.execute("INSERT INTO Comentario VALUES (%s, %s, %s)",
                    (comentario.idInteracao, comentario.texto, comentario.data))
        conn.commit()
        return cur.lastrowid

def inserir_avaliacao() -> int:
    with get_connection() as conn:
        clear_console()
        print("Inserindo avaliacao")

        avalicao = Avaliacao()
        avalicao.idInteracao = input("Id: ").strip()
        avalicao.nota = input("Nota: ").strip()
        avalicao.cometario = input("Comentaio: ").strip()
        avalicao.data = datetime.now()

        cur = conn.cursor()
        cur.execute("INSERT INTO Avaliacao VALUES (%s, %s, %s, %s)",
                    (avalicao.idInteracao, avalicao.data, avalicao.nota, avalicao.cometario))
        conn.commit()
        return cur.lastrowid

def inserir_report() -> int:
    with get_connection() as conn:
        clear_console()
        print("Inserindo report")

        report = Report()
        report.titulo = input("Titulo: ").strip()
        report.localizacao = input("Localizacao: ").strip()
        report.data = datetime.now()
        report.status = input("Status: ").strip()
        report.idCategoriaReport = input("idCategoriaReport: ").strip()
        report.descricao = input("Descricao: ").strip()


        cur = conn.cursor()
        cur.execute("INSERT INTO Report VALUES (%s, %s, %s, %s, %s, %s)",
                    (report.titulo, report.localizacao, report.data, report.status, report.idCategoriaReport, report.descricao))
        conn.commit()
        return cur.lastrowid

def inserir_midia() -> int:
    with get_connection() as conn:
        clear_console()
        print("Inserindo midia")

        midia = Midia()
        midia.link = input("Link: ").strip()
        midia.idReport = input("idReport: ").strip()
        midia.dataUpload = datetime.now()

        cur = conn.cursor()
        cur.execute("INSERT INTO Midia VALUES (%s, %s, %s)",
                    (midia.link, midia.idReport, midia.dataUpload))
        conn.commit()
        return cur.lastrowid

def inserir_categoriaReport() -> int:
    with get_connection() as conn:
        clear_console()
        print("Inserindo categoriaReport")

        categoriaReport = CategoriaReport()
        categoriaReport.nome = input("Nome: ").strip()
        categoriaReport.pontos = input("Pontos: ").strip()

        cur = conn.cursor()
        cur.execute("INSERT INTO CategoriaReport VALUES (%s, %s)",
                    (categoriaReport.nome, categoriaReport.pontos))
        conn.commit()
        return cur.lastrowid

@dataclass
class HistoricoAtualizado:
    funcionario: str
    idReport: str
    dataUpload: datetime.date
    atributoAtualizado: str

def inserir_historicoAtualizado() -> int:
    with get_connection() as conn:
        clear_console()
        print("Inserindo HistoricoAtualizado")

        historicoAtualizado = HistoricoAtualizado()
        historicoAtualizado.funcionario = input("Funcionario: ").strip()
        historicoAtualizado.idReport = input("idReport: ").strip()
        historicoAtualizado.dataUpload = datetime.now()
        historicoAtualizado.atributoAtualizado = input("Atributo Atualizado: ").strip()


        cur = conn.cursor()
        cur.execute("INSERT INTO HistoricoAtualizado VALUES (%s, %s, %s, %s)",
                    ( historicoAtualizado.funcionario,  historicoAtualizado.idReport,  historicoAtualizado.dataUpload,  historicoAtualizado.atributoAtualizado))
        conn.commit()
        return cur.lastrowid

def inserir_cidadaoBeneficio() -> int:
    with get_connection() as conn:
        clear_console()
        print("Inserindo CidadaoBeneficio")

        cidadaoBeneficio = CidadaoBeneficio()
        cidadaoBeneficio.cpf = input("CPF: ").strip()
        cidadaoBeneficio.nomeBeneficio = input("Nome do beneficio: ").strip()
        cidadaoBeneficio.dataUpload = datetime.now()


        cur = conn.cursor()
        cur.execute("INSERT INTO CidadaoBeneficio VALUES (%s, %s, %s)",
                    ( cidadaoBeneficio.cpf, cidadaoBeneficio.nomeBeneficio,  cidadaoBeneficio.dataUpload))
        conn.commit()
        return cur.lastrowid

def select_usuario(item_id: int) -> Optional[user]:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, description FROM items WHERE id = %s", (item_id,))
        row = cur.fetchone()
        return user(*row) if row else None

def list_usuarios() -> List[user]:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Usuario ORDER BY nome")
        rows = cur.fetchall()
        return [user(*r) for r in rows]


def input_nonempty(prompt: str) -> str:
    while True:
        v = input(prompt).strip()
        if v:
            return v
        print("Valor não pode ser vazio. Tente novamente.")

def menu():
    print("\n=== CRUD Console ===")
    print("1) Listar todos")
    print("2) Criar novo dado")
    print("3) Select")
    print("0) Sair")

def handle_list():
    users = list_usuarios()
    if not users:
        print("Nenhum item cadastrado.")
        return
    print("\nItens:")
    for it in users:
        print()

def handle_create():
    print("Selecione em qual tabela você deseja adiocionar um dado: ")
    print("1- Usuario")
    print("2- Funcionario")
    print("3- Cidadao")
    print("4- Beneficio")
    print("5- Interacao")
    print("6- Comentario")
    print("7- Avaliacao")
    print("8- Report")
    print("9- Midia")
    print("10- CategoriaReport")
    print("11- HistoricoAtualizado")
    print("12- CidadaoBeneficio")
    print("0- Sair")
    choice = input("Escolha: ").strip()
    match choice:
        case "1":
            inserir_usuario()
        case "2":
            inserir_funcionario()
        case "3":
            inserir_cidadao()
        case "4":
            inserir_beneficio()
        case "5":
            inserir_interacao()
        case "6":
            inserir_comentario()
        case "7":
            inserir_avaliacao()
        case "8":
            inserir_report()
        case "9":
            inserir_midia()
        case "10":
            inserir_categoriaReport()
        case "11":
            inserir_historicoAtualizado()
        case "12":
            inserir_cidadeBeneficio()
        case "0":
            pass


def handle_view():
    try:
    except ValueError:

def clear_console():
    """Clears the console screen."""
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For macOS and Linux
    else:
        os.system('clear')

def main_loop():
    init_db()
    while True:
        menu()
        choice = input("Escolha: ").strip()
        if choice == "1":
            handle_list()
        elif choice == "2":
            handle_create()
        elif choice == "3":
            handle_view()
        elif choice == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main_loop()
