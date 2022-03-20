import numpy.random as nr
import matplotlib.pyplot as plt
class Funciones:
    def graficar(self):
        sum = 0
        ejex = []
        lista = []
        for i in range (0, 9999):
            sum += nr.randint(0,36)
            print(sum)
            ejex.append(i+1)
            lista.append(sum/(i+1))
        plt.plot(ejex,lista, 'r')
        plt.show()

class Ruleta:
    obj = Funciones()
    obj.graficar()