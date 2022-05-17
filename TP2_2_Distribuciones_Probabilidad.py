import matplotlib.pyplot as plt
import math
import seaborn as sns
import os
import random as rn
import numpy as np

sns.set_style("white")
Dist = ["Uniforme", "Exponencial", "Gamma", "Normal", "Pascal", "Binomial", "Hipergeométrica", "Poisson", "Empiríca Discreta"]

def uniform(a, b):
    r = rn.random()
    return r*(b-a) + a

def exp(alpha):
    r = rn.random()
    return -np.log(r)/alpha

def normal(mu, sigma):
    """Box-Muller method"""
    s = 0
    while s == 0 or s >= 1:
        u = uniform(-1, 1)
        v = uniform(-1, 1)
        s = u ** 2 + v ** 2

    k = math.sqrt(np.log(s) * (-2) / s)
    z1 = u * k * sigma + mu
    z2 = v * k * sigma + mu
    return z1, z2

def Generar(opcion):
    data = []
    print(Dist[opcion-1])
    for i in range(10000):
        if opcion == 1:
            data.append(uniform(3,8))
        elif opcion == 2:
            data.append(exp(0.8))
        #elif opcion == 3:
            #Distribución Gamma
        elif opcion == 4:
            u, v = normal(0, 1)
            data.append(u + v)
    return data

def Graficar(data):
    sns.displot(data, kde=False)
    plt.show()

def main():
    while True:
        opcion = menu()
        os.system("cls")
        if(opcion != 0):
            data = Generar(opcion)
            Graficar(data)
        else:
            break

def menu():
    os.system("cls")
    print("Seleccione distribución:")
    for i in range(9):
        print(str(i+1) + ") - " + Dist[i])
    while True:
        op = int(input("Opción:  "))
        if op < 0 or op > 9:
            print("Debe ingresar un número comprendido entre 0 y 9")
        else:
            break
    return op
        
main()