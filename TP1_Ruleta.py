import numpy as np
import matplotlib.pyplot as plt

colores = ["r-", "g-", "y-", "b-", "c-", "k:"]
Participantes =["Hernan","Bruno","Angel","Maxi","Ova"]
muestras, nroTiradas = 5, 9999
ejex = [(i+1) for i in range(nroTiradas)]
fig, axs = plt.subplots(2,2)
tiradas = [[] for j in range(muestras)]
fRelativa = [[] for j in range(muestras + 1)]
promedio = [[] for j in range(muestras + 1)]
desvio = [[] for j in range(muestras + 1)]
varianza = [[] for j in range(muestras + 1)]

def main():
    for j in range(muestras):
        Graficar(j)
    Promedios()
    plt.show()

def Graficar(j):
    fig.suptitle("10.000 tiradas de ruleta para 5 jugadores en simultaneo")
    sum = 0
    accum = 0
    global PromedioReal
    global DesvioFinal
    global VarianzaFinal
    global DesFinal
    global VarFinal
    DesvioFinal  = np.arange(1, nroTiradas+1)
    VarianzaFinal = np.arange(1, nroTiradas+1)
    DesFinal = 0
    VarFinal = 0
    
    for i in range (nroTiradas):
        tiradas[j].append(np.random.randint(0,37))
        accum += tiradas[j][i]
        if(tiradas[j][i] == 12): #El programa está determinado para estudiar la aparicion del numero 12
            sum += 1
        fRelativa[j].append((sum/(i+1)))
        promedio[j].append(accum/(i+1))
        if (i == 9998):
            DesFinal =  np.std(tiradas[j])
            desvio[j].append(DesFinal)
            VarFinal = np.square(desvio[j][i])
            varianza[j].append(np.square(desvio[j][i]))
        else:
            desvio[j].append(np.std(tiradas[j]))
            varianza[j].append(np.square(desvio[j][i]))
            
    PromedioReal = np.ones(nroTiradas) * ((36 - 0) / 2) #(ValorMaximo - ValorMinimo) / 2
    VarianzaFinal = np.ones(nroTiradas) * VarFinal
    DesvioFinal =  np.ones(nroTiradas) * DesFinal
    axs[0,0].plot(ejex, fRelativa[j], colores[j], label = Participantes[j])
    axs[0,1].plot(ejex, promedio[j], colores[j], label = Participantes[j])
    axs[1,0].plot(ejex, desvio[j], colores[j], label = Participantes[j])
    axs[1,1].plot(ejex, varianza[j], colores[j], label = Participantes[j])
    AplicarEstilo(axs)

def Promedios():
    fig, axs = plt.subplots(2,2)
    fig.suptitle("Promedio de las 5 muestras de 10.000 tiradas")
    for i in range(nroTiradas):
        fRelativa[muestras].append(np.mean([fRelativa[j][i] for j in range(muestras)]))
        promedio[muestras].append(np.mean([promedio[j][i] for j in range(muestras)]))
        desvio[muestras].append(np.mean([desvio[j][i] for j in range(muestras)]))
        varianza[muestras].append(np.mean([varianza[j][i] for j in range(muestras)]))
    axs[0,0].plot(ejex, fRelativa[muestras], colores[5], label="Frecuencia de aciertos promedio de los 5 jugadores")
    axs[0,1].plot(ejex, promedio[muestras], colores[5], label="Promedio de los valores promedio de los 5 jugadores en la n-ésima jugada")
    axs[0,1].plot(ejex, PromedioReal, colores[0], label="Promedio Real / Esperado: "+str((36 - 0) / 2))
    axs[1,0].plot(ejex, desvio[muestras], colores[5], label="Desvio promedio de los 5 jugadores en la n-ésima jugada")
    axs[1,0].plot(ejex, DesvioFinal, colores[0], label="Desvio Real / Esperado: "+str(round(DesFinal,2)))
    axs[1,1].plot(ejex, varianza[muestras], colores[5], label="Varianza promedio de los 5 jugadores en la n-ésima jugada")
    axs[1,1].plot(ejex, VarianzaFinal, colores[0], label="Varianza Real / Esperado: "+str(round(VarFinal,2)))
    AplicarEstiloPromedio(axs)

def AplicarEstilo(axs):
    axs[0,0].set_title('Frecuencia Relativa de aciertos en N Cantidad de Tiradas')
    axs[0,0].set_ylim([0,0.1])
    axs[0,0].set(xlabel='Cantidad de Tiradas', ylabel='Frecuencia Relativa')
    axs[0,0].legend(loc='upper right')
    
    axs[0,1].set_title('Valor Promedio de Jugadas de Ruleta en N Cantidad de Tiradas')
    axs[0,1].set_ylim([0,36])
    axs[0,1].set(xlabel='Cantidad de Tiradas', ylabel='Valor Promedio')
    axs[0,1].legend(loc='upper right')
   
    axs[1,0].set_title('Desvío Estandar para N Cantidad de Tiradas')
    axs[1,0].set_ylim([8.5,12.5])
    axs[1,0].set(xlabel='Cantidad de Tiradas', ylabel='Desvío Estandar')
    axs[1,0].legend(loc='upper right')

    axs[1,1].set_title('Varianza para N Cantidad de Tiradas')
    axs[1,1].set_ylim([80,150])
    axs[1,1].set(xlabel='Cantidad de Tiradas', ylabel='Varianza')
    axs[1,1].legend(loc='upper right')


def AplicarEstiloPromedio(axs):
    axs[0,0].set_title('Promedio de Frecuencia Relativa de aciertos')
    axs[0,0].set_ylim([0,0.1])
    axs[0,0].set(xlabel='Cantidad de Tiradas', ylabel='Frecuencia Relativa')
    axs[0,0].legend(loc='upper right')
    
    axs[0,1].set_title('Promedio de Valor Promedio de Jugadas de Ruleta en N Cantidad de Tiradas')
    axs[0,1].set_ylim([0,36])
    axs[0,1].set(xlabel='Cantidad de Tiradas', ylabel='Valor Promedio')
    axs[0,1].legend(loc='upper right')
   
    axs[1,0].set_title('Promedio de Desvío Estandar para N Cantidad de Tiradas')
    axs[1,0].set_ylim([8.5,12.5])
    axs[1,0].set(xlabel='Cantidad de Tiradas', ylabel='Desvío Estandar')
    axs[1,0].legend(loc='upper right')

    axs[1,1].set_title('Promedio de Varianza para N Cantidad de Tiradas')
    axs[1,1].set_ylim([80,150])
    axs[1,1].set(xlabel='Cantidad de Tiradas', ylabel='Varianza')
    axs[1,1].legend(loc='upper right')

main()