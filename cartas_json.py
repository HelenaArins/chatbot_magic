# cartas_json.py

import json

# Carrega os dados do arquivo JSON
def carregar_cartas_json(caminho_arquivo="cartas_base.json"):
    with open(caminho_arquivo, encoding='utf-8') as f:
        data = json.load(f)
    return data

# Busca cartas por nome (parcial ou completo)
def buscar_cartas_por_nome(nome_busca, cartas_json):
    resultados = []
    for set_code, colecao in cartas_json.items():
        for carta in colecao.get("cards", []):
            if nome_busca.lower() in carta["name"].lower():
                resultados.append({
                    "nome": carta["name"],
                    "colecao": colecao["name"],
                    "set_code": set_code
                })
    return resultados

def buscar_colecao_por_nome_parcial(parte_nome, cartas_json):
    resultados = []
    for set_code, colecao in cartas_json.items():
        if parte_nome.lower() in colecao["name"].lower():
            resultados.append({
                "nome": colecao["name"],
                "set_code": set_code
            })
    return resultados

