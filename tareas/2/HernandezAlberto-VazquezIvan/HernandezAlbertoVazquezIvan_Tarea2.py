import random
from collections import deque

class Proceso:
    def __init__(self, nombre, tiempo_llegada, tiempo_ejecucion):
        self.nombre = nombre
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_ejecucion = tiempo_ejecucion

def generar_procesos(num_procesos, max_tiempo_ejecucion):
    procesos = []
    for i in range(num_procesos):
        nombre = chr(65 + i)  # Usar letras del alfabeto, comenzando desde 'A'
        tiempo_llegada = random.randint(0, num_procesos * 2)
        tiempo_ejecucion = random.randint(1, max_tiempo_ejecucion)
        procesos.append(Proceso(nombre, tiempo_llegada, tiempo_ejecucion))
    return procesos

def calcular_metricas(resultados, tiempo_llegada):
    tiempo_respuesta_total = sum(tiempo_espera + proceso.tiempo_ejecucion for proceso, tiempo_espera in resultados)
    tiempo_espera_promedio = tiempo_respuesta_total - tiempo_llegada
    proporcion_penalizacion = tiempo_respuesta_total / tiempo_llegada
    return tiempo_respuesta_total, tiempo_espera_promedio, proporcion_penalizacion

def fifo(procesos):
    cola = deque(procesos)
    tiempo_actual = 0
    resultados = []
    while cola:
        proceso = cola.popleft()
        tiempo_espera = max(0, tiempo_actual - proceso.tiempo_llegada)
        resultados.append((proceso, tiempo_espera))
        tiempo_actual += proceso.tiempo_ejecucion
    return resultados

def round_robin(procesos, quantum):
    cola = deque(procesos)
    tiempo_actual = 0
    resultados = []
    while cola:
        proceso = cola.popleft()
        tiempo_espera = max(0, tiempo_actual - proceso.tiempo_llegada)
        tiempo_ejecucion = min(quantum, proceso.tiempo_ejecucion)
        resultados.append((proceso, tiempo_espera))
        proceso.tiempo_ejecucion -= tiempo_ejecucion
        if proceso.tiempo_ejecucion > 0:
            cola.append(proceso)
        tiempo_actual += tiempo_ejecucion
    return resultados

def spn(procesos):
    procesos_ordenados = sorted(procesos, key=lambda p: p.tiempo_ejecucion)
    tiempo_actual = 0
    resultados = []
    for proceso in procesos_ordenados:
        tiempo_espera = max(0, tiempo_actual - proceso.tiempo_llegada)
        resultados.append((proceso, tiempo_espera))
        tiempo_actual += proceso.tiempo_ejecucion
    return resultados

def mostrar_comparaciones(ejecucion, procesos, resultados_fifo, resultados_rr, resultados_spn, tiempo_llegada):
    print(f"Ejecución {ejecucion}:")

    print("Procesos generados:")
    print("".join([proceso.nombre for proceso in procesos]))

    print("FCFS:", end=" ")
    tiempo_respuesta, tiempo_espera_promedio, proporcion_penalizacion = calcular_metricas(resultados_fifo, tiempo_llegada)
    for proceso, tiempo_espera in resultados_fifo:
        print(f"{proceso.nombre}", end="")
    print()
    print(f"T={tiempo_respuesta:.1f}, E={tiempo_espera_promedio:.1f}, P={proporcion_penalizacion:.2f}")

    print("Round Robin:", end=" ")
    tiempo_respuesta, tiempo_espera_promedio, proporcion_penalizacion = calcular_metricas(resultados_rr, tiempo_llegada)
    for proceso, tiempo_espera in resultados_rr:
        print(f"{proceso.nombre}", end="")
    print()
    print(f"T={tiempo_respuesta:.1f}, E={tiempo_espera_promedio:.1f}, P={proporcion_penalizacion:.2f}")

    print("SPN:", end=" ")
    tiempo_respuesta, tiempo_espera_promedio, proporcion_penalizacion = calcular_metricas(resultados_spn, tiempo_llegada)
    for proceso, tiempo_espera in resultados_spn:
        print(f"{proceso.nombre}", end="")
    print()
    print(f"T={tiempo_respuesta:.1f}, E={tiempo_espera_promedio:.1f}, P={proporcion_penalizacion:.2f}")

    print("\n---\n")

def main():
    num_procesos = 10
    max_tiempo_ejecucion = 10
    quantum = 2

    for ejecucion in range(1, 6):
        procesos = generar_procesos(num_procesos, max_tiempo_ejecucion)

        resultados_fifo = fifo(procesos)
        resultados_rr = round_robin(procesos, quantum)
        resultados_spn = spn(procesos)

        tiempo_llegada = sum(proceso.tiempo_llegada for proceso in procesos)

        mostrar_comparaciones(ejecucion, procesos, resultados_fifo, resultados_rr, resultados_spn, tiempo_llegada)

if __name__ == "__main__":
    main()