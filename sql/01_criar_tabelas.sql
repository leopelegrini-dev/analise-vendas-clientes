CREATE TABLE clientes (
    id_cliente     SERIAL PRIMARY KEY,
    nome           VARCHAR(100) NOT NULL,
    email          VARCHAR(100) UNIQUE NOT NULL,
    cidade         VARCHAR(60),
    estado         CHAR(2),
    data_cadastro  DATE NOT NULL
);

CREATE TABLE produtos (
    id_produto  SERIAL PRIMARY KEY,
    nome        VARCHAR(100) NOT NULL,
    categoria   VARCHAR(50) NOT NULL,
    preco       NUMERIC(10,2) NOT NULL CHECK (preco > 0)
);

CREATE TABLE pedidos (
    id_pedido    SERIAL PRIMARY KEY,
    id_cliente   INT NOT NULL REFERENCES clientes(id_cliente),
    data_pedido  DATE NOT NULL,
    status       VARCHAR(20) NOT NULL
);

CREATE TABLE itens_pedido (
    id_item         SERIAL PRIMARY KEY,
    id_pedido       INT NOT NULL REFERENCES pedidos(id_pedido),
    id_produto      INT NOT NULL REFERENCES produtos(id_produto),
    quantidade      INT NOT NULL CHECK (quantidade > 0),
    preco_unitario  NUMERIC(10,2) NOT NULL CHECK (preco_unitario > 0)
);