import numpy as np
import matplotlib.pyplot as plt
import os

class Constant:
    NROTIRADAS = 10000
    MUESTRAS = 5
    APUESTAINICIAL = 1

colores = ["red", "green", "yellow", "blue", "purple", "black"]
ejex = [(i+1) for i in range(Constant.NROTIRADAS)]
MartingalaInf = [[] for j in range(Constant.MUESTRAS)]
FibonacciInf = [[] for j in range(Constant.MUESTRAS)]
DAlembertInf = [[] for j in range(Constant.MUESTRAS)]
MartingalaFin = [[] for j in range(Constant.MUESTRAS)]
FibonacciFin = [[] for j in range(Constant.MUESTRAS)]
DAlembertFin = [[] for j in range(Constant.MUESTRAS)]

def main():
    op1 = menu()
    op2 = menu2()
    if op1 == 1 and op2==1:
        for j in range(Constant.MUESTRAS):
            cargaMartingalaInf(j)
        graficar(MartingalaInf, "Martingala")
    elif op1 == 2 and op2==1:
        for j in range(Constant.MUESTRAS):
            cargaFibonacciInf(j)
        graficar(FibonacciInf, "Fibonacci")
    elif op1 == 3 and op2 == 1:
        for j in range(Constant.MUESTRAS):
            cargaDAlembertInf(j)
        graficar(DAlembertInf, "D'Alembert")
    elif op1 == 1 and op2==2:
        capital = int(input('ingrese el capital con el que quiere iniciar: '))
        for j in range(Constant.MUESTRAS):
            cargaMartingalaFin(j, capital)
        graficar(MartingalaFin, "Martingala")
    plt.show()

def menu2():
    os.system('cls')
    print("***SELECCIONA UN TIPO DE CAPITAL PARA LA SIMULACION***")
    print("1 - Capital infinito")
    print("2 - Capital acotado")
    print("0 - Salir")
    while True:
        op = int(input("Ingrese su opción:  "))
        if op < 0 or op > 2:
            print("Debes ingresar un número comprendido entre 0 y 3")
        else:
            break
    return op

def menu():
    os.system('cls')
    print("*** MENU DE OPCIONES ***")
    print("Selecciona una opción")
    print("1 - Martingala")
    print("2 - Fibonacci")
    print("3 - D'Alambert")
    print("0 - Salir")
    while True:
        op = int(input("Ingrese su opción:  "))
        if op < 0 or op > 3:
            print("Debes ingresar un número comprendido entre 0 y 3")
        else:
            break
    return op
def cargaMartingalaInf(j):
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
        MartingalaInf[j].append(capital)
def cargaMartingalaFin(j, cap):
    perdidas=0
    for i in range(Constant.NROTIRADAS):
        apuesta = np.random.randint(0, 1)
        tirada = np.random.randint(0, 36)
        if (cap >= Constant.APUESTAINICIAL):

            if (calculaResultado(apuesta, tirada)):
                cap += Constant.APUESTAINICIAL * (2 ** perdidas)
                perdidas = 0
            else:
                cap -= Constant.APUESTAINICIAL * (2 ** perdidas)
                perdidas += 1
        else:
            if (calculaResultado(apuesta, tirada)):
                cap += cap
                perdidas = 0
            else:
                cap -= cap
                perdidas += 1
                break
        MartingalaFin[j].append(cap)


def cargaFibonacciInf(j):
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
        FibonacciInf[j].append(capital)

def cargaDAlembertInf(j):
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
        DAlembertInf[j].append(capital)

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