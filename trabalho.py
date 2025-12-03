#!/usr/bin/env python3
"""
crud_console.py
Esqueleto de CRUD em console usando PostgreSQL.
Sistema de relatos cívicos e pontos de benefícios.
"""

import psycopg2
import datetime
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
    """
    DEPRECATED: Database initialization now handled by migration files.
    Use 'make migrate-all' to create schema and populate data.
    """
    print("\n⚠️  Warning: init_db() is deprecated.")
    print("Database schema is now managed through migration files.")
    print("\nTo initialize the database, run:")
    print("  make migrate-all")
    print("\nFor a fresh start:")
    print("  make migrate-reset")
    print()

def check_db_ready():
    """
    Verify that database has been migrated and contains data.
    Returns True if ready, False otherwise with helpful error messages.
    """
    try:
        with get_connection() as conn:
            cur = conn.cursor()

            # Check if core tables exist
            cur.execute("""
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name IN ('usuario', 'report', 'cidadao')
            """)
            table_count = cur.fetchone()[0]

            if table_count < 3:
                print("\n❌ Database not initialized!")
                print("Core tables are missing.")
                print("\nRun: make migrate-all")
                return False

            # Check if data exists
            cur.execute("SELECT COUNT(*) FROM Usuario")
            user_count = cur.fetchone()[0]

            if user_count == 0:
                print("\n⚠️  Database has no data!")
                print("Tables exist but are empty.")
                print("\nRun: make migrate-data")
                return False

            return True

    except psycopg2.OperationalError as e:
        print("\n❌ Cannot connect to database!")
        print(f"Error: {e}")
        print("\nMake sure PostgreSQL is running:")
        print("  make db-up")
        return False
    except Exception as e:
        print(f"\n❌ Database error: {e}")
        print("\nTry rebuilding the database:")
        print("  make migrate-reset")
        return False

# -------------------------
# Adicionando dados(é o Fábio escrevendo nao o gepeto)
# -------------------------
def inserir_usuario(user: Usuario) -> int:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO Usuario (CAMPOS) VALUES (%s, %s, %s, %s, %s)",
                    (user.CPF, user.name, user.email, user.dataNasc, user.role))
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
    print("Funcionalidade de criação em desenvolvimento.")
    pass

def handle_view():
    try:
        print("Funcionalidade de visualização em desenvolvimento.")
        pass
    except ValueError:
        print("Erro ao visualizar dados.")
        pass


def main_loop():
    """Main application loop with database validation."""
    print("\n" + "="*50)
    print("    SISTEMA DE RELATOS CÍVICOS")
    print("="*50)

    # Validate database is ready before starting
    if not check_db_ready():
        print("\n⚠️  Cannot start application due to database issues.")
        print("Please fix the database first.\n")
        return

    print("✅ Database ready!\n")

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
