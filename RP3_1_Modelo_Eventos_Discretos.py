import numpy as np
import math

UValues = [.5121,.8116,.6717,.1901,.5184,.6467,.8954,.3884,.0279,.8365]
Alfa = .7
Beta = .66
ArrivalTimes = []
DepartureTimes = []
EventTimes = []


def Main_Program():
    SystemState = ['Free']

    DispachedClients = [0]
    Clock = [.0]
    
    EventType = [""]
    Queue = [0]

    Initialization_Routine()
    while DispachedClients[0] < 10:
        Timing_Routine(SystemState, EventType, Clock,DispachedClients)
        Event_Routine(SystemState,EventType,Queue)
    print("EventTimes:")
    print(EventTimes)
    #Report_Generator()

def Initialization_Routine():
    for Value in UValues:
        ArrivalTimes.append(truncate(-1 * Alfa * np.log(Value),4))
        DepartureTimes.append(truncate(-1 * Beta * np.log(Value),4))
    print("ArrivalTimes:")
    print(ArrivalTimes)
    print("DepartureTimes:")
    print(DepartureTimes)

def Timing_Routine(SystemState,EventType, Clock,DispachedClients):
    if (SystemState[0] == "Free"):
        EventType[0]  = "Arrival"
        Clock[0] += ArrivalTimes[0]
        ArrivalTimes.pop(0) #Elimina el primer elemento de la lista
    else:
        if (len(ArrivalTimes) != 0 and ArrivalTimes[0] < DepartureTimes[0]):
            EventType[0]  = 'Arrival'
            Clock[0] += ArrivalTimes[0]
            ArrivalTimes.pop(0) #Elimina el primer elemento de la lista
        else:
            EventType[0]  = 'Departure'
            Clock[0] += DepartureTimes[0]
            DepartureTimes.pop(0) #Elimina el primer elemento de la lista
            DispachedClients[0] += 1
    EventTimes.append(truncate(Clock[0],4))

def Event_Routine(SystemState,EventType,Queue):
    if (EventType[0] == 'Arrival'):
        if (SystemState[0] == 'Free'):
            SystemState[0] = 'Busy'
        else:
            Queue[0] += 1
    else: # EventType = 'Departure'
       
        if (Queue[0] == 0 ):
            SystemState[0] = 'Free'
        else:
            Queue[0] -= 1

def Report_Generator():
    print("REPORTE AQUI")

def truncate(num, n):
    integer = int(num * (10**n))/(10**n)
    return float(integer)

Main_Program()