import numpy as np
import matplotlib.pyplot as plt

class EventType:
    ARRIVAL = 'ARRIVAL'
    DEMAND = 'DEMAND'
    SIM_END = 'SIM_END'
    EVAL = 'EVAL'

class DemandType:
    def __init__(self, cant, begin):
        self.cant = cant
        self.begin = begin

class Event:
    def __init__(self, eventType, timeOfOccurence):
        self.type = eventType
        self.time = timeOfOccurence

class Inventario:
    def __init__(self, corridas):
        self.num_meses = 120 # Meses de la simulacion
        self.media_demandas = 0.1 # Promedio en meses del tiempo entre demandas
        # self.maximumDemandsSize = 4 # Tamaño maximo de las demandas 1,2,3,4
        self.costo_orden = 32 # Costo inicial de una orden
        self.costo_incremental = 3 # Costo extra por item ordenado
        self.delivery_lag_minimo = 0.5 # Tiempo minimo para una entrega
        self.delivery_lag_maximo = 1 # Tiempo maximo para una entrega
        self.inventario_inicial = 60 # Valor inicial de stock en inventario
        self.costo_mantenimiento = 1 # Costo mensual por item en inventario $
        self.costo_faltante = 5 # Costo mensual de tener un producto en el backlog sin stock $
        self.politicas_minimas = [20, 20, 20, 20, 40, 40, 40, 60, 60, 80] 
        self.politicas_maximas = [40, 60, 80, 100, 60, 80, 100, 80, 100, 100]
        # self.amountEvents = 4 # Arrival / Demand / End of Simulation / Inventory evaluation
        self.corridas = corridas
        self.tipos_demandas = [
            DemandType(cant = 1, begin = 0.16),
            DemandType(cant = 2, begin = 0.5),
            DemandType(cant = 3, begin = 0.83),
            DemandType(cant = 4, begin = 1)
        ]
        
        self.iniciar()

    def iniciar(self):
        self.mostrar_datos_iniciales()
        for i in range(len(self.politicas_minimas)):
            self.inicializar_estadisticas()
            for corrida in range(self.corridas):
                self.initialization_routine(self.politicas_minimas[i], self.politicas_maximas[i])

                while self.next_event.type != EventType.SIM_END:
                    self.timing_routine()

                    self.update_stats()

                    self.event_routine()
            self.mostrar_datos_finales()

    def initialization_routine(self, politica_minima, politica_maxima):
        self.clock = 0
        self.inventario = self.inventario_inicial

        self.costo_ordenes = 0
        self.area_mantenimiento = 0
        self.area_faltante = 0

        self.cantidad_productos_pedidos = 0
        self.politica_minima = politica_minima
        self.politica_maxima = politica_maxima

        self.tiempo_ultimo_evento = 0
        self.events = [
            Event(EventType.EVAL, 0), # Primer evento: evaluacion
            Event(EventType.DEMAND, np.random.exponential(self.media_demandas)),
            Event(EventType.SIM_END, self.num_meses)
        ]

        self.next_event = Event(None, None) # Evento basura para poder seguir con el loop

    def timing_routine(self):
        self.next_event = min(self.events, key = lambda event: event.time)

        self.events.remove(self.next_event)

        self.clock = self.next_event.time

    def update_stats(self):
        time_since_last_event = self.clock - self.tiempo_ultimo_evento
        self.tiempo_ultimo_evento = self.clock


        if self.inventario < 0:
            self.area_faltante -= self.inventario * time_since_last_event
        elif self.inventario > 0:
            self.area_mantenimiento += self.inventario * time_since_last_event

    def event_routine(self):
        if self.next_event.type == EventType.ARRIVAL:
            self.arribo()
        elif self.next_event.type == EventType.DEMAND:
            self.demanda()
        elif self.next_event.type == EventType.SIM_END:
            self.guardar_datos_corrida()
        elif self.next_event.type == EventType.EVAL:
            self.evaluar_inventario()

    def evaluar_inventario(self):
        if self.inventario < self.politica_minima:
            self.cantidad_productos_pedidos = self.politica_maxima - self.inventario

            self.costo_ordenes += self.costo_mantenimiento + self.costo_incremental * self.cantidad_productos_pedidos

            self.agregar_arrival()

        self.agregar_evaluacion()

    def demanda(self):
        demanda = self.get_cantidad_demandada()

        self.inventario -= demanda

        self.agregar_demanda()

    def arribo(self):
        self.inventario += self.cantidad_productos_pedidos


    # Helpers
    def agregar_arrival(self):
        self.events.append(Event(EventType.ARRIVAL, self.clock + np.random.uniform(self.delivery_lag_minimo, self.delivery_lag_maximo)))

    def agregar_evaluacion(self):
        self.events.append(Event(EventType.EVAL, self.clock + 1))

    def agregar_demanda(self):
        self.events.append(Event(EventType.DEMAND, self.clock + np.random.exponential(self.media_demandas)))

    def get_cantidad_demandada(self):
        num = np.random.uniform(0, 1)

        for tipo_demanda in self.tipos_demandas:
            if num < tipo_demanda.begin:
                return tipo_demanda.cant

    def guardar_datos_corrida(self):
        promedio_costo_ordenes_corrida = self.costo_ordenes / self.num_meses
        promedio_costo_mantenimiento_corrida = self.costo_mantenimiento * self.area_mantenimiento / self.num_meses
        promedio_costo_faltante_corrida = self.costo_faltante * self.area_faltante / self.num_meses
        costo_total_corrida = promedio_costo_ordenes_corrida + promedio_costo_mantenimiento_corrida + promedio_costo_faltante_corrida

        self.costo_promedio_total_ordenes.append(promedio_costo_ordenes_corrida)
        self.costo_promedio_total_mantenimiento.append(promedio_costo_mantenimiento_corrida)
        self.costo_promedio_total_faltante.append(promedio_costo_faltante_corrida)
        self.costo_total.append(costo_total_corrida)

    # Helpers
    def inicializar_estadisticas(self):
        self.costo_promedio_total_ordenes = []
        self.costo_promedio_total_mantenimiento = []
        self.costo_promedio_total_faltante = []
        self.costo_total = []

    def mostrar_datos_iniciales(self):
        print('DATOS INICIALES:')
        print(f"Nivel inicial de inventario:            {self.inventario_inicial}")
        print(f"Tiempo medio entre demanda:             {self.media_demandas}")
        print(f"Tiempo de entrega: entre                {self.delivery_lag_minimo} y {self.delivery_lag_maximo} meses")
        print(f"Duracion de la simulacion:              {self.num_meses} meses")
        print(f"K = {self.costo_orden}  i = {self.costo_incremental}  h = {self.costo_mantenimiento}  PI = {self.costo_faltante}")
        print('-------------------------------------------------------------------------------------------------------------------')

    def mostrar_datos_finales(self):
        costo_ordenes_promedio = np.mean(self.costo_promedio_total_ordenes)
        costo_mantenimiento_promedio = np.mean(self.costo_promedio_total_mantenimiento)
        costo_faltante_promedio = np.mean(self.costo_promedio_total_faltante)
        costo_total = np.mean(self.costo_total)

        print(f'Politica minima: {self.politica_minima}, Politica maxima: {self.politica_maxima}')
        print(f'Promedio Costo Total Mensual: {round(costo_total, 2)}')
        print(f'Promedio Costo Pedido Mensual: {round(costo_ordenes_promedio, 2)}')
        print(f'Promedio Costo Mantenimiento Mensual: {round(costo_mantenimiento_promedio, 2)}')
        print(f'Promedio Costo Faltantes Mensual: {round(costo_faltante_promedio, 2)}', '\n')

        print('-------------------------------------------------------------------------------------------------------------------', '\n')
        # print(f"[{self.politica_minima},{self.politica_maxima}] \t {round(costo_total, 2)} \t\t\t {round(costo_ordenes_promedio, 2)} \t\t\t\t {round(costo_mantenimiento_promedio, 2)} \t\t\t\t {round(costo_faltante_promedio, 2)}")
        
        self.plot(self.costo_promedio_total_ordenes, "Costo de Orden Promedio", "Dinero ($)",
        self.costo_promedio_total_mantenimiento, "Costo de Almacenamiento Promedio", "Dinero ($)",
        self.costo_promedio_total_faltante, "Costo de Faltante Promedio", "Dinero ($)",
        self.costo_total, "Costo Total Promedio", "Dinero ($)",
        f"Minimo Estrategia: {self.politica_minima}  Maximo Estrategia: {self.politica_maxima}"
        )

    def plot(self, a1, t1, l1, a2, t2, l2, a3, t3, l3, a4, t4, l4, titulo):
        fig, axs = plt.subplots(2, 2, constrained_layout=True)
        axs[0, 0].set_title(t1)
        axs[0, 0].set_xlabel("Cantidad de Corridas")
        axs[0, 0].set_ylabel(l1)
        axs[0, 0].grid(True)
        axs[0, 0].plot(a1)

        axs[1, 0].set_title(t2)
        axs[1, 0].set_xlabel("Cantidad de Corridas")
        axs[1, 0].set_ylabel(l2)
        axs[1, 0].grid(True)
        axs[1, 0].plot(a2)

        axs[0, 1].set_title(t3)
        axs[0, 1].set_xlabel("Cantidad de Corridas")
        axs[0, 1].set_ylabel(l3)
        axs[0, 1].grid(True)
        axs[0, 1].plot(a3)

        axs[1, 1].set_title(t4)
        axs[1, 1].set_xlabel("Cantidad de Corridas")
        axs[1, 1].set_ylabel(l4)
        axs[1, 1].grid(True)
        axs[1, 1].plot(a4)

        fig.suptitle(titulo)
        plt.savefig(f'graficos/Experimento-min-{self.politica_minima}-max-{self.politica_maxima}.png')
        #plt.show()

Inventario(100)