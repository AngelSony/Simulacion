import numpy.random as nr
import matplotlib.pyplot as plt
class Funciones:
    def suma(self, lista):
        sum = 0
        for i in range (0, len(lista)):
            sum += lista[i]
        return sum

    def graficar(self, lista):
        sum = 0
        ejex = []
        ejey = []
        for i in range (0, len(lista)):
            sum += lista[i]
            ejex.append(i+1)
            ejey.append(sum/(i+1))
        plt.plot(ejex,ejey, 'r')
        plt.show()

class Ruleta:
    obj = Funciones()
    list = []
    sum = 0
    for i in range (1, 9999):
        list.append(nr.randint(0,36))
        sum += list[i-1]
        print(sum/i)
    print("Resultado final: ")
    print(obj.suma(list)/i)
    obj.graficar(list)