import numpy as np
import matplotlib.pyplot as plt
import os
seed = ''
Seeds = []
Values = []
Eje_X = []
Seeds.clear
Values.clear
Eje_X.clear
def main():
    opcion = -1
    while opcion != 0:
        os.system("cls")
        print("Seleccione algoritmo:")
        print("1 - Parte media del cuadrado (Von Neuman)")
        print("2 - rand (MatLab - GCL)")
        print("3 - RANDU (GCL)")
        print("0 - Salir")
        opcion = input('Opcion: ')
        if   opcion == '1':
            print("Mid Square")
            os.system("cls")
            seed = input('Ingrese valor de la semilla: ')
            mid_square(seed,1000)
        elif opcion == '2':
            print("rand")
            max_rand_value = (2**31) - 1
            rand_argument = 7**5
            seed = np.random.randint(0,max_rand_value)
            rand(seed,1500,max_rand_value,rand_argument)
        elif opcion == '3':
            os.system("cls")
            print("RANDU")
            seed = input('Ingrese valor de la semilla: ')
            max_RANDU_value = (2**31)
            RANDU_argument = (2**16)+3
            RANDU(int(seed),1500,max_RANDU_value,RANDU_argument)
        elif opcion == '0':
            exit

def mid_square(seed,n):
    int_seed = int(seed)
    i = 0
    while i < n and int_seed != 0:
        int_value = int_seed**2
        str_value = str(int_value)
        len_value = len(str_value)
        while len_value < 8:
            str_value = '0' + str_value
            len_value += 1
        Seeds.append(int_seed)
        Values.append(str_value)
        next_seed = str_value[2:6]
        int_seed = int(next_seed)
        i += 1
        Eje_X.append(i+1)
    plt.figure("Mid square n-valor")
    plt.xlabel("N-ésimo valor generado")
    plt.ylabel("Valor generado")
    plt.plot(Eje_X, Values, '-o', linewidth = 1, color = 'blue', alpha=0.5)
    

    plt.figure("Mid square semilla-valor")
    plt.xlabel("Semilla")
    plt.ylabel("Valor generado por semilla")
    plt.plot(Seeds, Values, 'o', linewidth = 1, color = 'blue', alpha=0.5)
    
    plt.show()

def rand(seed,n,max_rand_value,rand_argument):
    Seeds.append(seed)
    Values.append(int(seed)/max_rand_value)
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
    y_sm, y_std = lowess(Eje_X, Values, f=1./5.)
    # plot it
    plt.plot(Eje_X, y_sm, color='withe', label='LOWESS')
    

    plt.figure("rand semilla-valor")
    plt.xlabel("Semilla")
    plt.ylabel("Valor generado por semilla")
    plt.plot(Seeds, Values, 'o', linewidth = 1, color = 'red', alpha=0.5)
    
    plt.show()

def RANDU(seed,n,max_RANDU_value,RANDU_argument):
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
    
    plt.figure("RANDU semilla-valor")
    plt.xlabel("Semilla")
    plt.ylabel("Valor generado por semilla")
    plt.plot(Seeds, Values, 'o', linewidth = 1, color = 'green', alpha=0.5)
    
    plt.show()

def lowess(x, y, f=1./3.):
    """
    Basic LOWESS smoother with uncertainty. 
    Note:
        - Not robust (so no iteration) and
             only normally distributed errors. 
        - No higher order polynomials d=1 
            so linear smoother.
    """
    # get some paras
    xwidth = f*1500 #f*(x.max()-x.min()) # effective width after reduction factor
    N = len(x) # number of obs
    # Don't assume the data is sorted
    order = np.argsort(x)
    # storage
    y_sm = np.zeros_like(y)
    y_stderr = np.zeros_like(y)
    # define the weigthing function -- clipping too!
    tricube = lambda d : np.clip((1- np.abs(d)**3)**3, 0, 1)
    # run the regression for each observation i
    for i in range(N):
        dist = np.abs((x[order][i]-x[order]))/xwidth
        w = tricube(dist)
        # form linear system with the weights
        A = np.stack([w, x[order]*w]).T
        b = w * y[order]
        ATA = A.T.dot(A)
        ATb = A.T.dot(b)
        # solve the syste
        sol = np.linalg.solve(ATA, ATb)
        # predict for the observation only
        yest = A[i].dot(sol)# equiv of A.dot(yest) just for k
        place = order[i]
        y_sm[place]=yest 
        sigma2 = (np.sum((A.dot(sol) -y [order])**2)/N )
        # Calculate the standard error
        y_stderr[place] = np.sqrt(sigma2 * A[i].dot(np.linalg.inv(ATA)).dot(A[i]))
    return y_sm, y_stderr

main()
