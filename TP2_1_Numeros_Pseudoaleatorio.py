import numpy as np
import matplotlib.pyplot as plt
import os
import math
import random
import pandas as pd
import scipy.stats as ss

class Constant:
    CANT_VALORES = 10000

def main():
    while True:
        opcion = menu()
        os.system("cls")
        if opcion == 1:
            print("Mid Square")
            seed = int(input('Ingrese valor de la semilla: '))
            mid_square(seed,Constant.CANT_VALORES)
        elif opcion == 2:
            print("rand")
            max_rand_value = (2**31) - 1
            rand_argument = 7**5
            seed = np.random.randint(0,max_rand_value)
            rand(seed,Constant.CANT_VALORES,max_rand_value,rand_argument)
        elif opcion == 3:
            print("RANDU")
            seed = int(input('Ingrese valor de la semilla: '))
            max_RANDU_value = (2**31)
            RANDU_argument = (2**16)+3
            RANDU(seed,Constant.CANT_VALORES,max_RANDU_value,RANDU_argument)
        elif opcion == 4:
            print("Python")
            Python(Constant.CANT_VALORES)
        elif opcion == 0:
            break

def menu():
    os.system("cls")
    print("Seleccione algoritmo:")
    print("1 - Parte media del cuadrado (Von Neuman)")
    print("2 - rand (MatLab - GCL)")
    print("3 - RANDU (GCL)")
    print("4 - Python")
    print("0 - Salir")
    while True:
        op = int(input("Opción:  "))
        if op < 0 or op > 4:
            print("Debe ingresar un número comprendido entre 0 y 4")
        else:
            break
    return op

def mid_square(seed,n):
    Seeds = []
    Values = []
    Eje_X = []
    i = 0
    while i < n and seed != 0:
        int_value = seed**2
        str_value = str(int_value)
        len_value = len(str_value)
        while len_value < 8:
            str_value = '0' + str_value
            len_value += 1
        Seeds.append(seed)
        Values.append(int_value)
        next_seed = str_value[2:6]
        seed = int(next_seed)
        i += 1
        Eje_X.append(i+1)
    plt.figure("Mid square n-valor")
    plt.xlabel("N-ésimo valor generado")
    plt.ylabel("Valor generado")
    plt.plot(Eje_X, Values, '-o', linewidth = 1, color = 'blue', alpha=0.5)
    y_sm, y_std = lowess(np.array(Eje_X), np.array(Values), f=1./5.)
    plt.plot(Eje_X, y_sm, color='white', label='LOWESS', linewidth = 1.5)
    Test(Values)
    plt.show()

def rand(seed,n,max_rand_value,rand_argument):
    Seeds = []
    Values = []
    Eje_X = []
    Seeds.append(seed)
    Values.append(seed/max_rand_value)
    Eje_X.append(1)
    i= 1
    while i < n:
        Seeds.append((rand_argument * Seeds[i-1]) % max_rand_value)
        Values.append(Seeds[i]/max_rand_value)
        Eje_X.append(i+1)
        i += 1
    plt.figure("rand n-valor")
    plt.xlabel("N-ésimo valor generado")
    plt.ylabel("Valor generado")
    plt.plot(Eje_X, Values, 'o', linewidth = 1, color = 'red', alpha=0.5)
    y_sm, y_std = lowess(np.array(Eje_X), np.array(Values), f=1./5.)
    plt.plot(Eje_X, y_sm, color='white', label='LOWESS', linewidth = 1.5)
    Test(Values)
    plt.show()

def RANDU(seed,n,max_RANDU_value,RANDU_argument):
    Seeds = []
    Values = []
    Eje_X = []
    Seeds.append(seed)
    Values.append(seed/max_RANDU_value)
    Eje_X.append(1)
    i= 1
    while i < n:
        Seeds.append((RANDU_argument * Seeds[i-1]) % max_RANDU_value)
        Values.append(Seeds[i]/max_RANDU_value)
        Eje_X.append(i+1)
        i += 1
    plt.figure("RANDU n-valor")
    plt.xlabel("N-ésimo valor generado")
    plt.ylabel("Valor generado")
    plt.plot(Eje_X, Values, 'o', linewidth = 1, color = 'green', alpha=0.5)
    y_sm, y_std = lowess(np.array(Eje_X), np.array(Values), f=1./5.)
    plt.plot(Eje_X, y_sm, color='white', label='LOWESS', linewidth = 1.5)
    Test(Values)
    plt.show()

def Python(n):
    Values = []
    Eje_X = []
    i= 1
    while i < n:
        Values.append(random.random())
        i += 1
        Eje_X.append(i)
    plt.figure("Pyhton n-valor")
    plt.xlabel("N-ésimo valor generado")
    plt.ylabel("Valor generado")
    plt.plot(Eje_X, Values, 'o', linewidth = 1, color = 'green', alpha=0.5)
    y_sm, y_std = lowess(np.array(Eje_X), np.array(Values), f=1./5.)
    plt.plot(Eje_X, y_sm, color='white', label='LOWESS', linewidth = 1.5)
    Test(Values)
    plt.show()
        



def lowess(x, y, f=1./3.):
    xwidth = f*(x.max()-x.min())
    N = len(x)
    order = np.argsort(x)
    y_sm = np.zeros_like(y)
    y_stderr = np.zeros_like(y)
    tricube = lambda d : np.clip((1- np.abs(d)**3)**3, 0, 1)
    for i in range(N):
        dist = np.abs((x[order][i]-x[order]))/xwidth
        w = tricube(dist)
        A = np.stack([w, x[order]*w]).T
        b = w * y[order]
        ATA = A.T.dot(A)
        ATb = A.T.dot(b)
        sol = np.linalg.solve(ATA, ATb)
        yest = A[i].dot(sol)
        place = order[i]
        y_sm[place]=yest 
        sigma2 = (np.sum((A.dot(sol) -y [order])**2)/N )
        y_stderr[place] = np.sqrt(sigma2 * A[i].dot(np.linalg.inv(ATA)).dot(A[i]))
    return y_sm, y_stderr

def TestCorridas(Values):
    print("\nTest de Corridas Sube/Baja: ")
    x = []
    a = 1
    for i in range(len(Values)-1):
        if Values[i+1] >= Values[i]:
            x.append("+")
        elif(Values[i+1] <Values[i]):
            x.append("-")

    for i in range(1, len(x)):
        if (x[i] != x[i-1]):
            a += 1
    n = len(x)
    media = (2*n-1)/3
    desviacion = math.sqrt((16*n-29)/90)
    z = (a-media)/desviacion
    print("Z <= "+ str(z))        

def TestArribaAbajo(Values):
    print("\nTest de Corrida Arriba/Abajo: ")
    x = []
    corridas = 1
    contmas = 0
    contmenos = 0
    u=[]
    
    for i in range(len(Values)-1):
        u.append(float(Values[i]))
    med=np.mean(u)

    for i in range(len(u)):
        if u[i] >= med:
            x.append("+")
        elif(u[i] < med):
            x.append("-")

    for i in range(1, len(x)):
        if (x[i] != x[i-1]):
            corridas += 1

    if  (x[0]=="+"):
        contmas+=1
    else:
        contmenos+=1
    for i in range(1,len(x)):
        if(x[i] == "+"):
            contmas += 1
        else:
            contmenos += 1

    n = contmas+contmenos
    media = ((2*contmenos*contmas)/(contmas+contmenos))+1
    desviacion = math.sqrt(((2*contmenos*contmas*(2*contmas*contmenos-n))/((n**2)*(n-1))))
    z = (corridas-media)/desviacion
    print("Z <= " + str(z) )

def TestBondad(Values):
    m=int(np.sqrt(Constant.CANT_VALORES))
    print('M: ',m)
    
    intervalos=[]
 
    for i in range(m+1):
        intervalo=i/m
        intervalos.append(intervalo)
 
    division = pd.cut(Values, bins=intervalos)
    
    oi = division.value_counts().reindex().tolist()
    ei = []
 
    for i in range(len(oi)):
        resultado = int(Constant.CANT_VALORES/m)
        ei.append(resultado)

    grados_libertad = m-1
 
    chicuadrado(oi,ei,grados_libertad)
    kolmogorovSmirnov(Values)

def chicuadrado(oi,ei, grados_libertad):
    print('\nTest de Bondad Chi Cuadrado: ')
    sumatoria = []
 
    for i in range(len(oi)):
        resultado = ((np.square(oi[i]-ei[i]))/ei[i])
        sumatoria.append(resultado)
 
    resultado_chi2=np.sum(sumatoria)
 
    print('Z <= ',resultado_chi2)
 
    tabla_chi2=ss.chi2.isf(0.05, grados_libertad)
 
    print('{0} < {1}'.format(resultado_chi2, tabla_chi2))
    if (resultado_chi2 < tabla_chi2):
        print('Los números son independientes.\n')
    else:
        print('Los números No son independientes.\n')

def kolmogorovSmirnov(Values):
    print('\nTest de Bondad Kolmogorov-Smirnov: ')
    media, desviacion = ss.norm.fit(Values)
 
    kstest = ss.kstest(Values,"norm",args=(media,desviacion))
 
    significacion = (1-kstest.pvalue/100)
    print('Nivel de Significación: ', significacion,'%')
 
    if kstest.pvalue < 0.01:
        print('LOS NUMEROS SON INDEPENDIENTES.\n')
    else:
        print('LOS NUMEROS NO SON INDEPENDIENTES.\n')

def Test(Values):
    TestCorridas(Values)
    TestArribaAbajo(Values)
    TestBondad(Values)

main()
