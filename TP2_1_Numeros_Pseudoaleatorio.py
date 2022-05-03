import numpy as np
import matplotlib.pyplot as plt
import os

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
        elif opcion == 0:
            break

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

    plt.figure("Mid square semilla-valor")
    plt.xlabel("Semilla")
    plt.ylabel("Valor generado por semilla")
    plt.plot(Seeds, Values, 'o', linewidth = 1, color = 'blue', alpha=0.5)
    
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
    

    plt.figure("rand semilla-valor")
    plt.xlabel("Semilla")
    plt.ylabel("Valor generado por semilla")
    plt.plot(Seeds, Values, 'o', linewidth = 1, color = 'red', alpha=0.5)
    
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
    
    plt.figure("RANDU semilla-valor")
    plt.xlabel("Semilla")
    plt.ylabel("Valor generado por semilla")
    plt.plot(Seeds, Values, 'o', linewidth = 1, color = 'green', alpha=0.5)
    
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

def menu():
    os.system("cls")
    print("Seleccione algoritmo:")
    print("1 - Parte media del cuadrado (Von Neuman)")
    print("2 - rand (MatLab - GCL)")
    print("3 - RANDU (GCL)")
    print("0 - Salir")
    while True:
        op = int(input("Opción:  "))
        if op < 0 or op > 3:
            print("Debe ingresar un número comprendido entre 0 y 3")
        else:
            break
    return op

main()
