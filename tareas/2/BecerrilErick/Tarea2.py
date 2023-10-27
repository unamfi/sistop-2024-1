# Tarea 2 "Comparacion de Planificadores"
# Becerril Martinez Erick Daniel
# Sistemas Operativos

import random
import numpy as np

class Proceso:
    def __init__(self, nombre, llegada, rafaga):
        self.nombre = nombre
        self.llegada = llegada
        self.rafaga = rafaga
        self.tiempo_espera = 0
        self.tiempo_respuesta = -1

# Función para generar una lista de procesos aleatorios
def generar_procesos(num_procesos):
    procesos = []
    for i in range(num_procesos):
        nombre = chr(65 + i)  # Generar nombres de proceso (A, B, C, ...)
        llegada = random.randint(0, 15)  # Tiempo de llegada aleatorio
        rafaga = random.randint(1, 10)  # Ráfaga de CPU aleatoria
        procesos.append(Proceso(nombre, llegada, rafaga))
    return procesos

# Algoritmo de planificación FCFS (First-Come, First-Served)
def fcfs(procesos):
    tiempo_total = 0
    tiempo_espera_total = 0
    tiempo_respuesta_total = 0
    
    for proceso in procesos:
        if tiempo_total < proceso.llegada:
            tiempo_total = proceso.llegada
        proceso.tiempo_respuesta = tiempo_total - proceso.llegada
        proceso.tiempo_espera = tiempo_total - proceso.llegada
        tiempo_total += proceso.rafaga
        tiempo_espera_total += proceso.tiempo_espera
        tiempo_respuesta_total += proceso.tiempo_respuesta
    
    promedio_tiempo_espera = tiempo_espera_total / len(procesos)
    promedio_tiempo_respuesta = tiempo_respuesta_total / len(procesos)
    
    return tiempo_total, promedio_tiempo_espera, promedio_tiempo_respuesta

# Algoritmo de planificación Round Robin (con quantum)
def round_robin(procesos, quantum):
    tiempo_total = 0
    tiempo_espera_total = 0
    tiempo_respuesta_total = 0
    cola = list(procesos)
    
    while cola:
        proceso = cola.pop(0)
        if proceso.tiempo_respuesta == -1:
            proceso.tiempo_respuesta = tiempo_total - proceso.llegada
        if proceso.rafaga <= quantum:
            tiempo_total += proceso.rafaga
            proceso.rafaga = 0
            tiempo_espera_total += tiempo_total - proceso.llegada - proceso.tiempo_respuesta
        else:
            tiempo_total += quantum
            proceso.rafaga -= quantum
            cola.append(proceso)
    
    promedio_tiempo_espera = tiempo_espera_total / len(procesos)
    promedio_tiempo_respuesta = promedio_tiempo_espera  # En RR, el tiempo de respuesta es igual al tiempo de espera
    
    return tiempo_total, promedio_tiempo_espera, promedio_tiempo_respuesta

# Algoritmo de planificación SPN (Shortest Process Next)
def spn(procesos):
    tiempo_total = 0
    tiempo_espera_total = 0
    tiempo_respuesta_total = 0
    
    procesos.sort(key=lambda x: x.rafaga)
    
    for proceso in procesos:
        if tiempo_total < proceso.llegada:
            tiempo_total = proceso.llegada
        proceso.tiempo_respuesta = tiempo_total - proceso.llegada
        proceso.tiempo_espera = tiempo_total - proceso.llegada
        tiempo_total += proceso.rafaga
        tiempo_espera_total += proceso.tiempo_espera
        tiempo_respuesta_total += proceso.tiempo_respuesta
    
    promedio_tiempo_espera = tiempo_espera_total / len(procesos)
    promedio_tiempo_respuesta = tiempo_respuesta_total / len(procesos)
    
    return tiempo_total, promedio_tiempo_espera, promedio_tiempo_respuesta

# Función para simular y mostrar los resultados de un algoritmo de planificación
def simular(planificador, procesos, nombre, quantum=None):
    if quantum is not None:
        tiempo_total, promedio_tiempo_espera, promedio_tiempo_respuesta = planificador(procesos, quantum)
    else:
        tiempo_total, promedio_tiempo_espera, promedio_tiempo_respuesta = planificador(procesos)
    print(f"{nombre}: T={tiempo_total/len(procesos):.2f}, E={promedio_tiempo_espera:.2f}, P={promedio_tiempo_respuesta:.2f}")

# Función principal
def main():
    random.seed(0)
    
    rondas = 5  # Número de rondas
    for ronda in range(1, rondas+1):
        print(f"Ronda {ronda}:")
        procesos = generar_procesos(5)  # Generar 5 procesos aleatorios en cada ronda
        for proceso in procesos:
            print(f"{proceso.nombre}: {proceso.llegada}, t={proceso.rafaga};", end=' ')
        print(f"(tot:{sum(proceso.rafaga for proceso in procesos)})")
    
        simular(fcfs, list(procesos), "FCFS")
        simular(round_robin, list(procesos), "RR1", 1)  # Define el quantum aquí (en este caso, 1)
        simular(round_robin, list(procesos), "RR4", 4)  # Define el quantum aquí (en este caso, 4)
        simular(spn, list(procesos), "SPN")
        print()

if __name__ == "__main__":
    main()


