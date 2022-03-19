import numpy.random as nr
import matplotlib.pyplot as plt
class Funciones:
    def suma(self, lista):
        sum = 0
        for i in range (0, len(lista)):
            sum += lista[i]
        return sum

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