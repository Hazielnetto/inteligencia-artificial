import random
import matplotlib.pyplot as plt

"""class percepcao:
    posicao = (int, int)
    status = str

def agenteReativoSimples(percepcao: percepcao):
    return percepcao.status"""

def embaralha(matrix):

    # Encontrar as posições dos elementos a serem embaralhados
    posicoes = [(i, j) for i in range(len(matrix)) for j in range(len(matrix[0])) if matrix[i][j] != 1]

    # Criar uma lista com os valores a serem embaralhados
    valores_embaralhar = [matrix[i][j] for i, j in posicoes]

    # Embaralhar a lista de posições
    random.shuffle(posicoes)

    # Embaralhar os valores na matriz
    for i, (x, y) in enumerate(posicoes):
        matrix[x][y] = valores_embaralhar[i]

    return matrix

def novaMatriz():

    matrix = [
        [1, 1, 1, 1, 1, 1],
        [1, 2, 0, 0, 0, 1],
        [1, 2, 0, 0, 0, 1],
        [1, 2, 0, 0, 0, 1],
        [1, 2, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1],
    ]

    return embaralha(matrix)

def limpa(matriz, x, y):

    if matriz[x][y] == 2 or matriz[0][y] == 2:
        matriz[x][y] = 0

    return matriz

def mapeamento(posicaoInicial: tuple, matrix, inverte):

    (x, y) = posicaoInicial
    print(posicaoInicial)

    if inverte == 0:
        if x < 4 and y % 2 != 0:
            x += 1

        if x > 1 and y % 2 == 0:
            x -= 1
    else:
        if x > 1 and y % 2 != 0:
            x -= 1

        if x < 4 and y % 2 == 0:
            x += 1

    return x, y

# Função que exibe o ambiente na tela
def exibir(matrix):
    # Altera o esquema de cores do ambiente

    i = 0
    y = 1

    plt.ion()

    while i <= 5:

        #plt.pause(0.3)

        if i == 1 and y == 4:
            inverte = 1
            print('inverso')
            matrix = novaMatriz()

        if i == 1 and y == 1:

            print('normal')
            inverte = 0

        if i == 0 and y == 1:
            print('normal')
            inverte = 0
            matrix = novaMatriz()

        proximaCasa, y = mapeamento((i,y), matrix, inverte)

        if inverte == 0:
            # Coloca o agente no ambiente

            if y%2 != 0:
                if i == 4:
                    y += 1
                if y % 2 != 0:
                    i += 1

            if y%2 == 0:
                if i == 1:
                    y += 1
                if y % 2 == 0 and proximaCasa < i:
                    i -= 1

        else:
            if y%2 == 0:
                if i == 4:
                    y -= 1
                if y % 2 == 0:
                    i += 1

            if y%2 != 0:
                if i == 1:
                    y -= 1
                if y % 2 != 0 and proximaCasa < i:
                    i -= 1

        matrix = limpa(matrix, y, i)

        plt.imshow(matrix)
        plt.nipy_spectral()

        plt.plot([proximaCasa], [y], marker='o', color='r', ls='')

        plt.draw()
        plt.pause(0.4)
        plt.clf()

        #if y == 6:
            #plt.pause(1)
            #mapeamento((proximaCasa, y))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    exibir(novaMatriz())
