# db.py

import sqlite3

# Função para criar o banco de dados e tabelas
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # Criação das tabelas
    c.execute('''CREATE TABLE IF NOT EXISTS colecoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT UNIQUE)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS cartas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    colecao_id INTEGER,
                    preco REAL,
                    status TEXT,
                    FOREIGN KEY(colecao_id) REFERENCES colecoes(id))''')
    
    conn.commit()
    conn.close()

# Função para adicionar uma coleção
def adicionar_colecao(nome):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute("INSERT OR IGNORE INTO colecoes (nome) VALUES (?)", (nome,))
    
    conn.commit()
    conn.close()

# Função para adicionar uma carta a uma coleção
def adicionar_carta(nome, colecao_nome, preco):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # Verifica se a coleção existe
    c.execute("SELECT id FROM colecoes WHERE nome = ?", (colecao_nome,))
    colecao = c.fetchone()
    if colecao:
        colecao_id = colecao[0]
        c.execute("INSERT INTO cartas (nome, colecao_id, preco, status) VALUES (?, ?, ?, ?)",
                  (nome, colecao_id, preco, 'disponível'))
        conn.commit()
    else:
        print("Coleção não encontrada!")
    
    conn.close()

# Função para listar as cartas de uma coleção
def listar_cartas(colecao_nome):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute('''SELECT c.nome, c.preco, c.status 
                 FROM cartas c
                 JOIN colecoes co ON c.colecao_id = co.id
                 WHERE co.nome = ?''', (colecao_nome,))
    
    cartas = c.fetchall()
    conn.close()
    
    return cartas
