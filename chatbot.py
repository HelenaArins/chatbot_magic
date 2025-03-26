# chatbot.py

import db

# Função para mostrar o menu de opções
def menu():
    print("\n--- Chatbot de Cartas de Jogos ---")
    print("1. Adicionar coleção")
    print("2. Adicionar carta")
    print("3. Listar cartas de uma coleção")
    print("4. Sair")

# Função para interagir com o usuário
def interagir():
    while True:
        menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome_colecao = input("Digite o nome da coleção: ")
            db.adicionar_colecao(nome_colecao)
            print(f"Coleção '{nome_colecao}' adicionada com sucesso!")
        
        elif opcao == "2":
            nome_carta = input("Digite o nome da carta: ")
            colecao = input("Digite o nome da coleção onde deseja adicionar a carta: ")
            preco = float(input("Digite o preço da carta: "))
            db.adicionar_carta(nome_carta, colecao, preco)
            print(f"Carta '{nome_carta}' adicionada à coleção '{colecao}'!")
        
        elif opcao == "3":
            colecao = input("Digite o nome da coleção para listar as cartas: ")
            cartas = db.listar_cartas(colecao)
            if cartas:
                print("\nCartas disponíveis na coleção:")
                for carta in cartas:
                    nome, preco, status = carta
                    print(f"- {nome} | Preço: {preco} | Status: {status}")
            else:
                print("Nenhuma carta encontrada nessa coleção.")
        
        elif opcao == "4":
            print("Saindo...")
            break

        else:
            print("Opção inválida! Tente novamente.")

# Inicia o banco de dados
db.init_db()

# Inicia a interação do chatbot
interagir()
