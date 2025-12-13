import sqlite3


def iniciarBanco(conexao):
    print("\n--- INICIANDO CONFIGURACAO DO SISTEMA MOTO PECAS ---\n")
    cursor = conexao.cursor()
    codigo_sql = """
    CREATE TABLE  IF NOT EXISTS pecas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco REAL NOT NULL,
        quantidade INTENGER NOT NULL
    )
    """
    cursor.execute(codigo_sql)
    print("SUCESSO: Cofiguracao concluida.\n")
    conexao.commit()


def exibirEstoque(conexao):
    print("\n--- SISTEMA MOTO PECAS: RELATORIO GERAL ---\n")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM pecas")
    todas_as_pecas = cursor.fetchall()
    print("-" * 50)
    print(f"{'ID':<5} | {'NOME':<20} | {'PRECO':<10} | {'QTD':<5}")
    print("-" * 50)
    for peca in todas_as_pecas:
        id_peca = peca[0]
        nome = peca[1]
        preco = peca[2]
        qtd = peca[3]
        print(f"{id_peca:<5} | {nome:<20} | R$ {preco:<7.2f} | {qtd:<5}")
        print("-" * 50)
    print("\n[ALERTA DO GERENTE] Pecas de Alto Valor (> R$ 200):")
    for peca in todas_as_pecas:
        nome = peca[1]
        preco = peca[2]

        if preco > 200:
            print(f"-> ATENCAO: O {nome} custa R$ {preco:.2f}!")


def deletar_peca(conexao, id_peca):
    cursor = conexao.cursor()
    print("--- REMOVER PEcA DO SISTEMA ---")
    id_peca = int(
        input("Digite o ID da peca que deseja EXCLUIR para sempre: "))
    comando_sql = "DELETE FROM pecas WHERE id=?"
    cursor.execute(comando_sql, (id_peca,))
    conexao.commit()
    print(f"\nSUCESSO: A peça de ID {id_peca} foi removida do banco de dados.")


def cadastrar_peca(conexao):
    while True:
        cursor = conexao.cursor()
        dados_peca = ler_dados_produto()
        comando_sql = "INSERT INTO pecas (nome, preco, quantidade) VALUES (?, ?, ?)"
        cursor.execute(
            comando_sql, (dados_peca["nome"], dados_peca["preco"], dados_peca["qtd_peca"]))
        conexao.commit()
        print(f"\nSUCESSO: A peca {dados_peca["nome"]} foi cadastrada!\n")
        res = int(
            input("Digite ENTER para cadastrar outro produto ou 9 para SAIR -> "))
        if res == 9:
            break


def ler_dados_produto():
    nome_peca = input("Digite o nome da peca: ", 1)
    preco_peca = float(ler_valor("Digite o preco (ex: 150. 50): ", 1))
    qtd_peca = ler_valor("Digite a quantidade em estoque: ")
    return {"nome": nome_peca, "preco": preco_peca, "qtd_peca": qtd_peca}


def ler_valor(texto, tipo_valor=0):
    if tipo_valor:
        while True:
            try:
                entrada = int(input(texto))
                if entrada <= 0:
                    raise ValueError
                break
            except ValueError:
                print("\nErro: O valor precisa ser numerico e maior que ZERO!\n")

    else:
        while True:
            try:
                entrada = input(texto).strip()
                if (entrada.isdigit()) or (not entrada):
                    raise ValueError
                break
            except ValueError:
                print(
                    "\nErro: O nome NÃO pode ter apenas numeros e tambem nao pode ser vazio\n")


def atualizarDados(conexao, id):
    atualizacao = int(input(
        "O que voce quer atualizar?\n1. Entradas no Estoque\n2. Saidas do Estoque\n3. Preco\n4. Nome\nDigite uma opcao -> "))
    if atualizacao == 1:
        if (atualizar_quantidade(conexao, id, 1)) == 0:
            print(
                f"\nSUCESSO: A quantidade do produto (ID {id}) foi atualizado!")
    elif atualizacao == 2:
        if (atualizar_quantidade(conexao, id, 0)) == 0:
            print(
                f"\nSUCESSO: A quantidade do produto (ID {id}) foi atualizado!")
    elif atualizacao == 3:
        if (atualizar_preco(conexao, id)) == 0:
            print(f"\nSUCESSO: O preço do produto (ID {id}) foi atualizado!")
    elif atualizacao == 4:
        if (atualizar_nome(conexao, id)) == 0:
            print(f"\nSUCESSO: O nome do produto (ID {id}) foi atualizado!")
    else:
        print("Opcao invalida!\n")


def atualizar_preco(conexao, id_peca):
    cursor = conexao.cursor()
    novo_preco = float(input("Digite o NOVO preco da peca: "))
    comando_sql = "UPDATE pecas SET preco=?  WHERE id=?"
    cursor.execute(comando_sql, (novo_preco, id_peca))
    conexao.commit()
    return 0


def atualizar_nome(conexao, id_peca):
    cursor = conexao.cusor()
    novo_nome = input("Digite o NOVO nome da peca: ")
    comando_sql = "UPDATE pecas SET nome=? WHERE id=?"
    cursor.execute(comando_sql, (novo_nome, id_peca))
    conexao.commit()
    return 0


def atualizar_quantidade(conexao, id_peca, entrada_saida):
    cursor = conexao.cursor()
    if entrada_saida:
        entrada = int(
            input(("Digite quantas unidades do produto entraram no estoque -> ")))
        comando_sql = "UPDATE pecas SET quantidade=quantidade+? WHERE id=?"
        cursor.execute(comando_sql, (entrada, id_peca))
        conexao.commit()
        return 0
    else:
        saida = int(
            input("Digite quantas unidades do produto sairam de estoque -> "))
        comando_sql = "UPDATE pecas SET quantidade=quantidade-? WHERE id=?"
        cursor.execute(comando_sql, (saida, id_peca))
        conexao.commit()
        return 0


def menu():
    loop = 1
    while loop:
        print("           Menu de Opcoes\n")
        print("1. Exibir Estoque\n2. Cadastrar no Estoque\n3. Atualizar Estoque\n4. Apagar do Estoque\n0. SAIR\n")
        try:
            res = int(input("Digite uma opcao acima -> "))
            loop = 0
        except ValueError:
            print("\nDigite apenas numeros!\n")
    return res


def main():
    conexao = sqlite3.connect('estoque.db')
    iniciarBanco(conexao)

    while True:
        print("\n----- SISTEMA DE GERENCIAMENTO DE ESTOQUE -----\n\n")
        opcao = menu()
        if opcao == 0:
            break
        elif opcao == 1:
            exibirEstoque(conexao)
        elif opcao == 2:
            cadastrar_peca(conexao)
        elif opcao == 3:
            exibirEstoque()
            id_da_peca = int(
                input("Digite o ID da peca que deseja atualizar -> "))
            atualizarDados(conexao, id_da_peca)
        elif opcao == 4:
            deletar_peca()

    conexao.close()


if __name__ == "__main__":
    main()
