import numpy as np
import matplotlib.pyplot as plt
import statistics as stat

class Constant:
    NROTIRADAS = 9999
    PROMEDIO = 18
    VARIANZA = 114
    DESVIO_ESTANDAR = np.sqrt(VARIANZA)

ValoresRuleta = [[x for x in range(36)]] 
Colores = ["r-", "g-", "y-", "b-", "c-", "k:"]
Participantes =["Hernan","Bruno","Angel","Maxi","Ova"]
Cantidad_Muestras = len(Participantes)
Valores_Estadisticos = [[0,0,0,0,0] for r in range(Cantidad_Muestras+1)]
Eje_x = [(i+1) for i in range(Constant.NROTIRADAS)]
fig, axs = plt.subplots(2,2)
Tiradas = [[] for j in range(Cantidad_Muestras)]
fRelativa = [[] for j in range(Cantidad_Muestras + 1)]
Promedio = [[] for j in range(Cantidad_Muestras + 1)]
Desvio = [[] for j in range(Cantidad_Muestras + 1)]
Varianza = [[] for j in range(Cantidad_Muestras + 1)]

def main():
    for j in range(Cantidad_Muestras):
        Muestreo(j)
    Graficar()
    Promedios()
    Tabla()
    plt.show()

def Tabla():
    Estadisticos = ["fA(X)","fR(X) (%)","Media","Desvío","Varianza"]
    Cantidad_Columnas = len(Estadisticos)
    Participantes.append("Promedios")
    
    fig, ax = plt.subplots() 
    ax.set_axis_off() 
    table = ax.table( 
        cellText = Valores_Estadisticos,  
        rowLabels = Participantes,  
        colLabels = Estadisticos, 
        rowColours =["tab:red", "tab:green","tab:olive","tab:blue","tab:cyan","tab:gray"],
        colColours =["palegreen"] * Cantidad_Columnas, 
        cellLoc ='center',  
        loc ='upper left')         
   
    ax.set_title('Estadísticos de '+ str(Cantidad_Muestras)+' jugadores en '+str(Constant.NROTIRADAS+1)+' tiradas', fontweight ="bold") 

def Muestreo(j):
    sum = 0
    cont = 0
    for i in range (Constant.NROTIRADAS):
        tirada = np.random.randint(0,37)
        cont += tirada
        Tiradas[j].append(tirada)
        if(Tiradas[j][i] == 12): #El programa está determinado para estudiar la aparicion del numero 12
            sum += 1
        fRelativa[j].append((sum/(i+1)))
        Promedio[j].append(cont/(i+1))
        Desvio[j].append(np.std(Tiradas[j]))
        Varianza[j].append(np.square(Desvio[j][i]))
        if (i == Constant.NROTIRADAS-1):
            Valores_Estadisticos[j][0] = sum
            Valores_Estadisticos[j][1] = round(fRelativa[j][i] * 100,2)
            Valores_Estadisticos[j][2] = round(Promedio[j][i],2)
            Valores_Estadisticos[j][3] = round(Desvio[j][i],4)
            Valores_Estadisticos[j][4] = round(Varianza[j][i],4)

def Graficar():
    fig.suptitle("10.000 Tiradas de ruleta para 5 jugadores en simultaneo")
    for j in range (Cantidad_Muestras):      
        axs[0,0].plot(Eje_x, fRelativa[j], Colores[j], label = Participantes[j])
        axs[0,1].plot(Eje_x, Promedio[j], Colores[j], label = Participantes[j])
        axs[1,0].plot(Eje_x, Desvio[j], Colores[j], label = Participantes[j])
        axs[1,1].plot(Eje_x, Varianza[j], Colores[j], label = Participantes[j])
        AplicarEstilo(axs)

def Promedios():
    fig, axs = plt.subplots(2,2)
    fig.suptitle("Promedio de las 5 Cantidad_Muestras de 10.000 Tiradas")
    for i in range(Constant.NROTIRADAS):
        fRelativa[Cantidad_Muestras].append(np.mean([fRelativa[j][i] for j in range(Cantidad_Muestras)]))
        Promedio[Cantidad_Muestras].append(np.mean([Promedio[j][i] for j in range(Cantidad_Muestras)]))
        Desvio[Cantidad_Muestras].append(np.mean([Desvio[j][i] for j in range(Cantidad_Muestras)]))
        Varianza[Cantidad_Muestras].append(np.mean([Varianza[j][i] for j in range(Cantidad_Muestras)]))
        if (i == Constant.NROTIRADAS-1):
            Valores_Estadisticos[Cantidad_Muestras][0] = round(fRelativa[Cantidad_Muestras][i] * (Constant.NROTIRADAS+1),2)
            Valores_Estadisticos[Cantidad_Muestras][1] = round(fRelativa[Cantidad_Muestras][i] * 100,2)
            Valores_Estadisticos[Cantidad_Muestras][2] = round(Promedio[Cantidad_Muestras][i],2)
            Valores_Estadisticos[Cantidad_Muestras][3] = round(Desvio[Cantidad_Muestras][i],4)
            Valores_Estadisticos[Cantidad_Muestras][4] = round(Varianza[Cantidad_Muestras][i],4)
    axs[0,0].plot(Eje_x, fRelativa[Cantidad_Muestras], Colores[5], label="Frecuencia de aciertos Promedio de los 5 jugadores")
    axs[0,1].plot(Eje_x, Promedio[Cantidad_Muestras], Colores[5], label="Promedio de los valores Promedio de los 5 jugadores en la n-ésima jugada")
    axs[0,1].hlines(Constant.PROMEDIO, 0, Constant.NROTIRADAS, "red", label="Valor Esperado: "+str(Constant.PROMEDIO))
    axs[1,0].plot(Eje_x, Desvio[Cantidad_Muestras], Colores[5], label="Desvio Promedio de los 5 jugadores en la n-ésima jugada")
    axs[1,0].hlines(Constant.DESVIO_ESTANDAR, 0, Constant.NROTIRADAS, "red", label="Desvio Estándar Esperado: "+str(round(Constant.DESVIO_ESTANDAR,2)))
    axs[1,1].plot(Eje_x, Varianza[Cantidad_Muestras], Colores[5], label="Varianza Promedio de los 5 jugadores en la n-ésima jugada")
    axs[1,1].hlines(Constant.VARIANZA, 0, Constant.NROTIRADAS, "red", label="Varianza Esperada: "+str(Constant.VARIANZA))
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