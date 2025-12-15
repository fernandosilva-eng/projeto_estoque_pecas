import sqlite3

# Configuração inicial do banco de dados
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
    conexao.commit()
    print("SUCESSO: Cofiguracao concluida.\n") # Mostra que houve exito na criação do banco
    

# Exibe o estoque armazenado no banco de dados e filtra 
def exibirEstoque(conexao):
    print("\n--- SISTEMA MOTO PECAS: RELATORIO GERAL ---\n")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM pecas")
    todas_as_pecas = cursor.fetchall()
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

        if preco > 200: # Filtro simples
            print(f"-> ATENCAO: O {nome} custa R$ {preco:.2f}!")


# Apaga um iten do banco através do seu id
def deletar_peca(conexao, id_peca):
    cursor = conexao.cursor()
    print("--- REMOVER PECA DO SISTEMA ---")
    comando_sql = "DELETE FROM pecas WHERE id=?"
    cursor.execute(comando_sql, (id_peca,))
    conexao.commit()
    print(f"\nSUCESSO: A peça de ID {id_peca} foi removida do banco de dados.")

# Loop para fazer o cadastro das peças
def cadastrar_peca(conexao):
    while True:
        cursor = conexao.cursor()
        dados_peca = ler_dados_produto() # Chama uma função especial para ler os dados
        comando_sql = "INSERT INTO pecas (nome, preco, quantidade) VALUES (?, ?, ?)"
        cursor.execute(
            comando_sql, (dados_peca["nome"], dados_peca["preco"], dados_peca["qtd_peca"]))
        conexao.commit()
        print(f"\nSUCESSO: A peca {dados_peca["nome"]} foi cadastrada!\n")
        res = input("Digite ENTER para cadastrar outro produto ou 0 (ZERO) para VOLTAR -> ")
        if res == '0':
            break

# Ler os dados com auxilio de uma função específica
def ler_dados_produto():
    nome_peca = ler_entrada_texto("Digite o nome da peca: ")
    preco_peca = float(ler_entrada_numerico("Digite o preco (ex: 150. 50): "))
    qtd_peca = ler_entrada_numerico("Digite a quantidade em estoque: ")
    return {"nome": nome_peca, "preco": preco_peca, "qtd_peca": qtd_peca}


# Função especialista em ler dados numericos e validalos
def ler_entrada_numerico(texto, fim_intervalo=0, ini_intervalo=0):
    while True:
        try:
            entrada = int(input(texto))
            if (entrada<ini_intervalo) or (fim_intervalo and entrada>fim_intervalo): # Verifica entrada é menor que o limite minimo ou se o 
                raise ValueError                                                     #fim tem algum valor e se esse valor é maior que o limite final         
            return entrada
        except ValueError: 
            print("\nErro: O valor precisa ser numerico e maior que ZERO!\n")


# Função especialista em ler dados de textos e validalos
def ler_entrada_texto(texto):
    while True:
        try:
            entrada = input(texto).strip()
            if (entrada.isdigit()) or (not entrada): # Verifica se é apenas numeros ou se não foi digitado nada
                raise ValueError
            return entrada
        except ValueError:
            print("\nErro: O nome NÃO pode ter apenas numeros e tambem nao pode ser vazio\n")


# Atualizar um iten do banco através do seu id
def atualizarDados(conexao, id):
    while True:             
            atualizacao = ler_entrada_numerico(
                "\nO que voce quer atualizar?\n1. Entradas no Estoque\n2. Saidas do Estoque\n3. Preco\n4. Nome\n0. VOLTAR\nDigite uma opcao -> ", 4)
            if atualizacao<0 or atualizacao>4:
                raise ValueError
            elif atualizacao == 1:
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
            elif atualizacao==0:
                break


def atualizar_preco(conexao, id_peca):
    cursor = conexao.cursor()
    novo_preco = float(ler_entrada_numerico("Digite o NOVO preco da peca -> "))
    comando_sql = "UPDATE pecas SET preco=?  WHERE id=?"
    cursor.execute(comando_sql, (novo_preco, id_peca))
    conexao.commit()
    return 0


def atualizar_nome(conexao, id_peca):
    cursor = conexao.cursor()
    novo_nome = ler_entrada_texto("Digite o NOVO nome da peca -> ")
    comando_sql = "UPDATE pecas SET nome=? WHERE id=?"
    cursor.execute(comando_sql, (novo_nome, id_peca))
    conexao.commit()
    return 0


def atualizar_quantidade(conexao, id_peca, entrada_saida):
    cursor = conexao.cursor()
    if entrada_saida:
        entradas = ler_entrada_numerico("\nDigite quantas unidades do produto entraram no estoque -> ")
        comando_sql = "UPDATE pecas SET quantidade = quantidade + ? WHERE id = ?"
        cursor.execute(comando_sql, (entradas, id_peca))
        conexao.commit()
        return 0
    else:
        saida = ler_entrada_numerico("\nDigite quantas unidades do produto sairam de estoque -> ")
        comando_sql = "UPDATE pecas SET quantidade = quantidade - ? WHERE id = ?"
        cursor.execute(comando_sql, (saida, id_peca))
        conexao.commit()
        return 0

# Primeiro menu de opções
def menu():
    print("           Menu de Opcoes\n")
    print("1. Exibir Estoque\n2. Cadastrar no Estoque\n3. Atualizar Estoque\n4. Apagar do Estoque\n0. SAIR\n")
    res = ler_entrada_numerico("Digite uma opcao acima -> ", 4)
    return res


# Script principal
def main():
    conexao = sqlite3.connect('estoque.db')
    iniciarBanco(conexao)

    while True:
        print("\n\n----- SISTEMA DE GERENCIAMENTO DE ESTOQUE -----\n\n")
        opcao = menu()
        if opcao == 0:
            break
        elif opcao == 1:
            exibirEstoque(conexao)
        elif opcao == 2:
            cadastrar_peca(conexao)
        elif opcao == 3:
            exibirEstoque(conexao)
            id_da_peca = ler_entrada_numerico("\nDigite o ID da peca que deseja atualizar -> ")
            atualizarDados(conexao, id_da_peca)
        elif opcao == 4:
            exibirEstoque(conexao)
            id_da_peca=ler_entrada_numerico("\nDigite o ID da peca que deseja EXCLUIR para sempre: ")
            deletar_peca(conexao, id_da_peca)

    # Encerrando a conexão com o banco
    conexao.close()


if __name__ == "__main__":
    main()
