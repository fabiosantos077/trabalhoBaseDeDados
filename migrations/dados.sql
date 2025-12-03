-- ===============================================
-- Projeto: Apontaí - Zeladoria Urbana Colaborativa
-- ===============================================
-- Script de Alimentação Inicial da Base de Dados
-- Contém no mínimo 2 tuplas por tabela, respeitando dependências FK
-- ===============================================

BEGIN TRANSACTION;

-- ===============================================
-- BLOCO 1: Usuários Base (sem dependências)
-- ===============================================

-- Inserção de 4 usuários (2 cidadãos + 2 funcionários)
INSERT INTO Usuario (cpf, nome, email, dataNascimento, role) VALUES
    ('123.456.789-01', 'Maria Silva Santos', 'maria.silva@email.com', '1985-03-15', 'Cidadao'),
    ('987.654.321-02', 'João Pedro Oliveira', 'joao.oliveira@prefeitura.gov.br', '1978-07-22', 'Funcionario'),
    ('456.789.123-03', 'Ana Carolina Costa', 'ana.costa@email.com', '1992-11-08', 'Cidadao'),
    ('321.654.987-04', 'Carlos Eduardo Souza', 'carlos.souza@prefeitura.gov.br', '1980-05-30', 'Funcionario');

-- ===============================================
-- BLOCO 2: Especializações de Usuário
-- ===============================================

-- Inserção de 2 Cidadãos (dependem de Usuario)
INSERT INTO Cidadao (cpf, pontos) VALUES
    ('123.456.789-01', 250),  -- Maria com 250 pontos acumulados
    ('456.789.123-03', 150);  -- Ana com 150 pontos acumulados

-- Inserção de 2 Funcionários (dependem de Usuario)
INSERT INTO Funcionario (cpf, setor, cidade) VALUES
    ('987.654.321-02', 'Secretaria de Infraestrutura', 'São Paulo'),
    ('321.654.987-04', 'Secretaria de Saúde Pública', 'Campinas');

-- ===============================================
-- BLOCO 3: Entidades Independentes
-- ===============================================

-- Inserção de 3 Categorias de Report (independente)
INSERT INTO CategoriaReport (nome, pontos) VALUES
    ('Buraco na Via', 50),
    ('Iluminação Pública', 30),
    ('Lixo Acumulado', 40);

-- Inserção de 2 Benefícios (independente)
INSERT INTO Beneficio (nomeBeneficio, custo, descricao) VALUES
    ('Desconto Transporte Público', 100, 'Desconto de 50% em passagens de ônibus por 1 mês'),
    ('Vale Cultura', 200, 'Ingresso gratuito para museus e teatros municipais');

-- ===============================================
-- BLOCO 4: Reports (dependem de CategoriaReport e Cidadao)
-- ===============================================

-- Inserção de 3 Reports com diferentes status
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
    );

-- ===============================================
-- BLOCO 5: Mídia (dependem de Report)
-- ===============================================

-- Inserção de 3 mídias vinculadas aos reports
-- Note: idMidia is SERIAL (auto-generated), dataUpload has DEFAULT NOW()
INSERT INTO Midia (link, idReport) VALUES
    ('https://storage.apontai.com/fotos/buraco_paulista_001.jpg', 1),
    ('https://storage.apontai.com/fotos/poste_republica_001.jpg', 2),
    ('https://storage.apontai.com/fotos/lixo_flores_001.jpg', 3);

-- ===============================================
-- BLOCO 6: Interações (dependem de Report e Cidadao)
-- ===============================================

-- Inserção de 3 interações de tipos diferentes
-- Note: dataHora has DEFAULT NOW()
INSERT INTO Interacao (cpfCidadao, idReport, tipo) VALUES
    ('456.789.123-03', 1, 'Comentario'),  -- Ana comenta no report de Maria
    ('123.456.789-01', 2, 'Upvote'),      -- Maria dá upvote no report de Ana
    ('123.456.789-01', 1, 'Avaliacao');   -- Maria avalia resolução do próprio report

-- ===============================================
-- BLOCO 7: Especializações de Interação
-- ===============================================

-- Inserção de 2 Comentários (dependem de Interacao tipo='Comentario')
INSERT INTO Comentario (idInteracao, texto) VALUES
    (1, 'Também passei por aqui e quase danifiquei meu carro! Urgente essa correção.');

-- Para ter pelo menos 2 tuplas, precisamos adicionar outro comentário
-- Vamos adicionar mais uma interação do tipo Comentario
INSERT INTO Interacao (cpfCidadao, idReport, tipo) VALUES
    ('456.789.123-03', 3, 'Comentario');

INSERT INTO Comentario (idInteracao, texto) VALUES
    (4, 'Situação muito grave, pode causar problemas de saúde pública!');

-- Inserção de 2 Upvotes (dependem de Interacao tipo='Upvote')
INSERT INTO Upvote (idInteracao) VALUES
    (2);

-- Adicionar mais um upvote para ter 2 tuplas
INSERT INTO Interacao (cpfCidadao, idReport, tipo) VALUES
    ('456.789.123-03', 1, 'Upvote');

INSERT INTO Upvote (idInteracao) VALUES
    (5);

-- Inserção de 2 Avaliações (dependem de Interacao tipo='Avaliacao')
INSERT INTO Avaliacao (idInteracao, nota, comentario) VALUES
    (3, 5, 'Problema resolvido rapidamente! Equipe muito eficiente.');

-- Adicionar mais uma avaliação
INSERT INTO Interacao (cpfCidadao, idReport, tipo) VALUES
    ('456.789.123-03', 2, 'Avaliacao');

INSERT INTO Avaliacao (idInteracao, nota, comentario) VALUES
    (6, 4, 'Estão analisando, aguardando retorno sobre prazo de resolução.');

-- ===============================================
-- BLOCO 8: Histórico de Atualizações (dependem de Report e Funcionario)
-- ===============================================

-- Inserção de 3 registros de atualização
-- Note: dataHoraAtualizacao has DEFAULT NOW()
INSERT INTO HistoricoAtualizacao (idReport, cpfFuncionario, atributoAtualizado) VALUES
    (1, '987.654.321-02', 'status'),      -- João muda status para "Em Análise"
    (1, '987.654.321-02', 'status'),      -- João muda status para "Resolvido"
    (2, '321.654.987-04', 'status');      -- Carlos muda status para "Em Análise"

-- ===============================================
-- BLOCO 9: Resgate de Benefícios (dependem de Cidadao e Beneficio)
-- ===============================================

-- Inserção de 2 resgates de benefícios
-- Note: dataHoraResgate has DEFAULT NOW()
-- Maria resgata "Desconto Transporte Público" (custo: 100 pontos)
INSERT INTO CidadaoBeneficio (cpfCidadao, nomeBeneficio, pontosResgatados) VALUES
    ('123.456.789-01', 'Desconto Transporte Público', 100);

-- Ana resgata "Vale Cultura" (custo: 200 pontos)
-- Nota: Ana teria que ter pelo menos 200 pontos, vamos ajustar seus pontos
UPDATE Cidadao SET pontos = 200 WHERE cpf = '456.789.123-03';

INSERT INTO CidadaoBeneficio (cpfCidadao, nomeBeneficio, pontosResgatados) VALUES
    ('456.789.123-03', 'Vale Cultura', 200);

-- Ajustar pontos dos cidadãos após resgates
-- Maria tinha 250, resgatou 100, ficou com 150
UPDATE Cidadao SET pontos = 150 WHERE cpf = '123.456.789-01';

-- Ana tinha 200, resgatou 200, ficou com 0
UPDATE Cidadao SET pontos = 0 WHERE cpf = '456.789.123-03';

COMMIT;

-- ===============================================
-- Resumo da Alimentação Inicial:
-- ===============================================
-- Usuario: 4 registros (2 cidadãos + 2 funcionários)
-- Cidadao: 2 registros
-- Funcionario: 2 registros
-- CategoriaReport: 3 registros
-- Beneficio: 2 registros
-- Report: 3 registros (1 Resolvido, 1 Em Análise, 1 Aberto)
-- Midia: 3 registros (1 foto por report)
-- Interacao: 6 registros (2 comentários + 2 upvotes + 2 avaliações)
-- Comentario: 2 registros
-- Upvote: 2 registros
-- Avaliacao: 2 registros
-- HistoricoAtualizacao: 3 registros
-- CidadaoBeneficio: 2 registros
-- ===============================================
-- TOTAL: 32 registros distribuídos em 13 tabelas
-- ===============================================
