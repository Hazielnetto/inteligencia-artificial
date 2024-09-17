import numpy as np
import matplotlib.pyplot as plt


class Agente:
    def __init__( self, posicao ):
        self.posicao = posicao

    def perceber( self, matriz ):
        x, y = self.posicao
        return matriz[x][y]

    def acao( self, percepcao ):
        if percepcao == 2:
            return 'aspirar'
        else:
            return 'mover'


def geraCaminho( matriz ):
    linhas = len( matriz )
    colunas = len( matriz[0] )
    caminho = []

    for i in range( linhas ):
        if i % 2 == 0:
            # Linhas pares: da esquerda para a direita
            for j in range( colunas ):
                if matriz[i][j] != 1:
                    caminho.append( (i, j) )
        else:
            # Linhas ímpares: da direita para a esquerda
            for j in range( colunas - 1, -1, -1 ):
                if matriz[i][j] != 1:
                    caminho.append( (i, j) )

    return caminho


def geraMatriz( rows, cols ):
    # Initialize the array with all 0s
    arr = np.zeros( (rows, cols), dtype=int )

    # Set the borders to 1
    arr[0, :] = 1
    arr[-1, :] = 1
    arr[:, 0] = 1
    arr[:, -1] = 1

    # Randomly switch some 0s to 2s
    num_switches = int( rows * cols * 0.2 )  # adjust this value to control the number of switches
    for _ in range( num_switches ):
        row_idx = np.random.randint( 1, rows - 1 )
        col_idx = np.random.randint( 1, cols - 1 )
        if arr[row_idx, col_idx] == 0:
            arr[row_idx, col_idx] = 2

    return arr


def plota( posicao ):
    plt.imshow( matriz )
    plt.nipy_spectral()
    plt.plot( posicao[1], posicao[0], 'ro' )  # Plotar o agente
    plt.pause( 0.4 )
    plt.clf()


def limpa( posicao ):
    matriz[posicao] = 0


def inicia( matriz, posicaoInicial ):
    caminho = geraCaminho( matriz )
    plt.ion()

    i = 0
    while True:
        posicao = caminho[i]

        agente = Agente( posicao )
        percepcao = agente.perceber( matriz )
        acao = agente.acao( percepcao )

        plota( posicao )

        if acao == 'aspirar':
            limpa( posicao )
        else:
            i += 1

    """while True:
        if inverte:
            for posicao in reversed(caminho):
                if agente.agir != 'aspirar':
                    agente = Agente(posicao)
                    percepcao = agente.perceber(matriz)
                    acao = agente.agir(percepcao)
                    plota(posicao)

                else:
                    matriz[posicao] = 0
                    plota(posicao)                   

            inicia(matriz, posicao, False)

        else:
            for posicao in caminho:
                if agente.agir != 'aspirar':
                    agente = Agente(posicao)
                    percepcao = agente.perceber(matriz)
                    acao = agente.agir(percepcao)
                    plota(posicao)

                else:
                    matriz[posicao] = 0
                    plota(posicao)

            inicia(matriz, posicao, True)"""


if __name__ == '__main__':
    altura, largura = 7, 7
    matriz = geraMatriz( altura, largura )
    posicaoInicial = (3, 5)
    inicia( matriz, posicaoInicial )