-- ===============================================
-- Projeto: Apontaí - Zeladoria Urbana Colaborativa
-- ===============================================

-- 1
-- Descrição: Apresenta o total de interações (Comentário, Upvote, Avaliação) por Report,
--            incluindo Reports que não tiveram nenhuma interação (Junção Externa).
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
LEFT JOIN -- LEFT JOIN para incluir Reports sem interações
    Interacao I ON R.idReport = I.idReport
GROUP BY
    R.idReport, R.titulo, R.status, CR.nome
ORDER BY
    TotalInteracoes DESC, R.idReport;

-- 2
-- Descrição: Apresenta o total de Reports atualizados por Funcionário,
--            incluindo funcionários que ainda não atualizaram nenhum Report (Junção Externa).
SELECT
    U.nome AS NomeFuncionario,
    F.setor,
    COUNT(DISTINCT HA.idReport) AS ReportsAtualizados
FROM
    Funcionario F
INNER JOIN
    Usuario U ON F.cpf = U.cpf
LEFT JOIN -- LEFT JOIN para incluir funcionários que ainda não atualizaram nenhum report
    HistoricoAtualizacao HA ON F.cpf = HA.cpfFuncionario
GROUP BY
    U.nome, F.setor
ORDER BY
    ReportsAtualizados DESC, U.nome;

-- 3
-- Descrição: Calcula a nota média de Avaliações para cada CategoriaReport,
--            apenas para Reports Resolvidos (status = 'Resolvido').
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
    R.status = 'Resolvido' -- Filtra apenas Reports Resolvidos para cálculo de performance
GROUP BY
    CR.nome
HAVING
    AVG(A.nota) > 4.0 -- Agrupamento com filtro
ORDER BY
    NotaMedia DESC;

-- 4
-- Descrição: Encontra os Funcionários que já atualizaram Reports de TODAS as
--            'CategoriaReport' cadastradas no sistema.
SELECT
    U.cpf,
    U.nome
FROM
    Funcionario F
INNER JOIN
    Usuario U ON F.cpf = U.cpf
WHERE
    NOT EXISTS ( -- NÃO EXISTE
        SELECT CR.idCategoriaReport -- UMA categoria (B)
        FROM CategoriaReport CR
        EXCEPT -- QUE NÃO ESTEJA
        SELECT R.idCategoriaReport
        FROM HistoricoAtualizacao HA
        INNER JOIN Report R ON HA.idReport = R.idReport
        WHERE HA.cpfFuncionario = F.cpf -- No conjunto de Categorias que o Funcionário (A) já atualizou
    )
ORDER BY
    U.nome;

-- 5
-- Descrição: Identifica Reports "Críticos" (com 2+ interações) que estão sem
--            atualização de um funcionário há mais de 2 dias.
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
    R.status IN ('Aberto', 'Em Análise') -- Apenas reports que precisam de atenção
GROUP BY
    R.idReport, R.titulo, R.dataCriacao
HAVING
    COUNT(I.idInteracao) >= 2 -- Reports de alta relevância (2 ou mais interações/engajamento)
    AND (NOW() - (SELECT MAX(dataHoraAtualizacao) FROM HistoricoAtualizacao WHERE idReport = R.idReport)) > INTERVAL '2 days' -- Sem atualização há mais de 2 dias
ORDER BY
    TotalInteracoes DESC, UltimaAtualizacaoFuncionario ASC;