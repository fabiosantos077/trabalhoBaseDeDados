-- ===============================================
-- Projeto: Apontaí - Zeladoria Urbana Colaborativa
-- ===============================================

-- ===============================================
-- CUSTOM TYPES
-- ===============================================

CREATE TYPE role_type AS ENUM ('Cidadao', 'Funcionario');
CREATE TYPE status_type AS ENUM ('Aberto', 'Em Análise', 'Resolvido', 'Fechado');
CREATE TYPE interacao_type AS ENUM ('Comentario', 'Upvote', 'Avaliacao');

-- ===============================================
-- TABLES
-- ===============================================

-- 1. USUARIO - Base user entity
COMMENT ON TABLE Usuario IS 'Entidade base para usuários do sistema (cidadãos e funcionários)';

CREATE TABLE Usuario (
    cpf VARCHAR(14) PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    dataNascimento DATE NOT NULL,
    role role_type NOT NULL,

    -- Validation constraints
    CHECK (cpf ~ '^\d{3}\.\d{3}\.\d{3}-\d{2}$'),  -- Formato CPF: 000.000.000-00
    CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),  -- Email válido
    CHECK (dataNascimento <= CURRENT_DATE)  -- Data de nascimento não pode ser futura
);

-- 2. CIDADAO - Citizen specialization
COMMENT ON TABLE Cidadao IS 'Especialização de usuário para cidadãos que reportam problemas';

CREATE TABLE Cidadao (
    cpf VARCHAR(14) PRIMARY KEY,
    pontos INTEGER DEFAULT 0,

    CHECK (pontos >= 0),

    FOREIGN KEY (cpf) REFERENCES Usuario (cpf)
        ON DELETE CASCADE
);

-- 3. FUNCIONARIO - Employee specialization
COMMENT ON TABLE Funcionario IS 'Especialização de usuário para funcionários públicos que gerenciam reports';

CREATE TABLE Funcionario (
    cpf VARCHAR(14) PRIMARY KEY,
    setor VARCHAR(100),
    cidade VARCHAR(100),

    FOREIGN KEY (cpf) REFERENCES Usuario (cpf)
        ON DELETE CASCADE
);

-- 4. CATEGORIAREPORT - Report categories with point values
COMMENT ON TABLE CategoriaReport IS 'Categorias de reports com pontuação base';

CREATE TABLE CategoriaReport (
    idCategoriaReport SERIAL PRIMARY KEY,
    nome VARCHAR(100) UNIQUE NOT NULL,
    pontos INTEGER NOT NULL,

    CHECK (pontos > 0)
);

-- 5. REPORT - Main entity for civic reports
COMMENT ON TABLE Report IS 'Reports de problemas urbanos criados por cidadãos';

CREATE TABLE Report (
    idReport SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    localizacao VARCHAR(255) NOT NULL,
    descricao TEXT,
    dataCriacao TIMESTAMPTZ DEFAULT NOW(),
    status status_type DEFAULT 'Aberto',
    idCategoriaReport INTEGER NOT NULL,
    cpfCidadao VARCHAR(14) NOT NULL,

    FOREIGN KEY (idCategoriaReport) REFERENCES CategoriaReport (idCategoriaReport),
    FOREIGN KEY (cpfCidadao) REFERENCES Cidadao (cpf)
);

-- 6. MIDIA - Media attachments for reports
COMMENT ON TABLE Midia IS 'Anexos de mídia (fotos/vídeos) associados aos reports';

CREATE TABLE Midia (
    idMidia SERIAL PRIMARY KEY,  -- Surrogate key (melhor que usar link como PK)
    link VARCHAR(255) UNIQUE NOT NULL,
    idReport INTEGER NOT NULL,
    dataUpload TIMESTAMPTZ DEFAULT NOW(),

    FOREIGN KEY (idReport) REFERENCES Report (idReport)
        ON DELETE CASCADE
);

-- 7. INTERACAO - Base interaction entity
COMMENT ON TABLE Interacao IS 'Entidade base para interações dos cidadãos com reports';

CREATE TABLE Interacao (
    idInteracao SERIAL PRIMARY KEY,
    cpfCidadao VARCHAR(14) NOT NULL,
    idReport INTEGER NOT NULL,
    dataHora TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    tipo interacao_type NOT NULL,

    FOREIGN KEY (cpfCidadao) REFERENCES Cidadao (cpf),
    FOREIGN KEY (idReport) REFERENCES Report (idReport)
        ON DELETE CASCADE,

    -- Prevent duplicate upvotes from same citizen on same report
    UNIQUE (cpfCidadao, idReport, tipo)
        DEFERRABLE INITIALLY DEFERRED  -- Allows multiple Comentarios
);

-- 8. COMENTARIO - Comment specialization
COMMENT ON TABLE Comentario IS 'Comentários textuais em reports';

CREATE TABLE Comentario (
    idInteracao INTEGER PRIMARY KEY,
    texto TEXT NOT NULL,

    CHECK (LENGTH(texto) >= 3),  -- Minimum comment length

    FOREIGN KEY (idInteracao) REFERENCES Interacao (idInteracao)
        ON DELETE CASCADE
);

-- 9. UPVOTE - Upvote specialization
COMMENT ON TABLE Upvote IS 'Votos de apoio em reports (sem atributos adicionais)';

CREATE TABLE Upvote (
    idInteracao INTEGER PRIMARY KEY,

    FOREIGN KEY (idInteracao) REFERENCES Interacao (idInteracao)
        ON DELETE CASCADE
);

-- 10. AVALIACAO - Rating specialization
COMMENT ON TABLE Avaliacao IS 'Avaliações (notas de 1 a 5) da resolução de reports';

CREATE TABLE Avaliacao (
    idInteracao INTEGER PRIMARY KEY,
    nota INTEGER NOT NULL,
    comentario TEXT,

    CHECK (nota >= 1 AND nota <= 5),

    FOREIGN KEY (idInteracao) REFERENCES Interacao (idInteracao)
        ON DELETE CASCADE
);

-- 11. BENEFICIO - Rewards catalog
COMMENT ON TABLE Beneficio IS 'Catálogo de benefícios resgatáveis com pontos';

CREATE TABLE Beneficio (
    nomeBeneficio VARCHAR(100) PRIMARY KEY,
    custo INTEGER NOT NULL,
    descricao TEXT,

    CHECK (custo > 0)
);

-- 12. CIDADAOBENEFICIO - Benefit redemption history
COMMENT ON TABLE CidadaoBeneficio IS 'Histórico de resgates de benefícios pelos cidadãos';

CREATE TABLE CidadaoBeneficio (
    cpfCidadao VARCHAR(14) NOT NULL,
    nomeBeneficio VARCHAR(100) NOT NULL,
    dataHoraResgate TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    pontosResgatados INTEGER NOT NULL,

    PRIMARY KEY (cpfCidadao, nomeBeneficio, dataHoraResgate),

    CHECK (pontosResgatados > 0),

    FOREIGN KEY (cpfCidadao) REFERENCES Cidadao (cpf),
    FOREIGN KEY (nomeBeneficio) REFERENCES Beneficio (nomeBeneficio)
);

-- 13. HISTORICOATUALIZACAO - Report update audit trail
COMMENT ON TABLE HistoricoAtualizacao IS 'Auditoria de atualizações em reports por funcionários';

CREATE TABLE HistoricoAtualizacao (
    idReport INTEGER NOT NULL,
    cpfFuncionario VARCHAR(14) NOT NULL,
    dataHoraAtualizacao TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    atributoAtualizado VARCHAR(100) NOT NULL,

    PRIMARY KEY (idReport, cpfFuncionario, dataHoraAtualizacao),

    FOREIGN KEY (idReport) REFERENCES Report (idReport),
    FOREIGN KEY (cpfFuncionario) REFERENCES Funcionario (cpf)
);