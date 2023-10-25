import random
from collections import deque


def generar_carga_aleatoria():
    return random.randint(1, 10)  


def simular_procesos(procesos, quantum=None):
    tiempo_total = 0
    tiempo_espera_promedio = 0
    proceso_ordenado = sorted(procesos, key=lambda x: x[1])
    salida = ""
    
    if quantum is not None:
        cola = deque(proceso_ordenado)
    else:
        tiempo_espera = 0

    while proceso_ordenado:
        proceso = proceso_ordenado.pop(0)
        nombre, llegada, tiempo = proceso

        if quantum is not None:
            if tiempo > quantum:
                salida += nombre * quantum
                tiempo_total += quantum
                proceso_nuevo = (nombre, llegada, tiempo - quantum)
                proceso_ordenado.append(proceso_nuevo)
            else:
                salida += nombre * tiempo
                tiempo_total += tiempo
                tiempo_espera_promedio += tiempo_total - llegada
        else:
            salida += nombre * tiempo
            tiempo_total += tiempo
            tiempo_espera += tiempo_total - llegada

    tiempo_espera_promedio /= len(procesos)
    return tiempo_total, tiempo_espera_promedio, salida


rondas = [
    [('A', 0, 3), ('B', 1, 5), ('C', 3, 2), ('D', 9, 5), ('E', 12, 5)],
    [('A', 0, 5), ('B', 3, 3), ('C', 3, 7), ('D', 7, 4), ('E', 8, 4)]
]

for ronda in range(5):
    print(f"Ronda {ronda + 1}:")
    
   
    procesos = [(chr(65 + i), random.randint(0, 15), random.randint(1, 10)) for i in range(10)]
    
    tot_tiempo_total, tot_tiempo_espera, tot_salida = simular_procesos(procesos)
    print(f"FCFS: T={tot_tiempo_total:.1f}, E={tot_tiempo_espera:.1f}, P={tot_tiempo_espera / sum(p[2] for p in procesos):.2f}")

    for quantum in [1, 4]:
        rr_tiempo_total, rr_tiempo_espera, rr_salida = simular_procesos(procesos, quantum)
        print(f"RR{quantum}: T={rr_tiempo_total:.1f}, E={rr_tiempo_espera:.1f}, P={rr_tiempo_espera / sum(p[2] for p in procesos):.2f}")

    spn_tiempo_total, spn_tiempo_espera, spn_salida = simular_procesos(procesos)
    print(f"SPN: T={spn_tiempo_total:.1f}, E={spn_tiempo_espera:.1f}, P={spn_tiempo_espera / sum(p[2] for p in procesos):.2f}")

    print(f"Salida: {tot_salida}\n")

