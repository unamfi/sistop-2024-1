import random

# Definir una lista de procesos con tiempos de llegada y ráfagas de CPU aleatorios
def generar_procesos(num_procesos):
    procesos = []
    for i in range(num_procesos):
        proceso = {
            'nombre': chr(ord('A') + i),
            'llegada': random.randint(0, 10),
            'rafaga': random.randint(1, 10)
        }
        procesos.append(proceso)
    return procesos

# Implementar algoritmos de planificación
def planificacion_fcfs(procesos):
    tiempo_total = 0
    tiempo_espera = 0
    tiempo_respuesta = 0
    for proceso in procesos:
        tiempo_total += proceso['rafaga']
        tiempo_espera += max(0, tiempo_total - proceso['llegada'] - proceso['rafaga'])
        tiempo_respuesta += max(0, tiempo_total - proceso['llegada'])
    promedio_tiempo_total = tiempo_total / len(procesos)
    promedio_tiempo_espera = tiempo_espera / len(procesos)
    promedio_tiempo_respuesta = tiempo_respuesta / len(procesos)
    return promedio_tiempo_total, promedio_tiempo_espera, promedio_tiempo_respuesta

# Implementar Round-Robin con diferentes tamaños de quantum
def planificacion_rr(procesos, quantum):
    tiempo_total = 0
    tiempo_espera = 0
    tiempo_respuesta = 0
    procesos_restantes = list(procesos)
    while procesos_restantes:
        proceso = procesos_restantes.pop(0)
        tiempo_total += min(quantum, proceso['rafaga'])
        proceso['rafaga'] -= min(quantum, proceso['rafaga'])
        if proceso['rafaga'] > 0:
            procesos_restantes.append(proceso)
        tiempo_respuesta += max(0, tiempo_total - proceso['llegada'])
        for otro_proceso in procesos_restantes:
            if otro_proceso != proceso:
                tiempo_espera += min(quantum, otro_proceso['rafaga'])
    promedio_tiempo_total = tiempo_total / len(procesos)
    promedio_tiempo_espera = tiempo_espera / len(procesos)
    promedio_tiempo_respuesta = tiempo_respuesta / len(procesos)
    return promedio_tiempo_total, promedio_tiempo_espera, promedio_tiempo_respuesta

# Implementar Shortest Process Next
def planificacion_spn(procesos):
    tiempo_total = 0
    tiempo_espera = 0
    tiempo_respuesta = 0
    procesos_ordenados = sorted(procesos, key=lambda x: x['rafaga'])
    for proceso in procesos_ordenados:
        tiempo_total += proceso['rafaga']
        tiempo_espera += max(0, tiempo_total - proceso['llegada'] - proceso['rafaga'])
        tiempo_respuesta += max(0, tiempo_total - proceso['llegada'])
    promedio_tiempo_total = tiempo_total / len(procesos)
    promedio_tiempo_espera = tiempo_espera / len(procesos)
    promedio_tiempo_respuesta = tiempo_respuesta / len(procesos)
    return promedio_tiempo_total, promedio_tiempo_espera, promedio_tiempo_respuesta

# Ejecutar múltiples rondas y mostrar resultados
num_rondas = 5
num_procesos = 5

for ronda in range(num_rondas):
    procesos = generar_procesos(num_procesos)
    
    print(f"Ronda {ronda + 1}:")
    for proceso in procesos:
        print(f"{proceso['nombre']}: Llegada={proceso['llegada']}, Rafaga={proceso['rafaga']}")
    
    tiempo_fcfs, espera_fcfs, respuesta_fcfs = planificacion_fcfs(procesos)
    tiempo_rr1, espera_rr1, respuesta_rr1 = planificacion_rr(procesos, 1)
    tiempo_rr4, espera_rr4, respuesta_rr4 = planificacion_rr(procesos, 4)
    tiempo_spn, espera_spn, respuesta_spn = planificacion_spn(procesos)
    
    print("FCFS: T={:.2f}, E={:.2f}, P={:.2f}".format(tiempo_fcfs, espera_fcfs, respuesta_fcfs))
    print("RR1: T={:.2f}, E={:.2f}, P={:.2f}".format(tiempo_rr1, espera_rr1, respuesta_rr1))
    print("RR4: T={:.2f}, E={:.2f}, P={:.2f}".format(tiempo_rr4, espera_rr4, respuesta_rr4))
    print("SPN: T={:.2f}, E={:.2f}, P={:.2f}".format(tiempo_spn, espera_spn, respuesta_spn))
    print()
