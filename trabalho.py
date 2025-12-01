#!/usr/bin/env python3
"""
crud_console.py
Esqueleto de CRUD em console usando sqlite3.
Modelo: "items" com campos id (inteiro autoincrement), name (texto), description (texto).
"""

import sqlite3
import datetime
from dataclasses import dataclass
from typing import Optional, List

DB_PATH = "exemplo.db"

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
    return sqlite3.connect(DB_PATH)

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
def inserir_usuario(Usuario: user) -> int:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO Usuario (CAMPOS) VALUES (?, ?)",
                    (user.CPF, user.name, user.email, user.dataNasc, user.role))
        conn.commit()
        return cur.lastrowid

def select_usuario(item_id: int) -> Optional[user]:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, description FROM items WHERE id = ?", (item_id,))
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

def handle_view():
    try:
    except ValueError:


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
