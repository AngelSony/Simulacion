import numpy as np
import matplotlib.pyplot as plt

class Constant:
    NROTIRADAS = 10000
    MUESTRAS = 5
    APUESTAINICIAL = 1

colores = ["red", "green", "yellow", "blue", "purple", "black"]
ejex = [(i+1) for i in range(Constant.NROTIRADAS)]
Martingala = [[] for j in range(Constant.MUESTRAS)]
Fibonacci = [[] for j in range(Constant.MUESTRAS)]
DAlembert = [[] for j in range(Constant.MUESTRAS)]

def main():
    for j in range(Constant.MUESTRAS):
        cargaMartingala(j)
    graficar(Martingala)

def cargaMartingala(j):
    perdidas = 0
    capital = 0
    
    for i in range(Constant.NROTIRADAS):
        apuesta = np.random.randint(0,1)
        tirada = np.random.randint(0,36)
        if(calculaResultado):
            capital += Constant.APUESTAINICIAL*(2^(perdidas))
            perdidas = 0
        else:
            capital -= Constant.APUESTAINICIAL*(2^(perdidas))
            perdidas += 1
        Martingala[j].append(capital)

def calculaResultado(apuesta, tirada):
    if(tirada == 0):
        return false
    else:
        return (apuesta == tirada%2)

def graficar(list):
    fig = plt.subplot()
    fig.suptitle("Martingala")
    for j in range(Constant.MUESTRAS):
        
main()