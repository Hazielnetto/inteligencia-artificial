from random import randint
import numpy as np
import matplotlib.pyplot as plt
from collections import deque


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


def encontrarPosicoesDosDois( array ):
    posicoes = []
    for i in range( len( array ) ):
        for j in range( len( array[0] ) ):
            if array[i][j] == 2:
                posicoes.append( (i, j) )
    return posicoes


def posicaoValida( x, y, array, visitado ):
    if 0 <= x < len( array ) and 0 <= y < len( array[0] ) and not visitado[x][y]:
        return True
    return False


# Busca em Largura (BFS) para encontrar o menor caminho para um alvo
def bfs( array, inicio, alvo ):
    filas = deque( [(*inicio, [])] )  # Fila contendo a posição atual e o caminho percorrido
    visitado = [[False for _ in range( len( array[0] ) )] for _ in range( len( array ) )]
    visitado[inicio[0]][inicio[1]] = True

    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Cima, Baixo, Esquerda, Direita

    while filas:
        x, y, caminho = filas.popleft()

        # Se encontrou o alvo (2)
        if (x, y) == alvo:
            return caminho + [(x, y)]

        # Explorar as direções
        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy
            if posicaoValida( nx, ny, array, visitado ):
                visitado[nx][ny] = True
                filas.append( (nx, ny, caminho + [(nx, ny)]) )

    return []  # Caso não seja possível chegar ao alvo


def adicionarCaminho( caminho, posicaoAtual, proximoPasso ):
    xAtual, yAtual = posicaoAtual
    xProximo, yProximo = proximoPasso

    # Movimento na direção x
    while xAtual != xProximo:
        if xAtual < xProximo:
            xAtual += 1
        else:
            xAtual -= 1
        caminho.append( (xAtual, yAtual) )

    # Movimento na direção y
    while yAtual != yProximo:
        if yAtual < yProximo:
            yAtual += 1
        else:
            yAtual -= 1
        caminho.append( (xAtual, yAtual) )


def gerarCaminho( array, inicio ):
    totalMovimentos = 0
    caminho = []
    posicoesDosDois = encontrarPosicoesDosDois( array )
    posicaoAtual = inicio
    caminho.append( posicaoAtual )  # Adiciona a posição inicial ao caminho

    while posicoesDosDois:
        distancias = []
        caminhosBfs = []
        for alvo in posicoesDosDois:
            caminhoParaAlvo = bfs( array, posicaoAtual, alvo )
            distancias.append( (len( caminhoParaAlvo ), alvo) )
            caminhosBfs.append( caminhoParaAlvo )

        # Escolhe o alvo mais próximo
        menorDistancia, alvoMaisProximo = min( distancias )
        indiceDoCaminho = distancias.index( (menorDistancia, alvoMaisProximo) )

        # Adiciona o caminho até o alvo mais próximo célula por célula
        for proximoPasso in caminhosBfs[indiceDoCaminho][1:]:
            adicionarCaminho( caminho, posicaoAtual, proximoPasso )
            posicaoAtual = proximoPasso

        totalMovimentos += menorDistancia

        # Remove o alvo da lista
        posicoesDosDois.remove( alvoMaisProximo )

    return totalMovimentos, caminho


def gerarMatriz( rows, cols, incidencia ):
    # Inicializa a matriz com todos os valores em 0
    matriz = np.zeros( (rows, cols), dtype=int )

    # Define as bordas como 1
    matriz[0, :] = 1
    matriz[-1, :] = 1
    matriz[:, 0] = 1
    matriz[:, -1] = 1

    # Troca aleatoriamente alguns 0s por 2s
    numSwitches = int( rows * cols * incidencia )
    for _ in range( numSwitches ):
        rowIdx = np.random.randint( 1, rows - 1 )
        colIdx = np.random.randint( 1, cols - 1 )
        if matriz[rowIdx, colIdx] == 0:
            matriz[rowIdx, colIdx] = 2

    return matriz


def plotar( posicao ):
    plt.imshow( matriz )
    plt.nipy_spectral()
    plt.plot( posicao[1], posicao[0], 'ro' )  # Plotar o agente
    plt.pause( delay )
    plt.clf()


def limpar( posicao ):
    matriz[posicao] = 0


def checarObjetivo( matriz ):
    return 'limpo' if 2 not in matriz else 'sujo'


def iniciar( matriz, posicaoInicial ):
    movimentos, caminho = gerarCaminho( matriz, posicaoInicial )
    pontos = 0
    plt.ion()
    i = 0
    while True:
        objetivo = checarObjetivo( matriz )
        posicao = caminho[i]

        agente = Agente( posicao )
        percepcao = agente.perceber( matriz )
        acao = agente.acao( percepcao )

        plotar( posicao )
        if objetivo != 'limpo':
            if acao == 'aspirar':
                limpar( posicao )
            else:
                i += 1
            # pontos += 1
        else:
            break

    print( f"Total de movimentos/pontos: {movimentos}" )
    # print( f"Total de pontos: {pontos}" )
    print( f"Caminho do agente: {caminho}" )


if __name__ == '__main__':
    altura, largura = 6, 6
    delay = 0.3
    incidencia = 1  # Ajuste esse valor para controlar a quantidade de "2s"
    matriz = gerarMatriz( altura, largura, incidencia )
    posicaoInicial = (randint( 1, altura - 2 ), randint( 1, largura - 2 ))  # Inicializa o agente numa posição aleatória
    iniciar( matriz, posicaoInicial )
