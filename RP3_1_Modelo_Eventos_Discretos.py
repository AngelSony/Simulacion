import numpy as np
import math

UValues = [.5121,.8116,.6717,.1901,.5184,.6467,.8954,.3884,.0279,.8365]
Alfa = .7
Beta = .66
ArrivalTimes = []
DepartureTimes = []
EventTimes = []
global SystemState
SystemState = "Free"

def Main_Program():
    DispachedClients = 0
    Clock = .0
    
    EventType = ""
    Queue = 0

    Initialization_Routine(ArrivalTimes,DepartureTimes)
    while DispachedClients < 10:
        Timing_Routine(Clock,ArrivalTimes,DepartureTimes,EventType)
        Event_Routine(EventType,Queue,DispachedClients,SystemState)
    print("EventTimes:")
    print(EventTimes)
    #Report_Generator()

def Initialization_Routine(ArrivalTimes,DepartureTimes):
    for Value in UValues:
        ArrivalTimes.append(truncate(-1 * Alfa * np.log(Value),4))
        DepartureTimes.append(truncate(-1 * Beta * np.log(Value),4))
    print("ArrivalTimes:")
    print(ArrivalTimes)
    print("DepartureTimes:")
    print(DepartureTimes)

    return ArrivalTimes,DepartureTimes

def Timing_Routine(Clock,ArrivalTimes,DepartureTimes,EventType):
    if (SystemState == "Free"):
        EventType  = "Arrival"
        Clock += ArrivalTimes[0]
        ArrivalTimes.pop(0) #Elimina el primer elemento de la lista
    else:
        if (ArrivalTimes[0] < DepartureTimes[0]):
            EventType  = 'Arrival'
            Clock += ArrivalTimes[0]
            ArrivalTimes.pop(0) #Elimina el primer elemento de la lista
        else:
            EventType  = 'Departure'
            Clock += DepartureTimes[0]
            DepartureTimes.pop(0) #Elimina el primer elemento de la lista        
    EventTimes.append(Clock)
    return EventType

def Event_Routine(EventType,Queue,DispachedClients,SystemState):
    if (EventType == 'Arrival'):
        if (SystemState == 'Free'):
            SystemState = 'Busy'
        else:
            Queue += 1
    else: # EventType = 'Partida'
        DispachedClients += 1
        if (Queue == 0 ):
            SystemState = 'Free'
        else:
            Queue -= 1

def Report_Generator():
    print("REPORTE AQUI")

def truncate(num, n):
    integer = int(num * (10**n))/(10**n)
    return float(integer)

Main_Program()