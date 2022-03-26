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
        cargaFibonacci(j)
        cargaDAlembert(j)
    graficar(Martingala, "Martingala")
    graficar(Fibonacci, "Fibonacci")
    graficar(DAlembert, "D'Alembert")
    plt.show()

def cargaMartingala(j):
    capital = 0
    perdidas = 0
    for i in range(Constant.NROTIRADAS):
        apuesta = np.random.randint(0,1)
        tirada = np.random.randint(0,36)
        if(calculaResultado(apuesta, tirada)):
            capital += Constant.APUESTAINICIAL*(2**perdidas)
            perdidas = 0
        else:
            capital -= Constant.APUESTAINICIAL*(2**perdidas)
            perdidas += 1
        Martingala[j].append(capital)

def cargaFibonacci(j):
    capital = 0
    fibo = 1
    for i in range(Constant.NROTIRADAS):
        apuesta = np.random.randint(0,1)
        tirada = np.random.randint(0,36)
        if(calculaResultado(apuesta, tirada)):
            capital += Constant.APUESTAINICIAL*(fib(fibo))
            if(fibo < 3):
                fibo = 1
            else:
                fibo -= 2
        else:
            capital -= Constant.APUESTAINICIAL*(fib(fibo))
            fibo += 1
        Fibonacci[j].append(capital)

def cargaDAlembert(j):
    capital = 0
    valorApuesta = Constant.APUESTAINICIAL
    for i in range(Constant.NROTIRADAS):
        apuesta = np.random.randint(0,1)
        tirada = np.random.randint(0,36)
        if(calculaResultado(apuesta, tirada)):
            capital += valorApuesta
            if(valorApuesta > Constant.APUESTAINICIAL):
                valorApuesta -= Constant.APUESTAINICIAL
        else:
            capital -= valorApuesta
            valorApuesta += Constant.APUESTAINICIAL
        DAlembert[j].append(capital)

def calculaResultado(apuesta, tirada):
    if(tirada == 0):
        return False
    else:
        return (apuesta == tirada%2)

def graficar(list, name):
    fig, axs = plt.subplots(1,2)
    fig.suptitle(name)
    for j in range(Constant.MUESTRAS):
        axs[1].plot(ejex, list[j], colores[j])

def fib(n):
    if n < 2:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

main()