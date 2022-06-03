from collections import deque
import numpy as np
import os
import matplotlib.pyplot as plt

# Promedio de clientes en el sistema
# Promedio de clientes en cola.
# Tiempo promedio en sistema
# Tiempo promedio en cola. Calcular demora promedio en cola por corrida, sumarlas y dividirlas por cantidad de corridas. Sería d(n), clase 07/04 56:00:00.
# Utilización del servidor
# Probabilidad de n clientes en cola
# Probabilidad de denegación de servicio (cola finita de tamaño: 0, 2, 5, 10, 50)

# Variar, al menos, las tasas de arribo: 25%, 50%, 75%, 100%, 125% con respecto a la tasa de servicio
# Mínimo de 10 corridas por cada experimento


# Constantes
class EventType:
    ARRIVAL = 'ARRIVAL'
    DEPARTURE = 'DEPARTURE'
class StatusCode:
    BUSY = 'BUSY'
    IDLE = 'IDLE'

# Clases
class Event:
    def __init__(self, eventType, timeOfOccurence):
        self.type = eventType
        self.time = timeOfOccurence

class Customer:
    def __init__(self, arrival_time):
        self.arrival_time = arrival_time

class Experiment:
    def __init__(self, service_rate, arrival_rate, queue_size, num_iterations):
        self.service_rate = service_rate
        self.arrival_rate = arrival_rate
        self.queue_size = queue_size
        self.num_iterations = num_iterations

        self.results = []

    def add_iteration_result(self, iteration_result):
        self.results.append(iteration_result)

    def calc_results(self):
        # TODO: Calc experiment results
        self.avg_delay_queue = sum(map(lambda result: result.avg_delay_queue, self.results)) / self.num_iterations
        self.reject_prob = sum(map(lambda result: result.reject_prob, self.results)) / self.num_iterations
        self.avg_cust_queue = sum(map(lambda result: result.avg_cust_queue, self.results)) / self.num_iterations
        self.server_usage = sum(map(lambda result: result.server_usage, self.results)) / self.num_iterations
        self.avg_cust_system = sum(map(lambda result: result.avg_cust_system, self.results)) / self.num_iterations
        self.avg_delay_system = sum(map(lambda result: result.avg_delay_system, self.results)) / self.num_iterations
        self.time = sum(map(lambda result: result.time, self.results)) / self.num_iterations

    def plot(self, id):
        # TODO: Plot
        self.fig, self.axs = plt.subplots(3, 2, constrained_layout=True)

        self.plot_single(0, 0, list(map(lambda result: result.avg_cust_system, self.results)), 'Promedio de clientes en sistema', 'Cantidad')
        self.plot_single(1, 0, list(map(lambda result: result.avg_cust_queue, self.results)), 'Promedio de clientes en cola', 'Cantidad')
        self.plot_single(2, 0, list(map(lambda result: result.avg_delay_system, self.results)), 'Tiempo promedio en sistema', 'Tiempo')
        self.plot_single(0, 1, list(map(lambda result: result.avg_delay_queue, self.results)), 'Tiempo promedio en cola', 'Tiempo')
        self.plot_single(1, 1, list(map(lambda result: result.server_usage, self.results)), 'Utilizacion del servidor', 'Utilizacion (%)')
        self.plot_single(2, 1, list(map(lambda result: result.reject_prob, self.results)), 'Probabilidad de denegacion de servicio', 'Probabilidad (%)')

        self.fig.suptitle(f'Tasa de Servicio: {self.service_rate} - Tasa de Arribo: {self.arrival_rate} - Tamaño de Cola: {self.queue_size}')
        
        plt.savefig(f'graficos/ExperimentoMM1-arribo-{self.arrival_rate}-cola-{self.queue_size}.png')


    def plot_single(self, posX, posY, data, title, yLabel):
        self.axs[posX, posY].set_title(title)
        self.axs[posX, posY].set_xlabel("Cantidad de Corridas")
        self.axs[posX, posY].set_ylabel(yLabel)
        self.axs[posX, posY].grid(True)
        self.axs[posX, posY].plot(data)


class IterationResult:
    def calc_avg_delay_queue(self, total_delays, num_served_customers):
        self.avg_delay_queue = total_delays / num_served_customers

    def calc_reject_prob(self, num_arrivals, num_rejected):
        self.reject_prob = num_rejected / num_arrivals

    def calc_avg_cust_queue(self, area_customers_in_queue, clock):
        self.avg_cust_queue = area_customers_in_queue / clock

    def calc_server_usage(self, area_server_status, clock):
        self.server_usage = area_server_status / clock

    def calc_avg_cust_system(self, lambda_parameter, mu_parameter):
        self.avg_cust_system = self.avg_cust_queue + (lambda_parameter / mu_parameter)

    def calc_avg_delay_system(self, mu_parameter):
        self.avg_delay_system = self.avg_delay_queue + (1 / mu_parameter)

    def set_experiment_time(self, time):
        self.time = time


class MM1:
    def __init__(self, max_served_customers, arrival_rate, service_rate, queue_size):
        # Parametros
        self.max_served_customers = max_served_customers
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.queue_size = queue_size # TODO: IMPLEMENT QUEUE SIZE

        # Variables de estado (rutina de inicializacion)
        self.initialization_routine()

    def start(self):
        while self.num_served_customers < self.max_served_customers:
            self.timing_routine()

            self.update_stats()

            self.event_routine()

        return self.build_results()

        # self.report_generator()

    # Main Flow
    def initialization_routine(self):
        # Variables de estado
        self.clock = 0
        self.status = StatusCode.IDLE
        self.queue = deque([])
        self.events = []
        self.add_arrival() # Primer evento: llegada en un instante aleatorio obtenido con dist. exponencial
        self.nextEvent = None
        self.num_served_customers = 0

        # Contadores Estadisticos
        # TODO: Agregar Inicializacion Contadores estadisticas
        self.total_delays = 0
        self.num_arrivals = 0
        self.num_rejected = 0
        self.last_event_time = 0
        self.area_customers_in_queue = 0
        self.area_server_status = 0

    def timing_routine(self):
        self.nextEvent = min(self.events, key = lambda event: event.time)

        self.events.remove(self.nextEvent)

        self.clock = self.nextEvent.time

    def update_stats(self):
        time_since_last_event = self.clock - self.last_event_time
        self.last_event_time = self.clock

        self.area_customers_in_queue += len(self.queue) * time_since_last_event
        self.area_server_status += time_since_last_event if self.status == StatusCode.BUSY else 0

    def event_routine(self):
        if self.nextEvent.type == EventType.ARRIVAL:
            self.num_arrivals += 1
            
            if self.status == StatusCode.BUSY:
                # Servidor ocupado, agregamos el customer a la cola (si hay espacio)
                if len(self.queue) < self.queue_size:
                    self.queue.append(Customer(self.clock))
                else:
                    self.num_rejected += 1
            else:
                # Servidor libre, atendemos al customer
                self.serve()
            
            self.add_arrival()
        else:
            if len(self.queue) > 0:
                self.serve()
            else:
                self.status = StatusCode.IDLE

    def report_generator(self):
        # TODO: implement or delete
        print('TO BE IMPLEMENTED')

    # Helpers
    def add_arrival(self):
        self.events.append(Event(EventType.ARRIVAL, np.random.exponential(1 / self.arrival_rate) + self.clock))

    def add_departure(self):
        self.events.append(Event(EventType.DEPARTURE, np.random.exponential(1 / self.service_rate) + self.clock))

    def serve(self):
        if (len(self.queue) > 0):
            self.total_delays += (self.clock - self.queue[0].arrival_time)
            self.queue.popleft()

        self.status = StatusCode.BUSY
        self.num_served_customers += 1
        self.add_departure()

    def build_results(self):
        # Creating entity instance
        result = IterationResult()

        # Calculating results
        result.calc_avg_delay_queue(self.total_delays, self.num_served_customers)
        result.calc_reject_prob(self.num_arrivals, self.num_rejected)
        result.calc_avg_cust_queue(self.area_customers_in_queue, self.clock)
        result.calc_server_usage(self.area_server_status, self.clock)
        result.calc_avg_cust_system(self.arrival_rate, self.service_rate)
        result.calc_avg_delay_system(self.service_rate)
        result.set_experiment_time(self.clock)

        return result

def build_experiments(service_rate, arrival_rates, queue_sizes, num_iterations):
    experiments = []
    for queue_size in queue_sizes:
        for arrival_rate in arrival_rates:
            experiments.append(Experiment(service_rate, arrival_rate, queue_size, num_iterations))
    
    return experiments


max_served_customers = 10000
num_iterations = 10
service_rate = 4

# Building experiments
arrival_rates = [.25 * service_rate, .5  * service_rate, .75  * service_rate, 1 * service_rate, 1.25 * service_rate]
queue_sizes = [0, 2, 5, 10, 50]
experiments = build_experiments(service_rate, arrival_rates, queue_sizes, num_iterations)

for experiment in experiments:
    for i in range(experiment.num_iterations):
        experiment.add_iteration_result(MM1(max_served_customers, experiment.arrival_rate, service_rate, experiment.queue_size).start())

    experiment.calc_results()

cont = 1
for experiment in experiments:
    print('-----------------------------------------------')
    print(f'EXPERIMENTO {cont} - Tasa de arribo {experiment.arrival_rate}. Tamaño de cola {experiment.queue_size}', '\n')

    print(f'Promedio de clientes en sistema:\t {str(experiment.avg_cust_system)}')
    print(f'Promedio de clientes en cola:\t {str(experiment.avg_cust_queue)}')
    print(f'Tiempo promedio en sistema:\t {str(experiment.avg_delay_system)}')
    print(f'Tiempo promedio en cola:\t {str(experiment.avg_delay_queue)}')
    print(f'Utilizacion del servidor:\t {str(experiment.server_usage)}')
    print(f'Probabilidad de denegacion de servicio:\t {str(experiment.reject_prob)}')
    print(f'El experimento finalizo en aproximadamente {str(experiment.time)} unidades de tiempo')
    print('-----------------------------------------------','\n')

    experiment.plot(cont)

    cont += 1