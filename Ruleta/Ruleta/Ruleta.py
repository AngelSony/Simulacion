import numpy as np
import matplotlib.pyplot as plt

colores = ["red", "green", "yellow", "blue", "purple", "black"]
muestras, nroTiradas = 5, 999
ejex = [(i+1) for i in range(nroTiradas)]
fig, axs = plt.subplots(2,2)
tiradas = [[] for j in range(muestras)]
fRelativa = [[] for j in range(muestras + 1)]
promedio = [[] for j in range(muestras + 1)]
desvio = [[] for j in range(muestras + 1)]
varianza = [[] for j in range(muestras + 1)]

def main():
    fig.suptitle("Gráfica de Muestras")
    for j in range(muestras):
        graficar(j)
    cargaPromedios()
    plt.show()

def graficar(j):
    sum = 0
    for i in range (nroTiradas):
        tiradas[j].append(np.random.randint(0,36))
        if(tiradas[j][i] == 12):
            sum += 1
        fRelativa[j].append((sum/(i+1)))
        promedio[j].append(np.mean(tiradas[j]))
        desvio[j].append(np.std(tiradas[j]))
        varianza[j].append(np.var(tiradas[j]))
    axs[0,1].plot(ejex, promedio[j], colores[j])
    axs[0,0].plot(ejex, fRelativa[j], colores[j])
    axs[1,0].plot(ejex, desvio[j], colores[j])
    axs[1,1].plot(ejex, varianza[j], colores[j])
    estilos(axs)
    
def cargaPromedios():
    fig, axs = plt.subplots(2,2)
    fig.suptitle("Promedio de Muestras")
    for i in range(nroTiradas):
        fRelativa[muestras].append(np.mean([fRelativa[j][i] for j in range(muestras)]))
        promedio[muestras].append(np.mean([promedio[j][i] for j in range(muestras)]))
        desvio[muestras].append(np.mean([desvio[j][i] for j in range(muestras)]))
        varianza[muestras].append(np.mean([varianza[j][i] for j in range(muestras)]))
    axs[0,1].plot(ejex, promedio[muestras], colores[5])
    axs[0,0].plot(ejex, fRelativa[muestras], colores[5])
    axs[1,0].plot(ejex, desvio[muestras], colores[5])
    axs[1,1].plot(ejex, varianza[muestras], colores[5])
    estilos(axs)
    

def estilos(axs):
    axs[0,1].set_title('Promedio')
    axs[0,1].set_ylim([0,36])
    axs[0,1].set(xlabel='n', ylabel='vp')
    axs[0,0].set_title('Frecuencia Relativa')
    axs[0,0].set_ylim([0,0.1])
    axs[0,0].set(xlabel='n', ylabel='fr')
    axs[1,0].set_title('Desvío Estandar')
    axs[1,0].set_ylim([0,20])
    axs[1,0].set(xlabel='n', ylabel='vd')
    axs[1,1].set_title('Varianza')
    axs[1,1].set_ylim([0,200])
    axs[1,1].set(xlabel='n', ylabel='vv')


main()