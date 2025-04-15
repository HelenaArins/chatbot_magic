# chatbot.py

import db
import cartas_json

cartas_base = cartas_json.carregar_cartas_json()

def adicionar_carta_por_busca():
    nome_parcial = input("Digite o nome (ou parte) da carta: ")
    resultados = cartas_json.buscar_cartas_por_nome(nome_parcial, cartas_base)

    if not resultados:
        print("Nenhuma carta encontrada.")
        return

    print(f"\nForam encontradas {len(resultados)} carta(s):")
    for idx, carta in enumerate(resultados):
        print(f"{idx + 1}. {carta['nome']} - Coleção: {carta['colecao']}")

    escolha = input("\nDigite o número da carta que deseja adicionar ou '0' para cancelar: ")
    if escolha == "0":
        print("Operação cancelada.")
        return

    try:
        idx_escolhido = int(escolha) - 1
        carta_escolhida = resultados[idx_escolhido]
        preco = float(input("Digite o preço da carta: "))
        db.adicionar_colecao(carta_escolhida['colecao'])  # adiciona coleção se não existir
        db.adicionar_carta(carta_escolhida['nome'], carta_escolhida['colecao'], preco)
        print(f"Carta '{carta_escolhida['nome']}' adicionada com sucesso!")
    except (IndexError, ValueError):
        print("Escolha inválida.")


def adicionar_colecao_inteligente():
    while True:
        nome_parcial = input("Digite o nome da coleção (ou 'voltar' para cancelar): ")
        if nome_parcial.lower() == "voltar":
            continue

        resultados = cartas_json.buscar_colecao_por_nome_parcial(nome_parcial, cartas_base)

        if not resultados:
            print("Nenhuma coleção encontrada. Tente novamente.")
            continue

        # Caso só tenha um resultado
        if len(resultados) == 1:
            sugerida = resultados[0]["nome"]
            print(f"\nEncontramos apenas uma coleção chamada:\n\"{sugerida}\"")
            print("Digite:\n1 - Para adicionar essa coleção\n2 - Para criar nova com o nome que você digitou")
            print("3 - Para digitar novamente")
            escolha = input("Sua escolha: ")

            if escolha == "1":
                db.adicionar_colecao(sugerida)
                print(f"Coleção '{sugerida}' adicionada com sucesso!")
                break
            elif escolha == "2":
                db.adicionar_colecao(nome_parcial)
                print(f"Coleção '{nome_parcial}' adicionada com sucesso!")
                break
            elif escolha == "3":
                continue
            else:
                print("Opção inválida.")
                continue

        else:
            # Múltiplas opções encontradas
            print("\nColeções encontradas:")
            for i, col in enumerate(resultados):
                print(f"{i + 1}. {col['nome']}")
            print(f"{len(resultados) + 1}. Digitar novamente")
            escolha = input("Escolha o número da coleção desejada: ")
            try:
                idx = int(escolha)
                if 1 <= idx <= len(resultados):
                    nome_escolhido = resultados[idx - 1]["nome"]
                    db.adicionar_colecao(nome_escolhido)
                    print(f"Coleção '{nome_escolhido}' adicionada com sucesso!")
                    break
                elif idx == len(resultados) + 1:
                    continue
                else:
                    print("Opção inválida.")
            except ValueError:
                print("Por favor, digite um número.")


def menu():
    print("\n--- Chatbot de Cartas de Magic ---")
    print("1. Adicionar coleção")
    print("2. Adicionar carta manualmente")
    print("3. Listar cartas de uma coleção")
    print("4. Adicionar carta a partir do JSON")
    print("5. Excluir carta ou coleção")
    print("6. Alterar preço de uma carta")  # nova opção
    print("7. Sair")



# Interação
def interagir():
    while True:
        menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            adicionar_colecao_inteligente()
        
        elif opcao == "2":
            nome_carta = input("Digite o nome da carta: ")
            # colecao = input("Digite o nome da coleção: ")
            colecao_parcial = input("Digite o nome da coleção: ")
            colecao_resultados = cartas_json.buscar_colecao_por_nome_parcial(colecao_parcial, cartas_base)

            if not colecao_resultados:
                print("Coleção não encontrada.")
                return

            if len(colecao_resultados) == 1:
                colecao = colecao_resultados[0]["nome"]
            else:
                print("\nColeções encontradas:")
                for i, col in enumerate(colecao_resultados):
                    print(f"{i + 1}. {col['nome']}")
                escolha = input("Escolha o número da coleção desejada: ")
                try:
                    idx = int(escolha) - 1
                    colecao = colecao_resultados[idx]["nome"]
                except:
                    print("Escolha inválida.")
                    return

            preco = float(input("Digite o preço da carta: "))
            db.adicionar_carta(nome_carta, colecao, preco)
            print(f"Carta '{nome_carta}' adicionada à coleção '{colecao}'!")
        

        elif opcao == "3":
            while True:
                entrada = input("Digite o nome (ou parte) da coleção para listar as cartas: ")
                possiveis = db.buscar_colecoes_por_nome_parcial(entrada)

                if not possiveis:
                    print("Nenhuma coleção encontrada. Tente novamente.")
                    continue

                if len(possiveis) == 1:
                    nome_colecao = possiveis[0]
                    confirm = input(f"Você quis dizer '{nome_colecao}'? (s/n): ").lower()
                    if confirm != 's':
                        continue
                else:
                    print("\nColeções encontradas:")
                    for i, nome in enumerate(possiveis):
                        print(f"{i + 1}. {nome}")
                    print(f"{len(possiveis) + 1}. Digitar novamente")
                    escolha = input("Escolha a coleção: ")

                    try:
                        idx = int(escolha)
                        if 1 <= idx <= len(possiveis):
                            nome_colecao = possiveis[idx - 1]
                        elif idx == len(possiveis) + 1:
                            continue
                        else:
                            print("Opção inválida.")
                            continue
                    except ValueError:
                        print("Digite um número válido.")
                        continue

                # Listar cartas da coleção selecionada
                cartas = db.listar_cartas(nome_colecao)
                if cartas:
                    print(f"\nCartas disponíveis na coleção '{nome_colecao}':")
                    for carta in cartas:
                        nome, preco, status = carta
                        print(f"- {nome} | Preço: {preco} | Status: {status}")
                else:
                    print(f"Nenhuma carta encontrada na coleção '{nome_colecao}'.")
                break

        elif opcao == "4":
            adicionar_carta_por_busca()

        elif opcao == "5":
            print("\n--- Excluir ---")
            print("1. Excluir carta")
            print("2. Excluir coleção")
            sub_opcao = input("Escolha uma opção: ")

            if sub_opcao == "1":
                nome_carta = input("Digite o nome da carta que deseja excluir: ")
                nome_colecao_parcial = input("Digite o nome (ou parte) da coleção: ")
                resultados = db.buscar_colecoes_por_nome_parcial(nome_colecao_parcial)

                if not resultados:
                    print("Nenhuma coleção encontrada.")
                    continue
                elif len(resultados) == 1:
                    nome_colecao = resultados[0]
                else:
                    print("\nColeções encontradas:")
                    for i, nome in enumerate(resultados):
                        print(f"{i + 1}. {nome}")
                    escolha = input("Escolha a coleção: ")
                    try:
                        idx = int(escolha)
                        nome_colecao = resultados[idx - 1]
                    except:
                        print("Opção inválida.")
                        continue

                confirm = input(f"Confirmar exclusão da carta '{nome_carta}' da coleção '{nome_colecao}'? (s/n): ")
                if confirm.lower() == "s":
                    db.excluir_carta(nome_carta, nome_colecao)

            elif sub_opcao == "2":
                nome_colecao_parcial = input("Digite o nome (ou parte) da coleção que deseja excluir: ")
                resultados = db.buscar_colecoes_por_nome_parcial(nome_colecao_parcial)

                if not resultados:
                    print("Nenhuma coleção encontrada.")
                    continue
                elif len(resultados) == 1:
                    nome_colecao = resultados[0]
                else:
                    print("\nColeções encontradas:")
                    for i, nome in enumerate(resultados):
                        print(f"{i + 1}. {nome}")
                    escolha = input("Escolha a coleção: ")
                    try:
                        idx = int(escolha)
                        nome_colecao = resultados[idx - 1]
                    except:
                        print("Opção inválida.")
                        continue

                confirm = input(f"Tem certeza que deseja excluir a coleção '{nome_colecao}' e todas as suas cartas? (s/n): ")
                if confirm.lower() == "s":
                    db.excluir_colecao(nome_colecao)
               
        elif opcao == "6":
            parte_nome = input("Digite o nome (ou parte) da carta que deseja alterar (ou 'voltar' para cancelar): ")
            if parte_nome.lower() == "voltar":
                continue

            cartas_encontradas = db.buscar_cartas_por_nome_parcial(parte_nome)

            if not cartas_encontradas:
                print("Nenhuma carta encontrada.")
                continue

            elif len(cartas_encontradas) == 1:
                nome_carta, nome_colecao = cartas_encontradas[0]
                print(f"Encontramos uma carta: '{nome_carta}' da coleção '{nome_colecao}'")
            else:
                print("\nCartas encontradas:")
                for i, (nome, colecao) in enumerate(cartas_encontradas):
                    print(f"{i + 1}. {nome} | Coleção: {colecao}")
                print(f"{len(cartas_encontradas) + 1}. Digitar novamente")
                print(f"0. Voltar ao menu")
                escolha = input("Escolha a carta desejada: ")

                if escolha == "0":
                    continue

                try:
                    idx = int(escolha)
                    if 1 <= idx <= len(cartas_encontradas):
                        nome_carta, nome_colecao = cartas_encontradas[idx - 1]
                    elif idx == len(cartas_encontradas) + 1:
                        continue
                    else:
                        print("Opção inválida.")
                        continue
                except ValueError:
                    print("Digite um número válido.")
                    continue

            novo_preco_input = input(f"Digite o novo preço da carta '{nome_carta}' (ou 'voltar' para cancelar): R$ ")
            if novo_preco_input.lower() == "voltar":
                continue

            try:
                novo_preco = float(novo_preco_input)
            except:
                print("Preço inválido.")
                continue

            confirm = input(f"Confirmar alteração de preço de '{nome_carta}' para R${novo_preco:.2f}? (s/n): ")
            if confirm.lower() != "s":
                print("Alteração cancelada.")
                continue

            db.alterar_preco_carta(nome_carta, nome_colecao, novo_preco)


        elif opcao == "7":
            print("Saindo...")
            break

        else:
            print("Opção inválida! Tente novamente.")
# Inicia o banco de dados
db.init_db()

# Inicia a interação do chatbot
interagir()