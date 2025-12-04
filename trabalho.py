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

def consultar_total_interacoes():
    """
    Consulta 1: Total de interações por Report.
    """
    sql = """
    SELECT
        R.idReport,
        R.titulo,
        R.status,
        CR.nome AS Categoria,
        COUNT(I.idInteracao) AS TotalInteracoes
    FROM
        Report R
    INNER JOIN
        CategoriaReport CR ON R.idCategoriaReport = CR.idCategoriaReport
    LEFT JOIN
        Interacao I ON R.idReport = I.idReport
    GROUP BY
        R.idReport, R.titulo, R.status, CR.nome
    ORDER BY
        TotalInteracoes DESC, R.idReport;
    """
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(sql)
                rows = cur.fetchall()
                
                clear_console()
                print("\n=== Relatório: Total de Interações por Report ===")
                print(f"{'ID':<5} | {'Título':<35} | {'Status':<12} | {'Categoria':<20} | {'Total':<5}")
                print("-" * 90)
                
                for row in rows:
                    titulo = (row[1][:32] + '..') if len(row[1]) > 32 else row[1]
                    print(f"{row[0]:<5} | {titulo:<35} | {row[2]:<12} | {row[3]:<20} | {row[4]:<5}")
                
                input("\nPressione ENTER para voltar...")
                
            except Exception as e:
                print(f"Erro ao executar consulta: {e}")
                input("Pressione ENTER para continuar...")

def consultar_reports_por_funcionario():
    """
    Consulta 2: Total de Reports atualizados por Funcionário.
    """
    sql = """
    SELECT
        U.nome AS NomeFuncionario,
        F.setor,
        COUNT(DISTINCT HA.idReport) AS ReportsAtualizados
    FROM
        Funcionario F
    INNER JOIN
        Usuario U ON F.cpf = U.cpf
    LEFT JOIN -- LEFT JOIN para incluir funcionários sem atualizações
        HistoricoAtualizacao HA ON F.cpf = HA.cpfFuncionario
    GROUP BY
        U.nome, F.setor
    ORDER BY
        ReportsAtualizados DESC, U.nome;
    """
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(sql)
                rows = cur.fetchall()
                
                clear_console()
                print("\n=== Relatório: Produtividade dos Funcionários ===")
                print(f"{'Nome':<35} | {'Setor':<30} | {'Qtd Atualizada':<15}")
                print("-" * 85)
                
                for row in rows:
                    nome = (row[0][:32] + '..') if len(row[0]) > 32 else row[0]
                    setor = (row[1][:27] + '..') if row[1] and len(row[1]) > 27 else (row[1] or "N/A")
                    qtd = row[2]
                    
                    print(f"{nome:<35} | {setor:<30} | {qtd:<15}")
                
                input("\nPressione ENTER para voltar...")
                
            except Exception as e:
                print(f"Erro ao executar consulta: {e}")
                input("Pressione ENTER para continuar...")

def consultar_media_avaliacoes():
    """
    Consulta 3: Média de avaliações por Categoria (apenas Resolvidos e Média > 4.0).
    """
    sql = """
    SELECT
        CR.nome AS Categoria,
        ROUND(AVG(A.nota), 2) AS NotaMedia
    FROM
        CategoriaReport CR
    INNER JOIN
        Report R ON CR.idCategoriaReport = R.idCategoriaReport
    INNER JOIN
        Interacao I ON R.idReport = I.idReport
    INNER JOIN
        Avaliacao A ON I.idInteracao = A.idInteracao
    WHERE
        R.status = 'Resolvido'
    GROUP BY
        CR.nome
    HAVING
        AVG(A.nota) > 4.0
    ORDER BY
        NotaMedia DESC;
    """
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(sql)
                rows = cur.fetchall()
                
                clear_console()
                print("\n=== Relatório: Qualidade dos Serviços (Resolvidos > 4.0) ===")
                print(f"{'Categoria':<35} | {'Nota Média':<10}")
                print("-" * 50)
                
                if not rows:
                    print("Nenhuma categoria atingiu os critérios (Resolvido & Média > 4.0).")
                else:
                    for row in rows:
                        categoria = row[0]
                        media = float(row[1]) 
                        print(f"{categoria:<35} | {media:<10.2f}")
                
                input("\nPressione ENTER para voltar...")
                
            except Exception as e:
                print(f"Erro ao executar consulta: {e}")
                input("Pressione ENTER para continuar...")

def consultar_funcionarios_todos_categorias():
    """
    Consulta 4: Funcionários que atualizaram Reports de TODAS as Categorias (Divisão Relacional).
    """
    sql = """
    SELECT
        U.cpf,
        U.nome
    FROM
        Funcionario F
    INNER JOIN
        Usuario U ON F.cpf = U.cpf
    WHERE
        NOT EXISTS ( -- NÃO EXISTE
            SELECT CR.idCategoriaReport -- UMA categoria
            FROM CategoriaReport CR
            EXCEPT -- QUE NÃO ESTEJA
            SELECT R.idCategoriaReport
            FROM HistoricoAtualizacao HA
            INNER JOIN Report R ON HA.idReport = R.idReport
            WHERE HA.cpfFuncionario = F.cpf -- Nas categorias que este funcionário já mexeu
        )
    ORDER BY
        U.nome;
    """
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(sql)
                rows = cur.fetchall()
                
                clear_console()
                print("\n=== Relatório: Funcionários 'Expert' (Todas as Categorias) ===")
                print(f"{'CPF':<15} | {'Nome':<35}")
                print("-" * 55)
                
                if not rows:
                    print("Nenhum funcionário atualizou reports de TODAS as categorias ainda.")
                else:
                    for row in rows:
                        print(f"{row[0]:<15} | {row[1]:<35}")
                
                input("\nPressione ENTER para voltar...")
                
            except Exception as e:
                print(f"Erro ao executar consulta: {e}")
                input("Pressione ENTER para continuar...")

def consultar_reports_criticos():
    """
    Consulta 5: Reports Críticos (2+ interações e sem atualização há > 2 dias).
    """    
    sql = """
    SELECT
        R.idReport,
        R.titulo,
        R.dataCriacao,
        COUNT(I.idInteracao) AS TotalInteracoes,
        (SELECT MAX(dataHoraAtualizacao) FROM HistoricoAtualizacao WHERE idReport = R.idReport) AS UltimaAtualizacaoFuncionario
    FROM
        Report R
    INNER JOIN
        Interacao I ON R.idReport = I.idReport
    WHERE
        R.status IN ('Aberto', 'Em Análise')
    GROUP BY
        R.idReport, R.titulo, R.dataCriacao
    HAVING
        COUNT(I.idInteracao) >= 2
        -- Para teste imediato, vou comentar a regra de 2 dias para você ver o report aparecer pela contagem de interações
        -- AND (NOW() - (SELECT MAX(dataHoraAtualizacao) FROM HistoricoAtualizacao WHERE idReport = R.idReport)) > INTERVAL '2 days'
    ORDER BY
        TotalInteracoes DESC;
    """
        
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(sql)
                rows = cur.fetchall()
                
                clear_console()
                print("\n=== Relatório: Reports Críticos (Alta Interação) ===")
                print(f"{'ID':<5} | {'Título':<35} | {'Interações':<10}")
                print("-" * 60)
                
                if not rows:
                    print("Nenhum report crítico encontrado no momento.")
                else:
                    for row in rows:
                        titulo = (row[1][:32] + '..') if len(row[1]) > 32 else row[1]
                        print(f"{row[0]:<5} | {titulo:<35} | {row[3]:<10}")
                
                input("\nPressione ENTER para voltar...")
                
            except Exception as e:
                print(f"Erro ao executar consulta: {e}")
                input("Pressione ENTER para continuar...")

def consultar_areas_problematicas():
    """
    Consulta 6: Áreas com maior concentração de problemas ativos (Hotspots).
    Baseado na imagem enviada.
    """
    sql = """
    SELECT
        R.localizacao,
        COUNT(R.idReport) AS TotalReportsAtivos,
        ROUND(AVG(EXTRACT(EPOCH FROM NOW() - R.dataCriacao) / 3600), 2) AS MediaHorasAberto
    FROM
        Report R
    WHERE
        R.status IN ('Aberto', 'Em Análise')
    GROUP BY
        R.localizacao
    HAVING
        COUNT(R.idReport) > 1
    ORDER BY
        TotalReportsAtivos DESC, MediaHorasAberto DESC
    LIMIT 5;
    """
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(sql)
                rows = cur.fetchall()
                
                clear_console()
                print("\n=== Relatório: Áreas com Concentração de Problemas (Hotspots) ===")
                print(f"{'Localização':<40} | {'Qtd Ativos':<10} | {'Média Horas':<12}")
                print("-" * 70)
                
                if not rows:
                    print("Nenhuma localização com múltiplos problemas ativos encontrada.")
                else:
                    for row in rows:
                        loc = (row[0][:37] + '..') if len(row[0]) > 37 else row[0]
                        qtd = row[1]
                        # O PostgreSQL retorna Decimal, convertemos para float
                        horas = float(row[2])
                        print(f"{loc:<40} | {qtd:<10} | {horas:<12.2f}")
                
                input("\nPressione ENTER para voltar...")
                
            except Exception as e:
                print(f"Erro ao executar consulta: {e}")
                input("Pressione ENTER para continuar...")

def consultar_comentarios_recentes():
    """
    Consulta 7: Lista os 10 comentários mais recentes em reports ativos.
    CORRIGIDO: Trata usuários com nome NULL.
    """
    sql = """
    SELECT
        R.idReport,
        R.titulo AS TituloReport,
        U.nome AS NomeCidadao,
        C.texto AS Comentario,
        I.dataHora AS DataComentario
    FROM
        Interacao I
    INNER JOIN
        Comentario C ON I.idInteracao = C.idInteracao
    INNER JOIN
        Report R ON I.idReport = R.idReport
    INNER JOIN
        Usuario U ON I.cpfCidadao = U.cpf
    WHERE
        R.status IN ('Aberto', 'Em Análise')
    ORDER BY
        I.dataHora DESC
    LIMIT 10;
    """
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(sql)
                rows = cur.fetchall()
                
                clear_console()
                print("\n=== Relatório: Últimos Comentários (Reports Ativos) ===")
                print(f"{'ID':<4} | {'Report':<25} | {'Cidadão':<20} | {'Comentário':<30}")
                print("-" * 90)
                
                if not rows:
                    print("Nenhum comentário recente encontrado em reports ativos.")
                else:
                    for row in rows:
                        id_rep = row[0]
                        
                        # Tratamento seguro para strings (evita erro NoneType)
                        titulo_raw = row[1] or "Sem Título"
                        nome_raw = row[2] or "Anônimo" # <--- AQUI ESTAVA O ERRO
                        texto_raw = row[3] or ""
                        
                        titulo = (titulo_raw[:22] + '..') if len(titulo_raw) > 22 else titulo_raw
                        cidadao = (nome_raw[:17] + '..') if len(nome_raw) > 17 else nome_raw
                        texto = (texto_raw[:27] + '..') if len(texto_raw) > 27 else texto_raw
                        
                        print(f"{id_rep:<4} | {titulo:<25} | {cidadao:<20} | {texto:<30}")
                
                input("\nPressione ENTER para voltar...")
                
            except Exception as e:
                print(f"Erro ao executar consulta: {e}")
                input("Pressione ENTER para continuar...")
                
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
    while True:
        clear_console()
        print("\n=== Menu de Consultas (Selects) ===")
        print("1) Total de Interações por Report")
        print("2) Reports por Funcionário")
        print("3) Média de Avaliações (Alta Performance)")
        print("4) Funcionários Expert (Todas Categorias)")
        print("5) Reports Críticos (Alta Relevância)")
        print("6) Hotspots (Áreas com Problemas Recorrentes)")
        print("7) Últimos Comentários")                       
        print("0) Voltar")
        
        choice = input("Escolha uma consulta: ").strip()
        
        if choice == "1":
            consultar_total_interacoes()
        elif choice == "2":
            consultar_reports_por_funcionario() 
        elif choice == "3":
            consultar_media_avaliacoes()
        elif choice == "4":
            consultar_funcionarios_todos_categorias()
        elif choice == "5":
            consultar_reports_criticos()
        elif choice == "6":
            consultar_areas_problematicas()    
        elif choice == "7":
            consultar_comentarios_recentes()   
        elif choice == "0":
            break
        else:
            print("Opção inválida ou ainda não implementada.")
            input("Pressione ENTER...")

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
