-- ===============================================
-- Projeto: Apontaí - Zeladoria Urbana Colaborativa
-- ===============================================

-- 1. Tabela USUARIO (Entidade Genérica)
-- CPF é a chave primária e o identificador principal.
CREATE TABLE Usuario (
    cpf VARCHAR(14) PRIMARY KEY, -- Formato '000.000.000-00'
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL, -- Email deve ser único
    dataNascimento DATE NOT NULL,
    role VARCHAR(50) NOT NULL, -- Ex: 'Cidadao' ou 'Funcionario'
    CHECK (role IN ('Cidadao', 'Funcionario')) -- Restrição de domínio para a role
);

-- 2. Tabela CIDADAO (Especialização de Usuário)
-- Herda o CPF do Usuário. Pontos é um atributo próprio.
CREATE TABLE Cidadao (
    cpf VARCHAR(14) PRIMARY KEY,
    pontos INTEGER DEFAULT 0 NOT NULL,
    CHECK (pontos >= 0),
    FOREIGN KEY (cpf) REFERENCES Usuario (cpf)
        ON DELETE CASCADE -- Se o usuário for deletado, o cidadão também é.
);

-- 3. Tabela FUNCIONARIO (Especialização de Usuário)
-- Herda o CPF do Usuário. Setor e Cidade são atributos próprios.
CREATE TABLE Funcionario (
    cpf VARCHAR(14) PRIMARY KEY,
    setor VARCHAR(100) NOT NULL, -- Ex: Secretaria de Obras, Iluminação Pública
    cidade VARCHAR(100) NOT NULL,
    FOREIGN KEY (cpf) REFERENCES Usuario (cpf)
        ON DELETE CASCADE -- Se o usuário for deletado, o funcionário também é.
);

-- 4. Tabela CATEGORIAREPORT (Com ID artificial para eficiência)
CREATE TABLE CategoriaReport (
    idCategoriaReport SERIAL PRIMARY KEY, -- Chave artificial auto-incrementável
    nome VARCHAR(100) UNIQUE NOT NULL,
    pontos INTEGER NOT NULL, -- Pontuação base para reports desta categoria
    CHECK (pontos > 0)
);

-- 5. Tabela REPORT (Entidade Central)
-- idReport como chave artificial para referências mais curtas.
CREATE TABLE Report (
    idReport SERIAL PRIMARY KEY, -- Chave artificial auto-incrementável
    titulo VARCHAR(200) NOT NULL,
    localizacao VARCHAR(255) NOT NULL, -- Localização geográfica (pode ser endereço ou coordenadas)
    descricao TEXT,
    dataCriacao TIMESTAMP NOT NULL,
    status VARCHAR(50) NOT NULL, -- Ex: Aberto, Em Análise, Resolvido, Fechado
    idCategoriaReport INTEGER NOT NULL,
    cpfCidadao VARCHAR(14) NOT NULL, -- FK para o Cidadão que criou o Report

    FOREIGN KEY (idCategoriaReport) REFERENCES CategoriaReport (idCategoriaReport),
    FOREIGN KEY (cpfCidadao) REFERENCES Cidadao (cpf)
);

-- 6. Tabela MIDIA (Entidade Fraca de Report)
-- Armazena links para fotos/vídeos. Link é a PK, mas depende de idReport.
CREATE TABLE Midia (
    link VARCHAR(255) PRIMARY KEY, -- O link é o identificador único da mídia
    idReport INTEGER NOT NULL,
    dataUpload TIMESTAMP NOT NULL,

    FOREIGN KEY (idReport) REFERENCES Report (idReport)
        ON DELETE CASCADE -- Se o Report for deletado, a mídia também é.
);

-- 7. Tabela INTERACAO (Entidade Genérica para Comentário, Upvote, Avaliação)
-- idInteracao é a chave artificial para otimizar as referências.
CREATE TABLE Interacao (
    idInteracao SERIAL PRIMARY KEY,
    cpfCidadao VARCHAR(14) NOT NULL, -- FK para o Cidadão que realizou a Interação
    idReport INTEGER NOT NULL, -- FK para o Report alvo da Interação
    dataHora TIMESTAMP NOT NULL,
    tipo VARCHAR(20) NOT NULL, -- Ex: 'Comentario', 'Upvote', 'Avaliacao'
    
    CHECK (tipo IN ('Comentario', 'Upvote', 'Avaliacao')),

    FOREIGN KEY (cpfCidadao) REFERENCES Cidadao (cpf),
    FOREIGN KEY (idReport) REFERENCES Report (idReport)
        ON DELETE CASCADE -- Se o Report for deletado, as interações associadas são.
);

-- 8. Tabela COMENTARIO (Especialização de Interação)
CREATE TABLE Comentario (
    idInteracao INTEGER PRIMARY KEY, -- É a mesma PK da tabela Interacao (mapeamento de especialização)
    texto TEXT NOT NULL,
    
    FOREIGN KEY (idInteracao) REFERENCES Interacao (idInteracao)
        ON DELETE CASCADE
);

-- 9. Tabela UPVOTE (Especialização de Interação)
-- Não possui atributos próprios, é mapeado apenas pela sua PK herdada.
CREATE TABLE Upvote (
    idInteracao INTEGER PRIMARY KEY,
    
    FOREIGN KEY (idInteracao) REFERENCES Interacao (idInteracao)
        ON DELETE CASCADE
);

-- 10. Tabela AVALIACAO (Especialização de Interação)
CREATE TABLE Avaliacao (
    idInteracao INTEGER PRIMARY KEY, -- É a mesma PK da tabela Interacao (mapeamento de especialização)
    nota INTEGER NOT NULL, -- Ex: 1 a 5
    comentario TEXT,
    CHECK (nota >= 1 AND nota <= 5),

    FOREIGN KEY (idInteracao) REFERENCES Interacao (idInteracao)
        ON DELETE CASCADE
);

-- 11. Tabela BENEFICIO (Catálogo de Recompensas)
CREATE TABLE Beneficio (
    nomeBeneficio VARCHAR(100) PRIMARY KEY, -- Nome é a chave primária
    custo INTEGER NOT NULL,
    descricao TEXT,
    CHECK (custo > 0)
);

-- 12. Tabela CIDADAOBENEFICIO (Relacionamento N:M entre Cidadão e Benefício)
-- Guarda o histórico de resgate de benefícios.
CREATE TABLE CidadaoBeneficio (
    cpfCidadao VARCHAR(14) NOT NULL,
    nomeBeneficio VARCHAR(100) NOT NULL,
    dataHoraResgate TIMESTAMP NOT NULL,
    pontosResgatados INTEGER NOT NULL, -- Pontos resgatados no momento do resgate

    PRIMARY KEY (cpfCidadao, nomeBeneficio, dataHoraResgate),

    FOREIGN KEY (cpfCidadao) REFERENCES Cidadao (cpf),
    FOREIGN KEY (nomeBeneficio) REFERENCES Beneficio (nomeBeneficio)
);

-- 13. Tabela HISTORICOATUALIZACAO (Relacionamento N:M entre Report e Funcionário)
-- Também armazena qual atributo foi atualizado.
CREATE TABLE HistoricoAtualizacao (
    idReport INTEGER NOT NULL,
    cpfFuncionario VARCHAR(14) NOT NULL,
    dataHoraAtualizacao TIMESTAMP NOT NULL,
    atributoAtualizado VARCHAR(100), -- Ex: 'status', 'localizacao', etc.

    PRIMARY KEY (idReport, cpfFuncionario, dataHoraAtualizacao),

    FOREIGN KEY (idReport) REFERENCES Report (idReport),
    FOREIGN KEY (cpfFuncionario) REFERENCES Funcionario (cpf)
);

-- ===============================================
-- Fim do Script de Criação de Tabelas
-- ===============================================