-- ===============================================
-- Projeto: Apontaí - Zeladoria Urbana Colaborativa
-- ===============================================

-- ===============================================
-- QUERY 1: TOTAL DE INTERAÇÕES POR REPORT
-- ===============================================
-- Descrição: Apresenta o total de interações (Comentário, Upvote, Avaliação) por Report,
--            incluindo Reports que não tiveram nenhuma interação (Junção Externa).
--
-- Conceitos demonstrados:
--   - INNER JOIN: Relaciona Report com sua Categoria (sempre existe)
--   - LEFT OUTER JOIN: Inclui Reports mesmo sem interações (COUNT retorna 0)
--   - GROUP BY: Agrupa por Report para contar interações
--   - Agregação: COUNT() conta interações por Report
--
SELECT
    R.idReport,              -- Identificador único do Report
    R.titulo,                -- Título do problema reportado
    R.status,                -- Status atual (Aberto, Em Análise, Resolvido, etc.)
    CR.nome AS Categoria,    -- Nome da categoria do problema
    COUNT(I.idInteracao) AS TotalInteracoes  -- Conta interações (0 se nenhuma)
FROM
    Report R
INNER JOIN
    CategoriaReport CR ON R.idCategoriaReport = CR.idCategoriaReport  -- Busca categoria do Report
LEFT JOIN -- LEFT JOIN garante que Reports sem interação apareçam com COUNT = 0
    Interacao I ON R.idReport = I.idReport  -- Relaciona interações ao Report
GROUP BY
    R.idReport, R.titulo, R.status, CR.nome  -- Agrupa por Report (uma linha por Report)
ORDER BY
    TotalInteracoes DESC, R.idReport;  -- Ordena: mais interações primeiro

-- ===============================================
-- QUERY 2: REPORTS ATUALIZADOS POR FUNCIONÁRIO
-- ===============================================
-- Descrição: Apresenta o total de Reports atualizados por Funcionário,
--            incluindo funcionários que ainda não atualizaram nenhum Report (Junção Externa).
--
-- Conceitos demonstrados:
--   - LEFT OUTER JOIN: Inclui funcionários mesmo sem atualizações
--   - INNER JOIN: Relaciona Funcionario com Usuario (relacionamento obrigatório)
--   - COUNT DISTINCT: Conta Reports únicos (evita duplicação se múltiplas atualizações)
--   - GROUP BY: Agrupa por Funcionário
--
SELECT
    U.nome AS NomeFuncionario,           -- Nome do funcionário
    F.setor,                             -- Setor onde o funcionário trabalha
    COUNT(DISTINCT HA.idReport) AS ReportsAtualizados  -- Conta Reports distintos atualizados
FROM
    Funcionario F
INNER JOIN
    Usuario U ON F.cpf = U.cpf  -- Busca dados do usuário (nome) para o funcionário
LEFT JOIN -- LEFT JOIN garante que funcionários sem atualizações apareçam com COUNT = 0
    HistoricoAtualizacao HA ON F.cpf = HA.cpfFuncionario  -- Relaciona atualizações do funcionário
GROUP BY
    U.nome, F.setor  -- Agrupa por funcionário (uma linha por funcionário)
ORDER BY
    ReportsAtualizados DESC, U.nome;  -- Ordena: mais produtivos primeiro

-- ===============================================
-- QUERY 3: NOTA MÉDIA DE AVALIAÇÕES POR CATEGORIA
-- ===============================================
-- Descrição: Calcula a nota média de Avaliações para cada CategoriaReport,
--            apenas para Reports Resolvidos (status = 'Resolvido').
--
-- Conceitos demonstrados:
--   - Múltiplos INNER JOINs: Navega relacionamentos obrigatórios
--   - WHERE: Filtra antes da agregação (apenas Reports Resolvidos)
--   - GROUP BY + Agregação: Calcula média por Categoria
--   - HAVING: Filtra depois da agregação (apenas categorias com nota > 4.0)
--   - Função de agregação: AVG() para cálculo de média
--
SELECT
    CR.nome AS Categoria,              -- Nome da categoria
    ROUND(AVG(A.nota), 2) AS NotaMedia -- Média arredondada das notas de avaliação
FROM
    CategoriaReport CR
INNER JOIN
    Report R ON CR.idCategoriaReport = R.idCategoriaReport  -- Relaciona categoria aos seus reports
INNER JOIN
    Interacao I ON R.idReport = I.idReport  -- Relaciona reports às interações
INNER JOIN
    Avaliacao A ON I.idInteracao = A.idInteracao  -- Relaciona interações às avaliações
WHERE
    R.status = 'Resolvido' -- FILTRO PRÉ-AGREGAÇÃO: Considera apenas Reports finalizados
GROUP BY
    CR.nome  -- Agrupa por categoria (uma linha por categoria)
HAVING
    AVG(A.nota) > 4.0 -- FILTRO PÓS-AGREGAÇÃO: Mostra apenas categorias bem avaliadas
ORDER BY
    NotaMedia DESC;  -- Ordena: melhores avaliações primeiro

-- ===============================================
-- QUERY 4: FUNCIONÁRIOS QUE ATUALIZARAM TODAS AS CATEGORIAS
-- ===============================================
-- Descrição: Encontra os Funcionários que já atualizaram Reports de TODAS as
--            'CategoriaReport' cadastradas no sistema.
--
-- Conceitos demonstrados:
--   - NOT EXISTS: Verifica ausência de elementos
--   - EXCEPT (operação de conjunto): Subtração de conjuntos
--   - Subconsulta correlacionada: Subconsulta referencia tabela externa (F.cpf)
--   - Álgebra Relacional: Divisão (A ÷ B) = "todos os elementos de B estão em A"
--
-- Lógica: Encontra funcionários onde NÃO EXISTE uma categoria
--         que NÃO esteja no conjunto de categorias que ele já atualizou
--
-- Equivalente a: Categorias_Totais - Categorias_Atualizadas_Funcionário = Vazio
--
SELECT
    U.cpf,   -- CPF do funcionário
    U.nome   -- Nome do funcionário
FROM
    Funcionario F
INNER JOIN
    Usuario U ON F.cpf = U.cpf  -- Busca dados do usuário
WHERE
    NOT EXISTS (  -- NÃO EXISTE uma categoria...
        SELECT CR.idCategoriaReport  -- Pega TODAS as categorias do sistema
        FROM CategoriaReport CR
        EXCEPT  -- SUBTRAI (operação de conjunto)
        SELECT R.idCategoriaReport   -- As categorias que o funcionário JÁ atualizou
        FROM HistoricoAtualizacao HA
        INNER JOIN Report R ON HA.idReport = R.idReport
        WHERE HA.cpfFuncionario = F.cpf  -- CORRELACIONADO: para este funcionário específico
    )
    -- Se o resultado do EXCEPT for vazio, significa que o funcionário atualizou TODAS
ORDER BY
    U.nome;

-- ===============================================
-- QUERY 5: REPORTS CRÍTICOS SEM ATUALIZAÇÃO
-- ===============================================
-- Descrição: Identifica Reports "Críticos" (com 2+ interações) que estão sem
--            atualização de um funcionário há mais de 2 dias.
--
-- Conceitos demonstrados:
--   - Subconsulta escalar: Retorna um único valor (última atualização)
--   - Subconsulta no SELECT: Calcula valor adicional por registro
--   - Subconsulta no HAVING: Filtra com base em subconsulta
--   - Agregação com filtro complexo: Combina COUNT com cálculo de intervalo
--   - Funções de data: NOW(), operações com INTERVAL
--
SELECT
    R.idReport,                -- ID do Report
    R.titulo,                  -- Título do problema
    R.dataCriacao,             -- Data de criação do Report
    COUNT(I.idInteracao) AS TotalInteracoes,  -- Conta interações (indica urgência)
    -- SUBCONSULTA ESCALAR: Retorna última atualização do funcionário neste Report
    (SELECT MAX(dataHoraAtualizacao)
     FROM HistoricoAtualizacao
     WHERE idReport = R.idReport) AS UltimaAtualizacaoFuncionario
FROM
    Report R
INNER JOIN
    Interacao I ON R.idReport = I.idReport  -- Relaciona interações
WHERE
    R.status IN ('Aberto', 'Em Análise') -- Filtra apenas Reports pendentes
GROUP BY
    R.idReport, R.titulo, R.dataCriacao  -- Agrupa por Report
HAVING
    COUNT(I.idInteracao) >= 2  -- FILTRO 1: Alta prioridade (muito engajamento)
    AND (NOW() - (SELECT MAX(dataHoraAtualizacao)   -- FILTRO 2: Calcula tempo sem atualização
                  FROM HistoricoAtualizacao
                  WHERE idReport = R.idReport)) > INTERVAL '2 days'  -- Mais de 2 dias abandonado
ORDER BY
    TotalInteracoes DESC, UltimaAtualizacaoFuncionario ASC;  -- Ordena: mais críticos primeiro

-- ===============================================
-- QUERY 6: HOTSPOTS - ÁREAS COM MAIS PROBLEMAS
-- ===============================================
-- Descrição: Identifica áreas com maior concentração de problemas ativos (Hotspots).
--            Agrupa por localização e mostra apenas locais com mais de 1 report ativo.
--
-- Conceitos demonstrados:
--   - Agregação múltipla: COUNT e AVG na mesma query
--   - EXTRACT: Extrai parte de timestamp (segundos desde epoch)
--   - Operações aritméticas em datas: Cálculo de duração
--   - HAVING com filtro simples: Exclui locais com poucos reports
--   - LIMIT: Restringe resultado aos Top 5 hotspots
--
SELECT
    R.localizacao,                     -- Endereço/localização do problema
    COUNT(R.idReport) AS TotalReportsAtivos,  -- Quantidade de problemas ativos
    -- Calcula média de horas que os reports estão abertos nesta localização
    ROUND(AVG(EXTRACT(EPOCH FROM NOW() - R.dataCriacao) / 3600), 2) AS MediaHorasAberto
    -- EXTRACT(EPOCH FROM intervalo) = converte intervalo para segundos
    -- / 3600 = converte segundos para horas
    -- AVG() = calcula média entre todos os reports da localização
FROM
    Report R
WHERE
    R.status IN ('Aberto', 'Em Análise')  -- Considera apenas reports pendentes
GROUP BY
    R.localizacao  -- Agrupa por local (uma linha por localização)
HAVING
    COUNT(R.idReport) > 1  -- Mostra apenas locais com múltiplos problemas
ORDER BY
    TotalReportsAtivos DESC, MediaHorasAberto DESC  -- Ordena: mais problemáticos primeiro
LIMIT 5;  -- Top 5 áreas mais críticas

-- ===============================================
-- QUERY 7: COMENTÁRIOS RECENTES EM REPORTS ATIVOS
-- ===============================================
-- Descrição: Lista os 10 comentários mais recentes feitos em Reports que ainda estão ativos.
--            Inclui tratamento para usuários com nome nulo (COALESCE).
--
-- Conceitos demonstrados:
--   - COALESCE: Tratamento de valores NULL (substitui por valor padrão)
--   - Múltiplos INNER JOINs: Navegação por 4 tabelas relacionadas
--   - ORDER BY com DESC: Ordenação do mais recente para o mais antigo
--   - LIMIT: Restringe resultado aos 10 registros mais recentes
--
SELECT
    R.idReport,                              -- ID do Report comentado
    R.titulo AS TituloReport,                -- Título do Report
    COALESCE(U.nome, 'Anônimo') AS NomeCidadao,  -- Nome do cidadão (ou 'Anônimo' se NULL)
    C.texto AS Comentario,                   -- Texto do comentário
    I.dataHora AS DataComentario             -- Data e hora do comentário
FROM
    Interacao I
INNER JOIN
    Comentario C ON I.idInteracao = C.idInteracao  -- Relaciona interação ao comentário
INNER JOIN
    Report R ON I.idReport = R.idReport  -- Relaciona interação ao Report
INNER JOIN
    Usuario U ON I.cpfCidadao = U.cpf  -- Busca dados do cidadão que comentou
WHERE
    R.status IN ('Aberto', 'Em Análise')  -- Filtra apenas Reports ativos
ORDER BY
    I.dataHora DESC  -- Ordena do mais recente para o mais antigo
LIMIT 10;  -- Retorna apenas os 10 mais recentes