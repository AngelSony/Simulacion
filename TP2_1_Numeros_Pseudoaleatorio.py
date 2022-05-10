import numpy as np
import matplotlib.pyplot as plt
import os
import math
import random
import pandas as pd
import scipy.stats as ss

#https://support.minitab.com/es-mx/minitab/18/help-and-how-to/statistics/nonparametrics/how-to/runs-test/methods-and-formulas/methods-and-formulas/
#https://prezi.com/s5dlkuvrozou/prueba-de-corridas/?frame=dd00b164abe52ef88a7fd8f342c7ef1224f017e1

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
    print("Test de Corridas: ")
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
    print("Test arriba y abajo : ")
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
    print("Z <=" + str(z) )

def TestBondad(Values):
    print('TIRADAS: ', Constant.CANT_VALORES)
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
 
    print('INTERVALOS: ', intervalos)
    print('FRECUENCIA OBSERVADA: ', oi)
    print('FRECUENCIA ESPERADA: ', ei)
 
    grados_libertad = m-1
 
    chicuadrado(oi,ei,grados_libertad)
    kolmogorovSmirnov(Values)

def chicuadrado(oi,ei, grados_libertad):
    print('\n#### CHI CUADRADO ####')
 
 
    sumatoria = []
 
    for i in range(len(oi)):
        resultado = ((np.square(oi[i]-ei[i]))/ei[i])
        sumatoria.append(resultado)
 
    resultado_chi2=np.sum(sumatoria)
 
    print('RESULTADO DE CHI CUADRADO (z): ',resultado_chi2)
 
    tabla_chi2=ss.chi2.isf(0.05, grados_libertad)
 
    print('{0} < {1}'.format(resultado_chi2, tabla_chi2))
    if (resultado_chi2 < tabla_chi2):
        print('LOS NUMEROS SON INDEPENDIENTES.\n')
    else:
        print('LOS NUMEROS NO SON INDEPENDIENTES.\n')

def kolmogorovSmirnov(Values):
    print('\n#### KOLMOGOROV-SMIRNOV ####')
    media, desviacion = ss.norm.fit(Values)
 
    kstest = ss.kstest(Values,"norm",args=(media,desviacion))
 
    significacion = (1-kstest.pvalue/100)
    print('NIVEL DE SIGNIFICACION: ', significacion,'%')
 
    if kstest.pvalue < 0.01:
        print('LOS NUMEROS SON INDEPENDIENTES.\n')
    else:
        print('LOS NUMEROS NO SON INDEPENDIENTES.\n')

def Poker(Values):
    lista = []
    TD=0
    P1=0
    P2=0
    TP=0
    T=0
    P=0
    Q=0
 
    for i in Values:
        resultado = np.around(i,5)
        lista.append(resultado)
 
    for i in lista:
        numero=i
        decimal = str(numero-int(numero))[2:].zfill(5)
        
        A=None
        B=None
        C=None
        D=None
        E=None
        
        decimal_resultado = []
        counter = 0
        for j in decimal:
            counter = counter+1
            if counter <= 5:
                if (A!=None):
                    if(j==A):
                        decimal_resultado.append('A')
                        continue
                else:
                    A=j
                    decimal_resultado.append('A')
                    continue
                
                if (B!=None):
                    if(j==B):
                        decimal_resultado.append('B')
                        continue
                else:
                    B=j
                    decimal_resultado.append('B')
                    continue
 
                if (C!=None):
                    if(j==C):
                        decimal_resultado.append('C')
                        continue
                else:
                    C=j
                    decimal_resultado.append('C')
                    continue
 
                if (D!=None):
                    if(j==D):
                        decimal_resultado.append('D')
                        continue
                else:
                    D=j
                    decimal_resultado.append('D')
                    continue
 
                if (E!=None):
                    if(j==E):
                        decimal_resultado.append('E')
                        continue
                else:
                    E=j
                    decimal_resultado.append('E')
                    continue
        
        cant_A = 0
        cant_B = 0
        cant_C = 0
        cant_D = 0
        cant_E = 0
 
        for x in decimal_resultado:
            if(x=='A'):
                cant_A = cant_A+1
            elif(x=='B'):
                cant_B = cant_B+1
            elif(x=='C'):
                cant_C = cant_C+1
            elif(x=='D'):
                cant_D = cant_D+1
            elif(x=='E'):
                cant_E = cant_E+1
 
        frecuencia = [cant_A,cant_B,cant_C,cant_D,cant_E]        
 
        frecuencia.sort(reverse=True)
 
        
        if(frecuencia==[1,1,1,1,1]):
            #TODOS DISTINTOS
            TD = TD+1
        elif(frecuencia==[2,1,1,1,0]):
            #PAR
            P1 = P1+1
        elif(frecuencia==[2,2,1,0,0]):
            #2 PARES
            P2 = P2+1
        elif(frecuencia==[3,1,1,0,0]):
            #TERCIA
            T = T+1
        elif(frecuencia==[3,2,0,0,0]):
            #TERCIA Y PAR
            TP = TP+1
        elif(frecuencia==[4,1,0,0,0]):
            #POKER
            P = P+1
        elif(frecuencia==[5,0,0,0,0]):
            #QUINTINA
            Q = Q+1        
    
    probabilidades = [0.3025,0.504,0.108,0.009,0.072,0.0045,0.0001]
    ei=[]
 
    for i in probabilidades:
        resultado = i*100
        ei.append(np.round(resultado,2))
        
    oi = [TD,P1,P2,T,TP,P,Q]
    print('Ei: ', ei)
    print('Oi: ', oi)
 
    grados_libertad = int(input('Ingrese grados de libertad: '))
    chicuadrado(oi, ei, grados_libertad)

def Test(Values):
    TestCorridas(Values)
    TestArribaAbajo(Values)
    TestBondad(Values)
    Poker(Values)

main()
