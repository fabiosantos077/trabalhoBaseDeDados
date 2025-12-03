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
    'port': 5435
}

@dataclass
class Usuario:
    cpf: str
    nome: str
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
def inserir_usuario() -> int:
    with get_connection() as conn:
        clear_console()
        print("Inserindo Usuario")
        cpf = input("CPF: ").strip()
        nome = input("Nome: ").strip()
        email = input("Email: ").strip()
        data_nasc = input("Data de Nascimento (AAAA-MM-DD): ").strip()
        role = input("Role (Cidadao/Funcionario): ").strip()
        
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Usuario (cpf, nome, email, dataNascimento, role) 
            VALUES (%s, %s, %s, %s, %s)
        """, (cpf, nome, email, data_nasc, role))
        conn.commit()
        return cur.rowcount

def inserir_funcionario() -> int:
    with get_connection() as conn:
        clear_console()
        print("Inserindo Funcionario")
        cpf = input("CPF: ").strip()
        setor = input("Setor: ").strip()
        cidade = input("Cidade: ").strip()
        
        cur = conn.cursor()
        cur.execute("INSERT INTO Funcionario (cpf, setor, cidade) VALUES (%s, %s, %s)",
                    (cpf, setor, cidade))
        conn.commit()
        return cur.rowcount

def inserir_cidadao() -> int:
    with get_connection() as conn:
        clear_console()
        print("Inserindo Cidadao")
        cpf = input("CPF: ").strip()
        pontos = input("Pontos: ").strip()
        
        cur = conn.cursor()
        cur.execute("INSERT INTO Cidadao (cpf, pontos) VALUES (%s, %s)",
                    (cpf, pontos))
        conn.commit()
        return cur.rowcount

def inserir_beneficio() -> int:
    with get_connection() as conn:
        clear_console()
        print("Inserindo Beneficio")
        nome = input("Nome: ").strip()
        custo = input("Custo (Pontos): ").strip()
        descricao = input("Descricao: ").strip()

        cur = conn.cursor()
        cur.execute("INSERT INTO Beneficio (nomeBeneficio, custo, descricao) VALUES (%s, %s, %s)",
                    (nome, custo, descricao))
        conn.commit()
        return cur.rowcount

def inserir_interacao() -> int:
    with get_connection() as conn:
        clear_console()
        print("Inserindo Interacao")
        cpf = input("CPF do Cidadão: ").strip()
        id_report = input("ID do Report: ").strip()
        tipo = input("Tipo (Comentario/Upvote/Avaliacao): ").strip()
        data = datetime.datetime.now()

        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Interacao (cpfCidadao, idReport, tipo, dataHora) 
            VALUES (%s, %s, %s, %s) RETURNING idInteracao
        """, (cpf, id_report, tipo, data))
        
        new_id = cur.fetchone()[0]
        conn.commit()
        print(f"ID Gerado: {new_id}")
        return new_id

def inserir_comentario() -> int:
    with get_connection() as conn:
        clear_console()
        print("Inserindo Comentario")
        id_interacao = input("Id da Interação: ").strip()
        texto = input("Texto: ").strip()

        cur = conn.cursor()
        cur.execute("INSERT INTO Comentario (idInteracao, texto) VALUES (%s, %s)",
                    (id_interacao, texto))
        conn.commit()
        return cur.rowcount

def inserir_avaliacao() -> int:
    with get_connection() as conn:
        clear_console()
        print("Inserindo Avaliacao")
        id_interacao = input("Id da Interação: ").strip()
        nota = input("Nota (1-5): ").strip()
        comentario = input("Comentario: ").strip()

        cur = conn.cursor()
        cur.execute("INSERT INTO Avaliacao (idInteracao, nota, comentario) VALUES (%s, %s, %s)",
                    (id_interacao, nota, comentario))
        conn.commit()
        return cur.rowcount

def inserir_report() -> int:
    with get_connection() as conn:
        clear_console()
        print("Inserindo Report")
        titulo = input("Titulo: ").strip()
        localizacao = input("Localizacao: ").strip()
        descricao = input("Descricao: ").strip()
        status = input("Status (Aberto/Em Análise/Resolvido/Fechado): ").strip()
        id_categoria = input("ID Categoria: ").strip()
        cpf_cidadao = input("CPF Cidadão: ").strip()
        data = datetime.datetime.now()

        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Report (titulo, localizacao, descricao, status, idCategoriaReport, cpfCidadao, dataCriacao) 
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING idReport
        """, (titulo, localizacao, descricao, status, id_categoria, cpf_cidadao, data))
        
        new_id = cur.fetchone()[0]
        conn.commit()
        print(f"ID Gerado: {new_id}")
        return new_id

def inserir_midia() -> int:
    with get_connection() as conn:
        clear_console()
        print("Inserindo Midia")
        link = input("Link: ").strip()
        id_report = input("ID Report: ").strip()
        data = datetime.datetime.now()

        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Midia (link, idReport, dataUpload) 
            VALUES (%s, %s, %s) RETURNING idMidia
        """, (link, id_report, data))
        
        new_id = cur.fetchone()[0]
        conn.commit()
        print(f"ID Gerado: {new_id}")
        return new_id

def inserir_categoriaReport() -> int:
    with get_connection() as conn:
        clear_console()
        print("Inserindo CategoriaReport")
        nome = input("Nome: ").strip()
        pontos = input("Pontos: ").strip()

        cur = conn.cursor()
        cur.execute("""
            INSERT INTO CategoriaReport (nome, pontos) 
            VALUES (%s, %s) RETURNING idCategoriaReport
        """, (nome, pontos))
        
        new_id = cur.fetchone()[0]
        conn.commit()
        print(f"ID Gerado: {new_id}")
        return new_id

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
        funcionario = input("CPF Funcionario: ").strip()
        id_report = input("idReport: ").strip()
        atributo = input("Atributo Atualizado: ").strip()
        data = datetime.datetime.now()

        cur = conn.cursor()
        cur.execute("""
            INSERT INTO HistoricoAtualizacao (cpfFuncionario, idReport, dataHoraAtualizacao, atributoAtualizado) 
            VALUES (%s, %s, %s, %s)
        """, (funcionario, id_report, data, atributo))
        conn.commit()
        return cur.rowcount

def inserir_cidadaoBeneficio() -> int:
    with get_connection() as conn:
        clear_console()
        print("Inserindo CidadaoBeneficio")
        cpf = input("CPF: ").strip()
        nome_beneficio = input("Nome do beneficio: ").strip()
        pontos = input("Pontos Resgatados: ").strip()
        data = datetime.datetime.now()

        cur = conn.cursor()
        cur.execute("""
            INSERT INTO CidadaoBeneficio (cpfCidadao, nomeBeneficio, pontosResgatados, dataHoraResgate) 
            VALUES (%s, %s, %s, %s)
        """, (cpf, nome_beneficio, pontos, data))
        conn.commit()
        return cur.rowcount
        
def select_usuario(item_id: int) -> Optional[Usuario]:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, description FROM items WHERE id = %s", (item_id,))
        row = cur.fetchone()
        return user(*row) if row else None

def list_usuarios() -> List[Usuario]:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Usuario ORDER BY nome")
        rows = cur.fetchall()
        return [Usuario(*r) for r in rows]


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
    print("\Lista de Usuários:")
    for u in users:
        print(f"Nome: {u.nome} | CPF: {u.cpf} | Role: {u.role}")

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
    if choice == "1":
        inserir_usuario()
    elif choice == "2":
        inserir_funcionario()
    elif choice == "3":
        inserir_cidadao()
    elif choice == "4":
        inserir_beneficio()
    elif choice == "5":
        inserir_interacao()
    elif choice == "6":
        inserir_comentario()
    elif choice == "7":
        inserir_avaliacao()
    elif choice == "8":
        inserir_report()
    elif choice == "9":
        inserir_midia()
    elif choice == "10":
        inserir_categoriaReport()
    elif choice == "11":
        inserir_historicoAtualizado()
    elif choice == "12":
        inserir_cidadaoBeneficio()
    elif choice == "0":
        pass


def handle_view():
    try:
        print("Funcionalidade de visualização em desenvolvimento.")
        pass
    except ValueError:
        print("Erro ao visualizar dados.")
        pass

def clear_console():
    """Clears the console screen."""
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For macOS and Linux
    else:
        os.system('clear')

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
