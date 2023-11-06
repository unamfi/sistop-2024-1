import copy

#Definiendo la clase procesos
class proceso:
    def __init__(self, id, llegada,t):
        self.id= id
        self.llegada = llegada
        self.t = t
        self.aux = 0


#Imprimir las variables de rendimiento
def imprimirRendimiento (algoritmo,T,E,P):
    print("")
    print( algoritmo+": T=" + str(T) +", E="+ str(E) +", P="+ str(P))
 

#Algoritmo First Come First Serve
def FCFS(procesos):
    tiempo = 0
    T=[]
    E=[]
    P=[]

    #Se inicia el algoritmo y se obtienen las variables T, E y P
    for proceso in procesos:
        ticksProceso=proceso.t
        if proceso.llegada <= tiempo:
            while proceso.t != 0:
                proceso.t = proceso.t-1
                tiempo = tiempo+1
                print(proceso.id, end ="")
        T.append(tiempo-proceso.llegada)
        E.append(tiempo-proceso.llegada-ticksProceso)
        P.append((tiempo-proceso.llegada)/ticksProceso)
    imprimirRendimiento ("FCFS",sum(T) / len(T),sum(E) / len(E),sum(P) / len(P))


#Algoritmo Round Robin (1)
def RR1(procesos):
    tiempo = 0
    T=[]
    E=[]
    P=[]
    tiempoProcesos=0
    tAux=[]
    
    #Para definir el tiempo total que tardarán los procesos (sumados)
    for proceso in procesos:
        tiempoProcesos= tiempoProcesos + proceso.t
        tAux.append(proceso.t)
    
    #Se inicia el algoritmo
    while(tiempo<tiempoProcesos):
        for proceso in procesos:
            if proceso.llegada <= tiempo:
                if proceso.t != 0:
                    proceso.t = proceso.t-1
                    tiempo = tiempo+1
                    print(proceso.id, end ="")

                    #proceso.aux es el tiempo de finalización
                    if proceso.t == 0 and proceso.aux == 0 :
                        proceso.aux = tiempo

    #Para obtener las variables T, E y P
    for i in range(0,len(procesos)):
        T.append(procesos[i].aux-procesos[i].llegada)
        E.append(procesos[i].aux-procesos[i].llegada-tAux[i])
        P.append((procesos[i].aux-procesos[i].llegada)/tAux[i])
    imprimirRendimiento ("RR1",sum(T) / len(T),sum(E) / len(E),sum(P) / len(P))


#Algoritmo Round Robin (4)
def RR4(procesos):
    tiempo = 0
    T=[]
    E=[]
    P=[]
    contador = 0
    tiempoProcesos=0
    tAux=[]
    
    #Para definir el tiempo total que tardarán los procesos (sumados)
    for proceso in procesos:
        tiempoProcesos= tiempoProcesos + proceso.t
        tAux.append(proceso.t)
    
    #Se inicia el algoritmo
    while(tiempo<tiempoProcesos):
        for proceso in procesos:
            contador = 0
            if proceso.llegada <= tiempo:
                while (contador<4):
                    if proceso.t != 0:
                        proceso.t = proceso.t-1
                        tiempo = tiempo+1
                        print(proceso.id, end ="")

                        #proceso.aux es el tiempo de finalización
                        if proceso.t == 0 and proceso.aux == 0 :
                            proceso.aux = tiempo
                    contador = contador+1

    #Para obtener las variables T, E y P
    for i in range(0,len(procesos)):
        T.append(procesos[i].aux-procesos[i].llegada)
        E.append(procesos[i].aux-procesos[i].llegada-tAux[i])
        P.append((procesos[i].aux-procesos[i].llegada)/tAux[i])
    imprimirRendimiento ("RR4",sum(T) / len(T),sum(E) / len(E),sum(P) / len(P))

#Algoritmo SPN
def SPN(procesos):
    tiempo = 0
    T=[]
    E=[]
    P=[]
    tiempoProcesos=0
    tAux=[]
    sorted_procesos = sorted(procesos, key=lambda proceso: proceso.t)
    tMax = sorted_procesos[-1].t

    #Para definir el tiempo total que tardarán los procesos (sumados)
    for proceso in procesos:
        tiempoProcesos= tiempoProcesos + proceso.t
        tAux.append(proceso.t)

    #Se inicia el algoritmo
    while(tiempo<tiempoProcesos):
        for i in range(0,tMax+1):
            for proceso in procesos:
                if proceso.llegada <= tiempo and proceso.t <= i:
                    while proceso.t != 0:
                        proceso.t = proceso.t-1
                        tiempo = tiempo+1
                        print(proceso.id, end ="")
                    if(proceso.t == 0 and proceso.aux==0):
                        proceso.aux=tiempo

    #Para obtener las variables T, E y P
    for i in range (0,len(procesos)):
        T.append(procesos[i].aux-procesos[i].llegada)
        E.append(procesos[i].aux-procesos[i].llegada-tAux[i])
        P.append((procesos[i].aux-procesos[i].llegada)/tAux[i])
    imprimirRendimiento ("SPN",sum(T) / len(T),sum(E) / len(E),sum(P) / len(P))



def rondas(ronda,procesos):

    # Imprimir el valor de los procesos al inicio de la evaluación
    print("Ronda " + str(ronda))
    for proceso in procesos:
        print(str(proceso.id) +":"+ str(proceso.llegada) +", t="+ str(proceso.t), end = '; ')
    print("\n")
    sorted_procesos = sorted(procesos, key=lambda proceso: proceso.llegada)

    # Mandar una copia de los procesos ordenados respecto a su llegada a cada uno de los algoritmos
    FCFS(copy.deepcopy(sorted_procesos))
    print("")
    RR1(copy.deepcopy(sorted_procesos))
    print("")
    RR4(copy.deepcopy(sorted_procesos))
    print("")
    SPN(copy.deepcopy(sorted_procesos))

# creando lista de procesos1
procesos1 = []
# Append de los objetos proceso a la lista de procesos
procesos1.append(proceso('A',0,3))
procesos1.append(proceso('B',1,5))
procesos1.append(proceso('C',3,2 ))
procesos1.append(proceso('D',9,5 ))
procesos1.append(proceso('E',12,5 ))

# creando lista de procesos2
procesos2 = []
# Append de los objetos proceso a la lista de procesos
procesos2.append(proceso('A',0,2))
procesos2.append(proceso('B',1,5))
procesos2.append(proceso('C',5,3 ))
procesos2.append(proceso('D',10,5 ))
procesos2.append(proceso('E',12,5 ))

# creando lista de procesos2
procesos3 = []
# Append de los objetos proceso a la lista de procesos
procesos3.append(proceso('A',0,5))
procesos3.append(proceso('B',2,5))
procesos3.append(proceso('C',4,5 ))
procesos3.append(proceso('D',12,5 ))
procesos3.append(proceso('E',12,5 ))

# creando lista de procesos2
procesos4 = []
# Append de los objetos proceso a la lista de procesos
procesos4.append(proceso('A',0,2))
procesos4.append(proceso('B',1,3))
procesos4.append(proceso('C',2,1 ))
procesos4.append(proceso('D',3,4 ))
procesos4.append(proceso('E',4,5 ))

# creando lista de procesos2
procesos5 = []
# Append de los objetos proceso a la lista de procesos
procesos5.append(proceso('A',0,4))
procesos5.append(proceso('B',4,2))
procesos5.append(proceso('C',5,5 ))
procesos5.append(proceso('D',10,4 ))
procesos5.append(proceso('E',14,5 ))

#Creando una única lista de procesos
procesosTotales = []
procesosTotales.append(procesos1)
procesosTotales.append(procesos2)
procesosTotales.append(procesos3)
procesosTotales.append(procesos4)
procesosTotales.append(procesos5)

#Empezar el algoritmo por rondas con la lista de todos los procesos
for index, procesos in enumerate(procesosTotales):
    print("\n------------------------\n")
    rondas(index+1,procesos)



