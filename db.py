# db.py

import sqlite3
import requests



def obter_dados_scryfall(nome_carta):
    url = f"https://api.scryfall.com/cards/named?exact={nome_carta}"
    response = requests.get(url)
    
    if response.status_code == 200:
        dados = response.json()
        # Extraindo as informações principais
        nome = dados['name']
        preco = dados.get('prices', {}).get('usd', None)  # Preço em USD, se disponível
        colecao = dados['set']
        tipo = dados['type_line']
        raridade = dados['rarity']
        
        return {
            'nome': nome,
            'preco': preco,
            'colecao': colecao,
            'tipo': tipo,
            'raridade': raridade
        }
    else:
        print(f"Erro ao consultar Scryfall: {response.status_code}")
        return None


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

def adicionar_carta(nome_carta, colecao_nome, preco=None):
    dados_carta = obter_dados_scryfall(nome_carta)
    
    if dados_carta:
        nome = dados_carta['nome']
        preco = preco if preco else dados_carta['preco']  # Usa o preço fornecido ou o da API
        colecao = dados_carta['colecao']
        
        # Verifica se a coleção existe no banco
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("SELECT id FROM colecoes WHERE nome = ?", (colecao_nome,))
        colecao_id = c.fetchone()
        
        if colecao_id:
            colecao_id = colecao_id[0]
            # Adiciona a carta no banco
            c.execute("INSERT INTO cartas (nome, colecao_id, preco, status) VALUES (?, ?, ?, ?)",
                      (nome, colecao_id, preco, 'disponível'))
            conn.commit()
            print(f"Carta '{nome}' adicionada à coleção '{colecao_nome}' com sucesso!")
        else:
            print(f"Coleção '{colecao_nome}' não encontrada!")
        
        conn.close()
    else:
        print(f"Não foi possível obter dados para a carta '{nome_carta}' da Scryfall.")


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
