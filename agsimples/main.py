import numpy as np
import matplotlib.pyplot as plt
import random

class Agente:
    def __init__(self, posicao):
        self.posicao = posicao

    def perceber(self, matriz):
        x, y = self.posicao
        if matriz[x][y] == 2:  # Sujo
            return (self.posicao, 'sujo')
        else:
            return (self.posicao, 'limpo')

def agenteReativoSimples(percepcao, voltar):
    posicao, status = percepcao
    x, y = posicao

    if status == 'sujo':
        return 'aspirar'
    else:
        if not voltar:
            if x % 2 == 1:
                if y < 4:
                    return 'direita'
                else:
                    return 'abaixo' if x < 5 else None
            else:
                if y > 1:
                    return 'esquerda'
                else:
                    return 'abaixo' if x < 5 else None
        else:
            if x % 2 == 1:
                if y > 1:
                    return 'esquerda'
                else:
                    return 'acima' if x > 1 else None
            else:
                if y < 4:
                    return 'direita'
                else:
                    return 'acima' if x > 1 else None

def gerarMatriz( rows, cols, incidencia ):
    matriz = np.zeros( (rows, cols), dtype=int )

    matriz[0, :] = 1
    matriz[-1, :] = 1
    matriz[:, 0] = 1
    matriz[:, -1] = 1

    numSwitches = int( rows * cols * incidencia )
    for _ in range( numSwitches ):
        rowIdx = np.random.randint( 1, rows - 1 )
        colIdx = np.random.randint( 1, cols - 1 )
        if matriz[rowIdx, colIdx] == 0:
            matriz[rowIdx, colIdx] = 2

    return matriz

def plotar(posicao, matriz):
    plt.imshow(matriz, 'gray')    
    plt.nipy_spectral()
    plt.plot(posicao[1], posicao[0], 'ro')
    plt.show(block=False)
    plt.pause(0.4)
    plt.clf()

def limpa(posicao, matriz):
    matriz[posicao] = 0

def mover(posicao, acao):
    x, y = posicao
    if acao == 'acima':
        return (x - 1, y)
    elif acao == 'abaixo':
        return (x + 1, y)
    elif acao == 'esquerda':
        return (x, y - 1)
    elif acao == 'direita':
        return (x, y + 1)
    return posicao

def iniciar(matriz, posicaoInicial):
    posicao = posicaoInicial
    voltar = False
    plt.ion()

    while True:
        agente = Agente(posicao)
        percepcao = agente.perceber(matriz)
        acao = agenteReativoSimples(percepcao, voltar)

        plotar(posicao, matriz)

        if acao == 'aspirar':
            limpa(posicao, matriz)
        else:
            novaPosicao = mover(posicao, acao)

            if matriz[novaPosicao] != 1:
                posicao = novaPosicao

        if posicao == (4, 1) and not voltar:
            voltar = True
        elif posicao == (1, 1) and voltar:
            voltar = False

if __name__ == '__main__':
    altura, largura = 6, 6
    incidencia = 0.3
    matriz = gerarMatriz(altura, largura, incidencia)
    posicaoInicial = (1, 1)
    iniciar(matriz, posicaoInicial)