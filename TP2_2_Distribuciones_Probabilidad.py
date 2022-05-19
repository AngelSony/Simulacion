import matplotlib.pyplot as plt
import math
import seaborn as sns
import os
import random as rn
import numpy as np

class Valores:
    CantMuestra = 100000
    Distribuciones = ["Uniforme", "Exponencial", "Gamma", "Normal", "Pascal", "Binomial", "Hipergeométrica", "Poisson", "Empiríca Discreta"]
    Uniforme = [[0,5],[1,10],[3,10]]
    Exponencial = [0.5,1,2]
    Gamma = [[1,2],[2,2],[5,1]]
    Normal = [[0,1],[-2,0.5],[1,0.2]]
    Pascal = [[8,0.5],[8,0.8],[2,0.8]]
    Binomial = [[20,0.5],[20,0.7],[50,0.5]]
    Hipergeometrica = [[200,60,50],[100,60,50],[100,60,30]]
    Poisson = [1,15,4]
    Empirica = [[.11, .12, .09, .08, .12, .1, .09, .09, .1, .1],[.1,.2,.3,.1,.11,.12,.07,.08,.11,.13],[.5,.6,.7,.8,.9,.4,.9,.8,.7]]

def Generar(opcion):
    data = [[],[],[]]
    print(Valores.Distribuciones[opcion-1])
    for j in range(3):
        if opcion == 1:
            for i in range(Valores.CantMuestra):
                data[j].append(uniform(Valores.Uniforme[j][0], Valores.Uniforme[j][1]))
        elif opcion == 2:
            for i in range(Valores.CantMuestra):
                data[j].append(exp(Valores.Exponencial[j]))
        elif opcion == 3:
            for i in range(Valores.CantMuestra):
                data[j].append(gamma(Valores.Gamma[j][0],Valores.Gamma[j][1]))
        elif opcion == 4:
            for i in range(Valores.CantMuestra):
                u, v = normal(Valores.Normal[j][0], Valores.Normal[j][1])
                data[j].append(u + v)
        elif opcion == 5:
            for i in range(Valores.CantMuestra):
                data[j].append(pascal(Valores.Pascal[j][0], Valores.Pascal[j][1]))
        elif opcion == 6:
            for i in range(Valores.CantMuestra):
                data[j].append(binomial(Valores.Binomial[j][0],Valores.Binomial[j][1]))
        elif opcion == 7:
            for i in range(Valores.CantMuestra):
                data[j].append(hypergeometric(Valores.Hipergeometrica[j][0],Valores.Hipergeometrica[j][1],Valores.Hipergeometrica[j][2]))
        elif opcion == 8:
            for i in range(Valores.CantMuestra):
                data[j].append(poisson(Valores.Poisson[j]))
        elif opcion == 9:
            for i in range(Valores.CantMuestra):
                data[j].append(empirical_discrete(Valores.Empirica[j]))

    return data

def Graficar(data, opcion):
    sns.set_style("white")
    if opcion in [5,6,7,8,9]:
        for j in range(3):
            discrete_plot(data[j])
    else:
        sns.displot(data, kde=False, legend=False)
    Leyenda = []
    for j in range(2,-1,-1):
        if opcion == 1:
            Leyenda.append('a = '+str(Valores.Uniforme[j][0])+', b = '+str(Valores.Uniforme[j][1]))
        if opcion == 2:
            Leyenda.append('α = '+str(Valores.Uniforme[j]))

    plt.legend(Leyenda)
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
        print(str(i+1) + ") - " + Valores.Distribuciones[i])
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

#Uniforme
def uniform(a,b):
    r = rn.random()
    return r*(b-a) + a

#Exponencial
def exp(alpha):
    r = rn.random()
    return -np.log(r)/alpha

#Gamma (Hace uso de lcg y clase Pascal)
def gamma(k, a):
    tr = 1.0
    for i in range(k):
        r = lcg()
        tr = tr * r
    x = -math.log(tr) / a
    return x

#Normal
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

class Pascal:
    m = 2**32
    a = 22695477
    c = 1
    x = 0

def lcg():
    Pascal.x = (Pascal.a * Pascal.x + Pascal.c) % Pascal.m 
    return (Pascal.x / Pascal.m)

#Pascal (Hace uso de lcg y clase Pascal)
def pascal(k,q):
    tr = 1.0
    qr = math.log(q)
    for i in range(k):
        r = lcg()
        tr = tr * r
    x = math.log(tr)/qr
    return x

def bernoulli(p):
    r = rn.random()
    if r < p:
        return 1
    else:
        return 0

#Binomial (Usa bernoulli)
def binomial(n, p):
    """n trials of a Bernoulli event"""
    x = 0
    for i in range(n):
        x += bernoulli(p)
    return x

#Hypergeométrica
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

#Poisson
def poisson(alpha):
    """Poisson process"""
    x = 0
    p = 1

    while p >= math.exp(-alpha):
        r = rn.random()
        p *= r
        x += 1

    return x

#Empírica Discreta
def empirical_discrete(fx):
    """ Discrete custom categorization"""
    cum = np.cumsum(fx)  # Cumulative distribution from density function
    r = rn.random()
    for i in range(len(cum)):
        if r < cum[i]:
            return i
        
main()