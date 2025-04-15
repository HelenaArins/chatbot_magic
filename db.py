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

def buscar_colecoes_por_nome_parcial(parte_nome):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute("SELECT nome FROM colecoes WHERE nome LIKE ?", (f"%{parte_nome}%",))
    resultados = [row[0] for row in c.fetchall()]

    conn.close()
    return resultados


# Excluir carta (por nome + coleção)
def excluir_carta(nome_carta, nome_colecao):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute('''SELECT id FROM colecoes WHERE nome = ?''', (nome_colecao,))
    colecao = c.fetchone()
    if colecao:
        colecao_id = colecao[0]
        c.execute('''DELETE FROM cartas 
                     WHERE nome = ? AND colecao_id = ?''', (nome_carta, colecao_id))
        conn.commit()
        print(f"Carta '{nome_carta}' excluída da coleção '{nome_colecao}'.")
    else:
        print("Coleção não encontrada.")

    conn.close()

# Excluir coleção (e suas cartas)
def excluir_colecao(nome_colecao):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # Verifica se a coleção existe
    c.execute("SELECT id FROM colecoes WHERE nome = ?", (nome_colecao,))
    colecao = c.fetchone()
    if colecao:
        colecao_id = colecao[0]
        c.execute("DELETE FROM cartas WHERE colecao_id = ?", (colecao_id,))
        c.execute("DELETE FROM colecoes WHERE id = ?", (colecao_id,))
        conn.commit()
        print(f"Coleção '{nome_colecao}' e todas as suas cartas foram excluídas.")
    else:
        print("Coleção não encontrada.")

    conn.close()

def alterar_preco_carta(nome_carta, nome_colecao, novo_preco):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute("SELECT id FROM colecoes WHERE nome = ?", (nome_colecao,))
    colecao = c.fetchone()

    if not colecao:
        print("Coleção não encontrada.")
        conn.close()
        return

    colecao_id = colecao[0]

    # Verifica se a carta existe
    c.execute("SELECT id FROM cartas WHERE nome = ? AND colecao_id = ?", (nome_carta, colecao_id))
    carta = c.fetchone()

    if carta:
        c.execute("UPDATE cartas SET preco = ? WHERE id = ?", (novo_preco, carta[0]))
        conn.commit()
        print(f"Preço da carta '{nome_carta}' atualizado para R${novo_preco:.2f}")
    else:
        print("Carta não encontrada nesta coleção.")

    conn.close()

def buscar_cartas_por_nome_parcial(parte_nome):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute('''
        SELECT c.nome, co.nome 
        FROM cartas c
        JOIN colecoes co ON c.colecao_id = co.id
        WHERE c.nome LIKE ?
    ''', (f"%{parte_nome}%",))

    resultados = c.fetchall()
    conn.close()
    return resultados  # Lista de tuplas (nome_carta, nome_colecao)
