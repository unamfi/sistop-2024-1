import random

def listaProcesos(num_de_procesos=5):
    nombres_procesos = ['A', 'B', 'C', 'D', 'E']
    llegada = 0
    procesos = []

    for i in range(num_de_procesos):
        nombre = nombres_procesos[i]
        duracion = random.randint(1, 5)
        procesos.append([nombre, llegada, duracion])
        llegada += random.randint(0, duracion - 1)

    return procesos

def calcular_metricas(cola_procesos):
    l = len(cola_procesos)
    t = [cola_procesos[i][2] for i in range(l)]
    T = [0 for i in range(l)]
    E = [0 for i in range(l)]
    P = [0 for i in range(l)]
    End = [0 for i in range(l)]

    for i in range(l):
        if i == 0:
            End[i] = cola_procesos[i][2]
        else:
            End[i] = max(cola_procesos[i][1], End[i - 1]) + cola_procesos[i][2]

        T[i] = End[i] - cola_procesos[i][1]
        E[i] = T[i] - cola_procesos[i][2]
        P[i] = T[i] / cola_procesos[i][2]

    return T, E, P

def imprimir_metricas(averageT, averageE, averageP, nombre_algoritmo):
    print(f'{nombre_algoritmo}: T = {averageT:.2f}\tE = {averageE:.2f}\tP = {averageP:.2f}')

def FCFS(cola_procesos):
    T, E, P = calcular_metricas(cola_procesos)
    averageT = sum(T) / len(T)
    averageE = sum(E) / len(E)
    averageP = sum(P) / len(P)
    imprimir_metricas(averageT, averageE, averageP, 'FCFS')

def RR1(cola_procesos):
    l = len(cola_procesos)
    cola_procesos_procesados = []
    t = [cola_procesos[i][2] for i in range(l)]
    T, E, P = calcular_metricas(cola_procesos)
    output = ''
    tiempo_actual = 0

    while any(tiempo != 0 for tiempo in t):
        for i in range(len(t)):
            if t[i] >= 1 and tiempo_actual >= cola_procesos[i][1]:
                cola_procesos_procesados.append(cola_procesos[i][0])
                output += cola_procesos[i][0]
                t[i] -= 1
                tiempo_actual += 1

    averageT = sum(T) / len(T)
    averageE = sum(E) / len(E)
    averageP = sum(P) / len(P)
    imprimir_metricas(averageT, averageE, averageP, 'RR1')
    print(output)

def RR4(cola_procesos):
    l = len(cola_procesos)
    cola_procesos_procesados = []
    t = [cola_procesos[i][2] for i in range(l)]
    T, E, P = calcular_metricas(cola_procesos)
    output = ''
    tiempo_actual = 0

    while any(tiempo != 0 for tiempo in t):
        for i in range(len(t)):
            if t[i] >= 4 and tiempo_actual >= cola_procesos[i][1]:
                for j in range(4):
                    cola_procesos_procesados.append(cola_procesos[i][0])
                    output += cola_procesos[i][0]
                tiempo_actual += 4
                t[i] -= 4
            elif t[i] < 4 and t[i] > 0 and tiempo_actual >= cola_procesos[i][1]:
                for j in range(t[i]):
                    cola_procesos_procesados.append(cola_procesos[i][0])
                    output += cola_procesos[i][0]
                tiempo_actual += t[i]
                t[i] = 0

    averageT = sum(T) / len(T)
    averageE = sum(E) / len(E)
    averageP = sum(P) / len(P)
    imprimir_metricas(averageT, averageE, averageP, 'RR4')
    print(output)

def spn(cola_procesos):
    cola_procesos.sort(key=lambda x: x[2])
    T, E, P = calcular_metricas(cola_procesos)
    averageT = sum(T) / len(T)
    averageE = sum(E) / len(E)
    averageP = sum(P) / len(P)
    output = ''.join([proceso[0] for proceso in cola_procesos])
    imprimir_metricas(averageT, averageE, averageP, 'SPN')
    print(output)

rondas = random.randint(1, 5)

for i in range(rondas):
    cola_procesos = listaProcesos()
    print(f'\nRonda Numero: {i+1}')
    print(f'Cola de Procesos: {cola_procesos}')
    FCFS(cola_procesos)
    RR1(cola_procesos)
    RR4(cola_procesos)
    spn(cola_procesos)