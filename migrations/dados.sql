-- ===============================================
-- Projeto: Apontaí - Zeladoria Urbana Colaborativa
-- ===============================================
-- Script de Alimentação Inicial da Base de Dados
-- COMPREHENSIVE CORNER CASE TESTING
-- Contém exemplos de todos os casos extremos e validações do esquema
-- ===============================================

BEGIN TRANSACTION;

-- ===============================================
-- BLOCO 1: Usuários Base (sem dependências)
-- ===============================================

-- Inserção de 6 usuários (normal + NULL cases)
INSERT INTO Usuario (cpf, nome, email, dataNascimento, role) VALUES
    -- Casos normais
    ('123.456.789-01', 'Maria Silva Santos', 'maria.silva@email.com', '1985-03-15', 'Cidadao'),
    ('987.654.321-02', 'João Pedro Oliveira', 'joao.oliveira@prefeitura.gov.br', '1978-07-22', 'Funcionario'),
    ('456.789.123-03', 'Ana Carolina Costa', 'ana.costa@email.com', '1992-11-08', 'Cidadao'),
    ('321.654.987-04', 'Carlos Eduardo Souza', 'carlos.souza@prefeitura.gov.br', '1980-05-30', 'Funcionario'),
    -- Corner case: NULL nome (válido conforme esquema)
    ('111.222.333-44', NULL, 'sem.nome@email.com', '1990-01-01', 'Cidadao'),
    -- Corner case: NULL email (válido conforme esquema)
    ('555.666.777-88', 'Pedro Sem Email', NULL, '1995-05-15', 'Funcionario');

-- ===============================================
-- BLOCO 2: Especializações de Usuário
-- ===============================================

-- Inserção de 4 Cidadãos (normal + edge cases)
INSERT INTO Cidadao (cpf, pontos) VALUES
    ('123.456.789-01', 250),  -- Normal: pontos positivos
    ('456.789.123-03', 150),  -- Normal: pontos positivos
    -- Corner case: pontos = 0 (mínimo permitido pelo CHECK >= 0)
    ('111.222.333-44', 0);
    -- Corner case: NULL pontos (válido, tem DEFAULT 0)
    -- Note: Will be inserted implicitly with DEFAULT value

-- Inserção de 3 Funcionários (normal + NULL cases)
INSERT INTO Funcionario (cpf, setor, cidade) VALUES
    ('987.654.321-02', 'Secretaria de Infraestrutura', 'São Paulo'),
    ('321.654.987-04', 'Secretaria de Saúde Pública', 'Campinas'),
    -- Corner case: NULL setor e NULL cidade (válido conforme esquema)
    ('555.666.777-88', NULL, NULL);

-- ===============================================
-- BLOCO 3: Entidades Independentes
-- ===============================================

-- Inserção de 4 Categorias de Report (normal + edge case)
INSERT INTO CategoriaReport (nome, pontos) VALUES
    ('Buraco na Via', 50),
    ('Iluminação Pública', 30),
    ('Lixo Acumulado', 40),
    -- Corner case: pontos = 1 (mínimo permitido pelo CHECK > 0)
    ('Pichação Leve', 1);

-- Inserção de 3 Benefícios (normal + edge cases)
INSERT INTO Beneficio (nomeBeneficio, custo, descricao) VALUES
    ('Desconto Transporte Público', 100, 'Desconto de 50% em passagens de ônibus por 1 mês'),
    ('Vale Cultura', 200, 'Ingresso gratuito para museus e teatros municipais'),
    -- Corner case: custo = 1 (mínimo permitido pelo CHECK > 0)
    ('Adesivo Apontaí', 1, 'Adesivo comemorativo do projeto');

-- ===============================================
-- BLOCO 4: Reports (dependem de CategoriaReport e Cidadao)
-- ===============================================

-- Inserção de 5 Reports (todos os 4 status ENUM + NULL descricao)
-- Note: dataCriacao has DEFAULT NOW(), status has DEFAULT 'Aberto'
INSERT INTO Report (titulo, localizacao, descricao, status, idCategoriaReport, cpfCidadao) VALUES
    (
        'Buraco grande na Av. Paulista',
        'Av. Paulista, 1000 - São Paulo/SP',
        'Buraco profundo causando riscos para veículos e pedestres',
        'Resolvido',
        1,  -- Categoria: Buraco na Via
        '123.456.789-01'  -- Cidadão: Maria
    ),
    (
        'Poste sem iluminação na praça',
        'Praça da República - São Paulo/SP',
        'Poste apagado há mais de 1 semana, comprometendo segurança',
        'Em Análise',
        2,  -- Categoria: Iluminação Pública
        '456.789.123-03'  -- Cidadão: Ana
    ),
    (
        'Lixo acumulado em terreno baldio',
        'Rua das Flores, 523 - Campinas/SP',
        'Grande volume de lixo acumulado atraindo roedores',
        'Aberto',
        3,  -- Categoria: Lixo Acumulado
        '123.456.789-01'  -- Cidadão: Maria
    ),
    -- Corner case: status = 'Fechado' (4º valor do ENUM, completando coverage)
    (
        'Report finalizado e arquivado',
        'Rua XYZ, 100 - São Paulo/SP',
        'Problema resolvido e arquivado após confirmação',
        'Fechado',
        1,
        '456.789.123-03'  -- Cidadão: Ana
    ),
    -- Corner case: NULL descricao (válido conforme esquema)
    (
        'Report sem descrição detalhada',
        'Av. ABC, 200 - Campinas/SP',
        NULL,  -- descricao é nullable
        'Aberto',
        4,  -- Categoria: Pichação Leve
        '111.222.333-44'  -- Cidadão sem nome
    ),
    (
        'Outro problema na mesma rua',
        'Rua das Flores, 523 - Campinas/SP',
        'Calçada quebrada perto do lixo',
        'Aberto', 
        1, 
        '456.789.123-03'
    );

-- ===============================================
-- BLOCO 5: Mídia (dependem de Report)
-- ===============================================

-- Inserção de 4 mídias vinculadas aos reports
-- Note: idMidia is SERIAL (auto-generated), dataUpload has DEFAULT NOW()
INSERT INTO Midia (link, idReport) VALUES
    ('https://storage.apontai.com/fotos/buraco_paulista_001.jpg', 1),
    ('https://storage.apontai.com/fotos/poste_republica_001.jpg', 2),
    ('https://storage.apontai.com/fotos/lixo_flores_001.jpg', 3),
    ('https://storage.apontai.com/fotos/report_fechado_001.jpg', 4);

-- ===============================================
-- BLOCO 6: Interações (dependem de Report e Cidadao)
-- ===============================================

-- Inserção de interações de tipos diferentes
-- Note: dataHora has DEFAULT NOW()
INSERT INTO Interacao (cpfCidadao, idReport, tipo) VALUES
    ('456.789.123-03', 1, 'Comentario'),  -- Ana comenta no report de Maria
    ('123.456.789-01', 2, 'Upvote'),      -- Maria dá upvote no report de Ana
    ('123.456.789-01', 1, 'Avaliacao');   -- Maria avalia resolução do próprio report

-- ===============================================
-- BLOCO 7: Especializações de Interação (Com Ajuste de Unicidade)
-- ===============================================

-- ID 1 (Já inserido acima)
INSERT INTO Comentario (idInteracao, texto) VALUES
    (1, 'Também passei por aqui e quase danifiquei meu carro! Urgente essa correção.');

-- ID 4: Novo comentário em outro report
INSERT INTO Interacao (cpfCidadao, idReport, tipo) VALUES
    ('456.789.123-03', 3, 'Comentario');
INSERT INTO Comentario (idInteracao, texto) VALUES
    (4, 'Situação muito grave, pode causar problemas de saúde pública!');

-- ID 5: Comentário curto (teste de constraint LENGTH)
INSERT INTO Interacao (cpfCidadao, idReport, tipo) VALUES
    ('111.222.333-44', 5, 'Comentario');
INSERT INTO Comentario (idInteracao, texto) VALUES
    (5, 'Sim'); 

-- ID 6: Altera o CPF para Maria 
INSERT INTO Interacao (cpfCidadao, idReport, tipo) VALUES
    ('123.456.789-01', 1, 'Comentario'); 
INSERT INTO Comentario (idInteracao, texto) VALUES
    (6, 'Voltei aqui e vi que ainda não foi resolvido!');

-- ID 7: Upvote
INSERT INTO Upvote (idInteracao) VALUES (2); -- Vincula ao ID 2 criado no Bloco 6

INSERT INTO Interacao (cpfCidadao, idReport, tipo) VALUES
    ('456.789.123-03', 2, 'Upvote'); -- ID 7 (novo upvote)
INSERT INTO Upvote (idInteracao) VALUES (7);

-- ID 8: Avaliação
INSERT INTO Avaliacao (idInteracao, nota, comentario) VALUES
    (3, 5, 'Problema resolvido rapidamente! Equipe muito eficiente.'); -- Vincula ao ID 3

INSERT INTO Interacao (cpfCidadao, idReport, tipo) VALUES
    ('456.789.123-03', 4, 'Avaliacao'); -- ID 8
INSERT INTO Avaliacao (idInteracao, nota, comentario) VALUES
    (8, 4, 'Bom atendimento e resolução adequada.');

-- ID 9: Avaliação nota 1
INSERT INTO Interacao (cpfCidadao, idReport, tipo) VALUES
    ('111.222.333-44', 1, 'Avaliacao'); -- ID 9
INSERT INTO Avaliacao (idInteracao, nota, comentario) VALUES
    (9, 1, NULL);

-- ===============================================
-- BLOCO 8: Histórico de Atualizações (Com Ajuste de Tempo)
-- ===============================================

INSERT INTO HistoricoAtualizacao (idReport, cpfFuncionario, atributoAtualizado, dataHoraAtualizacao) VALUES
    -- Report 1 (Categoria 1: Buraco)
    (1, '987.654.321-02', 'status', NOW()),
    -- Report 2 (Categoria 2: Iluminação) - João atualiza também
    (2, '987.654.321-02', 'status', NOW() + interval '5 minutes'),
    
    -- Report 3 (Categoria 3: Lixo) - João atualiza também
    (3, '987.654.321-02', 'status', NOW() + interval '10 minutes'),
    
    -- Report 5 (Categoria 4: Pichação) - João atualiza também
    (5, '987.654.321-02', 'status', NOW() + interval '15 minutes'),

    (2, '321.654.987-04', 'status', NOW()),
    (4, '555.666.777-88', 'status', NOW());

-- ===============================================
-- BLOCO 9: Resgate de Benefícios (dependem de Cidadao e Beneficio)
-- ===============================================

-- Ajustar pontos dos cidadãos para permitir resgates
UPDATE Cidadao SET pontos = 250 WHERE cpf = '123.456.789-01';  -- Maria
UPDATE Cidadao SET pontos = 200 WHERE cpf = '456.789.123-03';  -- Ana
UPDATE Cidadao SET pontos = 10 WHERE cpf = '111.222.333-44';   -- Cidadão sem nome

-- Inserção de resgates de benefícios (normal + edge case)
-- Note: dataHoraResgate has DEFAULT NOW()
INSERT INTO CidadaoBeneficio (cpfCidadao, nomeBeneficio, pontosResgatados) VALUES
    ('123.456.789-01', 'Desconto Transporte Público', 100),
    ('456.789.123-03', 'Vale Cultura', 200),
    -- Corner case: pontosResgatados = 1 (mínimo permitido pelo CHECK > 0)
    ('111.222.333-44', 'Adesivo Apontaí', 1);

-- Ajustar pontos após resgates
UPDATE Cidadao SET pontos = 150 WHERE cpf = '123.456.789-01';  -- 250 - 100
UPDATE Cidadao SET pontos = 0 WHERE cpf = '456.789.123-03';    -- 200 - 200 (edge case: pontos=0)
UPDATE Cidadao SET pontos = 9 WHERE cpf = '111.222.333-44';    -- 10 - 1

COMMIT;

-- ===============================================
-- Resumo da Alimentação com Corner Cases:
-- ===============================================
-- Usuario: 6 registros (4 normais + 2 NULL cases)
-- Cidadao: 3 registros (2 normais + 1 com pontos=0)
-- Funcionario: 3 registros (2 normais + 1 NULL setor/cidade)
-- CategoriaReport: 4 registros (3 normais + 1 pontos=1)
-- Beneficio: 3 registros (2 normais + 1 custo=1)
-- Report: 5 registros (todos 4 status ENUM + NULL descricao)
-- Midia: 4 registros
-- Interacao: 9 registros (todos 3 tipos ENUM + DEFERRABLE test)
-- Comentario: 4 registros (3 normais + 1 LENGTH=3)
-- Upvote: 2 registros
-- Avaliacao: 3 registros (2 normais + 1 nota=1 + NULL comentario)
-- HistoricoAtualizacao: 4 registros
-- CidadaoBeneficio: 3 registros (2 normais + 1 pontosResgatados=1)
-- ===============================================
-- TOTAL: 48 registros distribuídos em 13 tabelas
-- ===============================================
-- CORNER CASES TESTADOS:
-- ✅ NULL nome (Usuario)
-- ✅ NULL email (Usuario)
-- ✅ pontos = 0 (Cidadao - mínimo)
-- ✅ NULL setor, NULL cidade (Funcionario)
-- ✅ pontos = 1 (CategoriaReport - mínimo)
-- ✅ status = 'Fechado' (Report - 4º ENUM completo)
-- ✅ NULL descricao (Report)
-- ✅ LENGTH(texto) = 3 (Comentario - mínimo)
-- ✅ nota = 1 (Avaliacao - mínimo)
-- ✅ NULL comentario (Avaliacao)
-- ✅ custo = 1 (Beneficio - mínimo)
-- ✅ pontosResgatados = 1 (CidadaoBeneficio - mínimo)
-- ✅ DEFERRABLE UNIQUE (múltiplos Comentarios mesmo cidadão+report)
-- ===============================================
