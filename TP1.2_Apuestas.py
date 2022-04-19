import numpy as np
import matplotlib.pyplot as plt
import os

class Constant:
    NROTIRADAS = 10000
    MUESTRAS = 100
    APUESTAINICIAL = 1

colores = ["red", "green", "yellow", "blue", "purple", "cyan"]

def main():
    while True:
        os.system('cls')
        op1 = menu()
        if(op1 == 0):
            break
        os.system('cls')
        op2 = menu2()
        if(op1 == 1):
            if(op2 == 1):
                Martingala()
            elif(op2 == 2):
                dineroTotal = int(input('ingrese el capital con el que quiere iniciar: '))
                Martingala(dineroTotal)
        elif op1 == 2:
            if(op2 == 1):
                Fibonacci()
            elif(op2 == 2):
                dineroTotal = int(input('ingrese el capital con el que quiere iniciar: '))
                Fibonacci(dineroTotal)
        elif op1 == 3:
            if(op2 == 1):
                DAlembert()
            elif(op2 == 2):
                dineroTotal = int(input('ingrese el capital con el que quiere iniciar: '))
                DAlembert(dineroTotal)
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

def Martingala(dineroTotal = None):
    fig, axs = plt.subplots(1,2)
    fig.suptitle("Martingala")
    Apuestas = [[] for j in range(Constant.MUESTRAS + 1)]
    Frecuencia = [[] for j in range(Constant.MUESTRAS + 1)]
    for j in range(Constant.MUESTRAS):
        if(dineroTotal == None):
            capital = 0
        else:
            capital = dineroTotal
        ejex = []
        ganadas = 0
        valorApuesta = Constant.APUESTAINICIAL
        for i in range(Constant.NROTIRADAS):
            ejex.append(i+1)
            apuesta = np.random.randint(0,1)
            tirada = np.random.randint(0,37)
            if(calculaResultado(apuesta, tirada)):
                capital += valorApuesta
                valorApuesta = Constant.APUESTAINICIAL
                ganadas += 1
            else:
                capital -= valorApuesta
                valorApuesta = valorApuesta*2
            Apuestas[j].append(capital)
            Frecuencia[j].append(ganadas/(i+1))
            if(dineroTotal != None):
                if(capital == 0):
                    break
                elif(capital < valorApuesta):
                    valorApuesta = capital
        axs[0].plot(ejex, Frecuencia[j], colores[j%6], alpha = 0.75, linewidth = 0.5)
        axs[1].plot(ejex, Apuestas[j], colores[j%6], alpha = 0.75, linewidth = 0.5)
    Promedio(Apuestas, Frecuencia, axs)

def Fibonacci(dineroTotal = None):
    fig, axs = plt.subplots(1,2)
    fig.suptitle("Fibonacci")
    Apuestas = [[] for j in range(Constant.MUESTRAS + 1)]
    Frecuencia = [[] for j in range(Constant.MUESTRAS + 1)]
    for j in range(Constant.MUESTRAS):
        if(dineroTotal == None):
            capital = 0
        else:
            capital = dineroTotal
        ejex = []
        valorApuesta = Constant.APUESTAINICIAL
        fibo = 1
        ganadas = 0
        for i in range(Constant.NROTIRADAS):
            ejex.append(i+1)
            apuesta = np.random.randint(0,1)
            tirada = np.random.randint(0,37)
            if(calculaResultado(apuesta, tirada)):
                capital += valorApuesta
                if(fibo < 3):
                    fibo = 1
                else:
                    fibo -= 2
                ganadas += 1
            else:
                capital -= valorApuesta
                fibo += 1
            valorApuesta = Constant.APUESTAINICIAL*fib(fibo)
            Apuestas[j].append(capital)
            Frecuencia[j].append(ganadas/(i+1))
            if(dineroTotal != None):
                if(capital == 0):
                    break
                elif(capital < valorApuesta):
                    valorApuesta = capital
        axs[0].plot(ejex, Frecuencia[j], colores[j%6], alpha = 0.75, linewidth = 0.75)
        axs[1].plot(ejex, Apuestas[j], colores[j%6], alpha = 0.75, linewidth = 0.75)
    Promedio(Apuestas, Frecuencia, axs)
        

def DAlembert(dineroTotal = None):
    fig, axs = plt.subplots(1,2)
    fig.suptitle("D'Alembert")
    Apuestas = [[] for j in range(Constant.MUESTRAS + 1)]
    Frecuencia = [[] for j in range(Constant.MUESTRAS + 1)]
    for j in range(Constant.MUESTRAS):
        if(dineroTotal == None):
            capital = 0
        else:
            capital = dineroTotal
        ejex = []
        valorApuesta = Constant.APUESTAINICIAL
        ganadas = 0
        for i in range(Constant.NROTIRADAS):
            ejex.append(i+1)
            apuesta = np.random.randint(0,1)
            tirada = np.random.randint(0,37)
            if(calculaResultado(apuesta, tirada)):
                capital += valorApuesta
                if(valorApuesta <= Constant.APUESTAINICIAL):
                    valorApuesta = Constant.APUESTAINICIAL
                else:
                    valorApuesta -= Constant.APUESTAINICIAL
                ganadas += 1
            else:
                capital -= valorApuesta
                valorApuesta += Constant.APUESTAINICIAL
            Apuestas[j].append(capital)
            Frecuencia[j].append(ganadas/(i+1))
            if(dineroTotal != None):
                if(capital == 0):
                    break
                elif(capital < valorApuesta):
                    valorApuesta = capital
        axs[0].plot(ejex, Frecuencia[j], colores[j%6], alpha = 0.75, linewidth = 0.75)
        axs[1].plot(ejex, Apuestas[j], colores[j%6], alpha = 0.75, linewidth = 0.75)
    Promedio(Apuestas, Frecuencia, axs)

def Promedio(Apuestas, Frecuencia, axs):
    ejex =[]
    for i in range(Constant.NROTIRADAS):
        ejex.append(i+1)
        Frecuencia[Constant.MUESTRAS].append(np.mean([Frecuencia[j][i] if (len(Frecuencia[j]) > i) else (18/37) for j in range(Constant.MUESTRAS)]))
        Apuestas[Constant.MUESTRAS].append(np.mean([Apuestas[j][i] if (len(Apuestas[j]) > i) else 0 for j in range(Constant.MUESTRAS)]))
        if(i>100 and Apuestas[Constant.MUESTRAS][i] == 0):
            break
    axs[0].plot(ejex, Frecuencia[Constant.MUESTRAS], "black", label="Promedio", linewidth = 3)
    axs[0].legend(loc='upper right')
    axs[0].set_title('Frecuencia Relativa de Aciertos en N cantidad de tiradas')
    axs[0].set(xlabel='Cantidad de Tiradas', ylabel='Frecuencia Relativa')
    axs[1].plot(ejex, Apuestas[Constant.MUESTRAS], "black", label="Promedio", linewidth = 3)
    axs[1].legend(loc='upper right')
    axs[1].set_title('Capital Disponible en N cantidad de tiradas')
    axs[1].set(xlabel='Cantidad de Tiradas', ylabel='Capital Disponible')

def calculaResultado(apuesta, tirada):
    if(tirada == 0):
        return False
    else:
        return (apuesta == tirada%2)

def fib(n):
    if n < 2:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

main()
