import numpy as np
import matplotlib.pyplot as plt
class Funciones:
    def graficar(self):
        colores = ['r', 'g', 'y', 'b', 'purple']
        fig, axs = plt.subplots(2,2)
        for j in range (5):
            sum12 = 0
            ejex = []
            tiradas = []
            promedio = []
            fRelativa12 = []
            desvio = []
            varianza = []
            for i in range (0, 999):
                tirada = np.random.randint(0,36)
                tiradas.append(tirada)
                if(tirada == 12):
                    sum12 += 1
                fRelativa12.append(sum12/(i+1))
                ejex.append(i+1)
                promedio.append(np.mean(tiradas))
                desvio.append(np.std(tiradas))
                varianza.append(np.var(tiradas))
            axs[0,1].plot(ejex, promedio, colores[j])
            axs[0,0].plot(ejex, fRelativa12, colores[j])
            axs[1,0].plot(ejex, desvio, colores[j])
            axs[1,1].plot(ejex, varianza, colores[j])

        axs[0,1].set_title('Promedio')
        axs[0,1].set(xlabel='n', ylabel='vp')
        axs[0,0].set_title('Frecuencia Relativa')
        axs[0,0].set(xlabel='n', ylabel='fr')
        axs[1,0].set_title('Desvío Estandar')
        axs[1,0].set(xlabel='n', ylabel='vd')
        axs[1,1].set_title('Varianza')
        axs[1,1].set(xlabel='n', ylabel='vv')
        plt.show()

class Ruleta:
    obj = Funciones()
    obj.graficar()