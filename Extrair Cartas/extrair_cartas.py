# extrair_cartas.py

import json

def extrair_dados_all_printings(caminho_entrada, caminho_saida):
    with open(caminho_entrada, encoding='utf-8') as f:
        all_data = json.load(f)

    cartas_reduzidas = {}

    for set_code, colecao in all_data.get('data', {}).items():
        nome_colecao = colecao.get('name', 'Desconhecida')
        cartas = colecao.get('cards', [])

        cartas_simplificadas = []
        for carta in cartas:
            cartas_simplificadas.append({
                "name": carta.get("name"),
                "rarity": carta.get("rarity"),
                "types": carta.get("types"),
                "colors": carta.get("colors"),
                "manaCost": carta.get("manaCost"),
                "setCode": set_code,
            })

        cartas_reduzidas[set_code] = {
            "name": nome_colecao,
            "cards": cartas_simplificadas
        }

    with open(caminho_saida, "w", encoding="utf-8") as f_out:
        json.dump(cartas_reduzidas, f_out, indent=2, ensure_ascii=False)

    print(f"Arquivo reduzido salvo como {caminho_saida}")


# Uso
if __name__ == "__main__":
    extrair_dados_all_printings(
        caminho_entrada="AllPrintings.json",
        caminho_saida="cartas_base.json"
    )
