import matplotlib.pyplot as plt
import math
import seaborn as sns
import os
import random as rn
import numpy as np


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

def bernoulli(p):
    r = rn.random()
    if r < p:
        return 1
    else:
        return 0

def binomial(n, p):
    """n trials of a Bernoulli event"""
    x = 0
    for i in range(n):
        x += bernoulli(p)
    return x

def hypergeometric(N,K,n):
    x = 0
    c = N - K
    k = K

    for i in range(n-1):
        r = rn.random()
        if r <= k/N:
            x += 1
            k -= 1
        else:
            c -= 1
        N -= 1

    return x

def poisson(alpha):
    """Poisson process"""
    x = 0
    p = 1

    while p >= math.exp(-alpha):
        r = rn.random()
        p *= r
        x += 1

    return x

def empirical_discrete(fx):
    """ Discrete custom categorization"""
    cum = np.cumsum(fx)  # Cumulative distribution from density function
    r = rn.random()
    for i in range(len(cum)):
        if r < cum[i]:
            return i

def Generar(opcion):
    data = []
    print(Dist[opcion-1])
    for i in range(100000):
        if opcion == 1:
            data.append(uniform(3,8))
        elif opcion == 2:
            data.append(exp(0.8))
        #elif opcion == 3:
            #Distribución Gamma
        elif opcion == 4:
            u, v = normal(0, 1)
            data.append(u + v)
        #elif opcion == 5:
            #Distribución Pascal
        elif opcion == 6:
            data.append(binomial(6,0.5))
        elif opcion == 7:
            data.append(hypergeometric(500,50,100))
        elif opcion == 8:
            data.append(poisson(7))
        elif opcion == 9:
            data.append(empirical_discrete([.11, .12, .09, .08, .12, .1, .09, .09, .1, .1]))

    return data

def Graficar(data, opcion):
    sns.set_style("white")
    if opcion in [6,7,8,9]:
        discrete_plot(data)
    else:
        sns.displot(data, kde=False)
    plt.show()

def main():
    while True:
        opcion = menu()
        os.system("cls")
        if(opcion != 0):
            data = Generar(opcion)
            Graficar(data, opcion)
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

def discrete_plot(data, alpha=.5):
    hist, edges = np.histogram(data,bins=np.arange(min(data),max(data)+2)-0.5)
    return plt.bar(edges[:-1], hist, align="edge", ec="k", alpha=alpha)
        
main()