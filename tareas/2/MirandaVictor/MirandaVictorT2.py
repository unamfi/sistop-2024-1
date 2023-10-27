# Miranda Barajas Victor
import random
import collections

# Generar cargas aleatorias
def generar_cargas(num_procesos):
    return [(i, random.randint(1, 10)) for i in range(num_procesos)]

# Implementación de FCFS
def fcfs(cargas):
    tiempo_espera = 0
    tiempo_retorno = 0
    for i in range(len(cargas)):
        tiempo_espera += sum(carga[1] for carga in cargas[:i])
        tiempo_retorno += sum(carga[1] for carga in cargas[:i + 1])
    T = tiempo_retorno / len(cargas)
    E = tiempo_espera / len(cargas)
    P = T / (sum(carga[1] for carga in cargas) / len(cargas))
    return T, E, P

# Implementación de Round Robin
def round_robin(cargas, quantum):
    num_procesos = len(cargas)
    tiempo_total_ejecucion = sum(carga[1] for carga in cargas)
    cargas = collections.deque(cargas)
    tiempo_espera = 0
    tiempo_retorno = 0
    tiempo_transcurrido = 0
    while cargas:
        proceso, tiempo_restante = cargas.popleft()
        if tiempo_restante > quantum:
            tiempo_transcurrido += quantum
            cargas.append((proceso, tiempo_restante - quantum))
        else:
            tiempo_transcurrido += tiempo_restante
            tiempo_retorno += tiempo_transcurrido
            tiempo_espera += tiempo_transcurrido - tiempo_restante
    T = tiempo_retorno / num_procesos
    E = tiempo_espera / num_procesos
    P = T / (tiempo_total_ejecucion / num_procesos)
    return T, E, P

# Implementación de SPN
def spn(cargas):
    cargas.sort(key=lambda carga: carga[1])
    return fcfs(cargas)

# Ejecución y comparación
for i in range(5):  # 5 ejecuciones
    cargas = generar_cargas(20)  # Asumiendo 20 procesos
    print(f'Ejecución {i + 1}')
    print('FCFS:', fcfs(cargas))
    print('RR1:', round_robin(cargas, 1))
    print('RR4:', round_robin(cargas, 4))
    print('SPN:', spn(cargas))

