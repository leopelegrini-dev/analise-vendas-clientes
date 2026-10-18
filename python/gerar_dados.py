import os
import random
from datetime import date, timedelta

import pandas as pd
from dotenv import load_dotenv
from faker import Faker
from sqlalchemy import create_engine, text

load_dotenv()

url = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
engine = create_engine(url)

random.seed(42)
fake = Faker("pt_BR")
Faker.seed(42)

estados = ["SP", "RJ", "MG", "PR", "RS", "BA", "SC", "PE"]

clientes = []
for i in range(500):
    clientes.append({
        "nome": fake.name(),
        "email": f"cliente{i+1}@exemplo.com",
        "cidade": fake.city(),
        "estado": random.choice(estados),
        "data_cadastro": date(2023, 1, 1) + timedelta(days=random.randint(0, 700)),
    })
df_clientes = pd.DataFrame(clientes)


catalogo = {
    "Eletrônicos": [("Fone Bluetooth", 149.90), ("Carregador Turbo", 79.90),
                    ("Smartwatch", 399.00), ("Caixa de Som", 199.90),
                    ("Mouse Sem Fio", 59.90), ("Teclado Mecânico", 249.90),
                    ("Webcam HD", 129.90), ("Power Bank", 119.90)],
    "Casa": [("Jogo de Panelas", 289.90), ("Aspirador Portátil", 179.90),
             ("Luminária LED", 69.90), ("Jogo de Cama", 129.90),
             ("Cafeteira", 159.90), ("Organizador", 39.90),
             ("Ventilador", 189.90), ("Garrafa Térmica", 49.90)],
    "Moda": [("Camiseta Básica", 39.90), ("Calça Jeans", 129.90),
             ("Tênis Casual", 219.90), ("Jaqueta", 249.90),
             ("Boné", 49.90), ("Mochila", 119.90),
             ("Meias (Kit)", 29.90), ("Relógio Casual", 159.90)],
    "Esportes": [("Bola de Futebol", 89.90), ("Tapete de Yoga", 69.90),
                 ("Halteres 5kg", 99.90), ("Corda de Pular", 24.90),
                 ("Squeeze", 19.90), ("Luva de Treino", 44.90),
                 ("Bicicleta Ergométrica", 899.00), ("Faixa Elástica", 34.90)],
    "Livros": [("Livro de SQL", 79.90), ("Livro de Python", 89.90),
               ("Romance Best-seller", 49.90), ("Livro de Finanças", 59.90),
               ("HQ Clássica", 39.90), ("Livro Infantil", 34.90),
               ("Guia de Dados", 69.90), ("Biografia", 54.90)],
}

produtos = [
    {"nome": nome, "categoria": cat, "preco": preco}
    for cat, itens in catalogo.items()
    for nome, preco in itens
]
df_produtos = pd.DataFrame(produtos)

with engine.begin() as conn:
    conn.execute(text(
        "TRUNCATE itens_pedido, pedidos, produtos, clientes RESTART IDENTITY CASCADE"
    ))

df_clientes.to_sql("clientes", engine, if_exists="append", index=False)
df_produtos.to_sql("produtos", engine, if_exists="append", index=False)

status_opcoes = ["entregue"] * 85 + ["cancelado"] * 7 + ["enviado"] * 5 + ["pendente"] * 3

pedidos = []
for _ in range(3000):
    pedidos.append({
        "id_cliente": random.randint(1, 500),
        "data_pedido": date(2024, 1, 1) + timedelta(days=random.randint(0, 659)),
        "status": random.choice(status_opcoes),
    })
df_pedidos = pd.DataFrame(pedidos)
df_pedidos.to_sql("pedidos", engine, if_exists="append", index=False)

itens = []
for id_pedido in range(1, 3001):
    qtd_itens = random.randint(1, 4)
    produtos_sorteados = random.sample(range(1, 41), qtd_itens)
    for id_produto in produtos_sorteados:
        preco = df_produtos.loc[id_produto - 1, "preco"]
        itens.append({
            "id_pedido": id_pedido,
            "id_produto": id_produto,
            "quantidade": random.randint(1, 3),
            "preco_unitario": float(preco),
        })
df_itens = pd.DataFrame(itens)
df_itens.to_sql("itens_pedido", engine, if_exists="append", index=False)

os.makedirs("data", exist_ok=True)
df_clientes.to_csv("data/clientes.csv", index=False)
df_produtos.to_csv("data/produtos.csv", index=False)
df_pedidos.to_csv("data/pedidos.csv", index=False)
df_itens.to_csv("data/itens_pedido.csv", index=False)

print("Dados gerados com sucesso!")
print(f"Clientes: {len(df_clientes)} | Produtos: {len(df_produtos)}")
print(f"Pedidos: {len(df_pedidos)} | Itens: {len(df_itens)}")