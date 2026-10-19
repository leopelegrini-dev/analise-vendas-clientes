SELECT SUM(i.quantidade * i.preco_unitario) AS faturamento_total
FROM itens_pedido i
JOIN pedidos p ON p.id_pedido = i.id_pedido
WHERE p.status <> 'cancelado';

SELECT COUNT(*) AS total_pedidos
FROM pedidos
WHERE status <> 'cancelado';

SELECT
    SUM(i.quantidade * i.preco_unitario) / COUNT(DISTINCT p.id_pedido) AS ticket_medio
FROM itens_pedido i
JOIN pedidos p ON p.id_pedido = i.id_pedido
WHERE p.status <> 'cancelado';

SELECT pr.nome, pr.categoria, SUM(i.quantidade) AS qtd_vendida
FROM itens_pedido i
JOIN pedidos p   ON p.id_pedido = i.id_pedido
JOIN produtos pr ON pr.id_produto = i.id_produto
WHERE p.status <> 'cancelado'
GROUP BY pr.nome, pr.categoria
ORDER BY qtd_vendida DESC
LIMIT 10;

SELECT
    pr.categoria,
    SUM(i.quantidade * i.preco_unitario) AS faturamento,
    ROUND(
        100.0 * SUM(i.quantidade * i.preco_unitario)
        / SUM(SUM(i.quantidade * i.preco_unitario)) OVER (),
        2
    ) AS pct_do_total
FROM itens_pedido i
JOIN pedidos p   ON p.id_pedido = i.id_pedido
JOIN produtos pr ON pr.id_produto = i.id_produto
WHERE p.status <> 'cancelado'
GROUP BY pr.categoria
ORDER BY faturamento DESC;

SELECT
    DATE_TRUNC('month', p.data_pedido)::date AS mes,
    SUM(i.quantidade * i.preco_unitario) AS faturamento,
    COUNT(DISTINCT p.id_pedido) AS pedidos
FROM itens_pedido i
JOIN pedidos p ON p.id_pedido = i.id_pedido
WHERE p.status <> 'cancelado'
GROUP BY 1
ORDER BY 1;

WITH receita_pedido AS (
    SELECT
        p.id_pedido,
        p.id_cliente,
        SUM(i.quantidade * i.preco_unitario) AS valor
    FROM pedidos p
    JOIN itens_pedido i ON i.id_pedido = p.id_pedido
    WHERE p.status <> 'cancelado'
    GROUP BY p.id_pedido, p.id_cliente
)
SELECT
    c.nome,
    c.estado,
    COUNT(*) AS pedidos,
    SUM(r.valor) AS total_gasto,
    ROUND(AVG(r.valor), 2) AS ticket_medio
FROM receita_pedido r
JOIN clientes c ON c.id_cliente = r.id_cliente
GROUP BY c.id_cliente, c.nome, c.estado
ORDER BY total_gasto DESC
LIMIT 10;

WITH receita_pedido AS (
    SELECT
        p.id_pedido,
        p.id_cliente,
        SUM(i.quantidade * i.preco_unitario) AS valor
    FROM pedidos p
    JOIN itens_pedido i ON i.id_pedido = p.id_pedido
    WHERE p.status <> 'cancelado'
    GROUP BY p.id_pedido, p.id_cliente
)
SELECT
    c.nome,
    c.estado,
    COUNT(*) AS pedidos,
    SUM(r.valor) AS total_gasto,
    ROUND(AVG(r.valor), 2) AS ticket_medio
FROM receita_pedido r
JOIN clientes c ON c.id_cliente = r.id_cliente
GROUP BY c.id_cliente, c.nome, c.estado
ORDER BY total_gasto DESC
LIMIT 10;