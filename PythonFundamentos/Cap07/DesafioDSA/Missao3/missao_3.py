import random
import time

def create_matrix():
    max_rows = 8
    max_cols = 4
    matrix = [[1] * max_cols for _ in range(max_rows)]
    matrix[1][1] = 0
    matrix[2][2] = 0
    matrix[3][0] = 0
    matrix[4][2] = 0
    matrix[5][3] = 0
    matrix[6][1] = 0
    matrix[6][3] = 0
    matrix[7][1] = 0
    return matrix

def main():
    matrix = create_matrix()

    list_passos = [(0,0)]
    passo = (0, 0)
    direita = 0
    x = 0
    baixo = 0
    y = 0

    proximo_passo = True
    count = 0
    while(proximo_passo):
        block = True
        while (block):
            count = count + 1
            de_novo = True
            while (de_novo):
                de_novo = False

                if direita == len(matrix[0]):
                    direita = len(matrix[0]) - 1
                else:
                    direita = random.randrange(x, x + 2)

                if baixo == len(matrix):
                    baixo = len(matrix) - 1
                else:
                    baixo = random.randrange(y, y + 2)

                if list_passos[-1][0]==baixo & list_passos[-1][1]==direita:
                    de_novo = True
                if baixo == y & direita == x:
                    de_novo = True
                if baixo != y & direita != x:
                    de_novo = True
                if baixo == direita & y == x:
                    de_novo = True


            passo = (baixo, direita)
            x = direita
            y = baixo
            list_passos.append(passo)
            #     print(list_passos[count])

            if (matrix[list_passos[-1][0]][list_passos[-1][1]] == 1):
                block = False
            else:
                list_passos.remove(list_passos[-1])
                y = list_passos[-1][0]
                x = list_passos[-1][1]

        if list_passos[-1][0]==(len(matrix)-1) & list_passos[-1][1]==(len(matrix[0])-1):
            proximo_passo = False

if __name__ == "__main__":
    main()