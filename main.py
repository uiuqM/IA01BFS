# Tamanho do tabuleiro
n = int(input("Digite o tamanho do tabuleiro: "))


    # Função utilitária para verificar se i,j são índices válidos
    # para um tabuleiro de xadrez N*N casas

def isSafe(x, y, tabuleiro):
    if(x >= 0 and y >= 0 and x < n and y < n and tabuleiro[x][y] == -1):
        return True
    return False


   
    # Função utilitária para imprimir a matriz do tabuleiro de xadrez

def printSolution(n, tabuleiro):
    for i in range(n):
        for j in range(n):
            print(tabuleiro[i][j], end=' ')
        print()


    # Essa função resolve o problema do Passeio do Cavalo usando
    # Backtracking. Esta função usa principalmente solveKTUtil()
    # para resolver o problema. Ela retorna falso se nenhum passeio completo
    # é possível, caso contrário retorna verdadeiro e imprime o
    # passeio.
    # Pode haver mais de uma solução, esta função imprime uma das soluções
    # viáveis.

def solveKT(n):

    # Inicialização da matriz do tabuleiro
    tabuleiro = [[-1 for i in range(n)]for i in range(n)]

    # move_x e move_y definem o próximo movimento do cavalo.
    # move_x é para o próximo valor da coordenada x
    # move_y é para o próximo valor da coordenada y
    move_x = [2, 1, -1, -2, -2, -1, 1, 2]
    move_y = [1, 2, 2, 1, -1, -2, -2, -1]

    # Como o cavalo está inicialmente no primeiro bloco
    tabuleiro[0][0] = 0

    # Contador de passos para a posição do cavalo
    pos = 1

    # Verificando se a solução existe ou não
    if(not solveKTUtil(n, tabuleiro, 0, 0, move_x, move_y, pos)):
        print("Solução inexistente")
    else:
        printSolution(n, tabuleiro)



    # Função utilitária recursiva para resolver o problema do 
    # passeio do cavalo

def solveKTUtil(n, tabuleiro, curr_x, curr_y, move_x, move_y, pos):

    if(pos == n**2):
        return True

    # Tenta todos os próximos movimentos do cavalo a partir da posição atual x, y
    for i in range(8):
        new_x = curr_x + move_x[i]
        new_y = curr_y + move_y[i]
        if(isSafe(new_x, new_y, tabuleiro)):
            tabuleiro[new_x][new_y] = pos
            if(solveKTUtil(n, tabuleiro, new_x, new_y, move_x, move_y, pos+1)):
                return True

            # Backtracking
            tabuleiro[new_x][new_y] = -1
    return False


# código principal
if __name__ == "__main__":
    
    # chamada da função solveKT
    solveKT(n)