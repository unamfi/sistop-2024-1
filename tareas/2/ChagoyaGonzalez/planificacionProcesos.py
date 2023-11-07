import random
from queue import Queue


#definimos el nombre de los procesos y colocamos en 0 el tiempo total
listaProcesos=['A','B','C','D','E']
procesos=[]



#creamos los procesos y asignamos de forma aleatoria su tiempo llegada y de duracion
def creacionProcesos():
    
    tiempoLlegada=0
    tiempoRequerido=0
    i=0
    #la lista de procesos es una lista de listas contiene el nombre del proceso,tiempoLlegada y tiempo requerido
    while( i< len(listaProcesos)):
        if (i==0): #damos valores al primer proceso el cual su tiempo de llegada es 0
            tiempoRequerido=random.randint(2,8)
            procesos.append([listaProcesos[i],tiempoLlegada,tiempoRequerido])
            i=i+1
        #para todos los demas procesos
        tiempoRequerido=random.randint(2,8)
        tiempoLlegada+=random.randint(1,5)
    
        procesos.append([listaProcesos[i],tiempoLlegada,tiempoRequerido])
        i=i+1
    print('los procesos son' , procesos)

def FCFS():
    #metricas
    T=[]
    E=[]
    P=[]

    orden=[] #para que nos de el orden de los procesos

    cola = Queue()
    i=0
    j=0
    tiempoInicio=[]
    tiempoFinales=[]
    tiempo=0

    #ordena todos los elementos en una cola
    for i in range(len(listaProcesos)):
        cola.put(procesos[i])

    i=0
    #calculo de tiempos finales
    while(i<len(listaProcesos)):
        tiempo=tiempo+procesos[i][2]
        tiempoFinales.append(tiempo)
        i=i+1
    #print(tiempoFinales)

    i=0
    #calculo de tiempos de inicio
    while(i<len(listaProcesos)):
        tiempo=tiempoFinales[i]-procesos[i][2]
        tiempoInicio.append(tiempo)
        i=i+1
    #print(tiempoInicio)

    i=0
    #calculos de tiempos de espera
    while(i<len(listaProcesos)):

        if(i==0):   
            T.append(tiempoFinales[i])
            E.append(0)
            P.append(1)
            i=i+1

        T.append((tiempoInicio[i]-procesos[i][1]) +procesos[i][2])
        E.append(  (tiempoInicio[i]-procesos[i][1]))
        P.append( (tiempoInicio[i]-procesos[i][1])/procesos[i][2]   )
        i=i+1
    #print(T)
    #print(E)
    #print(P)

    #sacando los elementos de la cola
    i=0
    numProcesos = len(listaProcesos)

    while (i<numProcesos):
        elemento = cola.get(procesos[i])
        
        j=0
        while (j< elemento[2]):
            orden.append(elemento[0])
            
            j=j+1
        i=i+1
    #print(orden)
    
    #calculo de promedios
    PROMT = sum(T) / len(procesos)
    PROME = sum(E) / len(procesos)
    PROMP = sum(P) / len(procesos)
    print("FCFS: T=%.2f, E=%.2f, P=%.2f" % (PROMT, PROME, PROMP))
    print("Orden de ejecución:", "".join(orden))





def ronda(quantum):

    #metricas
    T = []
    E = []
    P = []

    tiempotot = 0
    i = 0
    tiempoFinal = []
    tiemporeq = [proceso[2] for proceso in procesos] #tiempo de cada proceso
    orden = ''
    

    #calculamos el tiempo total 
    for i in range (len(listaProcesos)):
        tiempotot = tiempotot+ procesos[i][2]


    while i < tiempotot:
        for i in range(len(procesos)):
            if i >= procesos[i][1] and procesos[i][2] > 0:
                ejecucion = min(quantum, procesos[i][2])  # quantum 
                procesos[i][2] -= ejecucion
                i += ejecucion
                orden += procesos[i][0]
                if procesos[i][2] == 0: #cuando un proceso haya terminado
                    tiempoFinal.append([procesos[i][0], i])

    #ordenamos por el nombre 
    tiempoFinal.sort()

    #calculo de metricas
    for i in range(len(procesos)):
        T.append(tiempoFinal[i][1] - procesos[i][1])
        E.append(T[i] - tiemporeq[i] )
        P.append(T[i] / tiemporeq[i] )

    #print(T)
    #print(E)
    #print(P)
    
    #calculo de promedios
    PROMT = sum(T) / len(procesos)
    PROME = sum(E) / len(procesos)
    PROMP = sum(P) / len(procesos)

    print("Round Robin con quantum de %.2f: T=%.2f, E=%.2f, P=%.2f" % (quantum,PROMT, PROME, PROMP))
    print("Orden de ejecución:", orden)


creacionProcesos()
FCFS()
ronda(2)

