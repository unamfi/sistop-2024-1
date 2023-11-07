import random

# Función para calcular el tiempo de finalización promedio
def calcular_tiempo_promedio_finalizacion(tiempo_finalizacion):
    return sum(tiempo_finalizacion) / len(tiempo_finalizacion)

# Función para calcular el tiempo de espera promedio
def calcular_tiempo_promedio_espera(tiempo_espera):
    return sum(tiempo_espera) / len(tiempo_espera)

# Función para calcular la proporción de penalización promedio
def calcular_proporcion_penalizacion_promedio(tiempo_finalizacion, tiempo_ráfaga):
    proporciones_penalizacion = [tiempo_finalizacion / tiempo_ráfaga for tiempo_finalizacion, tiempo_ráfaga in zip(tiempo_finalizacion, tiempo_ráfaga)]
    return sum(proporciones_penalizacion) / len(proporciones_penalizacion)

# Algoritmo de planificación FCFS
def fcfs(procesos, tiempo_ráfaga):
    n = len(procesos)
    tiempo_finalizacion = [0] * n
    tiempo_espera = [0] * n
    tiempo_retorno = [0] * n
    proporcion_penalizacion = [0] * n

    for i in range(1, n):
        tiempo_finalizacion[i] = tiempo_finalizacion[i - 1] + tiempo_ráfaga[i - 1]
        tiempo_retorno[i] = tiempo_finalizacion[i] - 0
        tiempo_espera[i] = tiempo_retorno[i] - tiempo_ráfaga[i]
        proporcion_penalizacion[i] = tiempo_retorno[i] / tiempo_ráfaga[i]

    tiempo_promedio_retorno = calcular_tiempo_promedio_finalizacion(tiempo_retorno)
    tiempo_promedio_espera = calcular_tiempo_promedio_espera(tiempo_espera)
    proporcion_penalizacion_promedio = calcular_proporcion_penalizacion_promedio(proporcion_penalizacion, tiempo_ráfaga)

    return tiempo_promedio_retorno, tiempo_promedio_espera, proporcion_penalizacion_promedio

# Algoritmo de planificación Round Robin (RR)
def round_robin(procesos, tiempo_ráfaga, quantum_de_tiempo):
    n = len(procesos)
    tiempo_finalizacion = [0] * n
    tiempo_espera = [0] * n
    tiempo_retorno = [0] * n
    proporcion_penalizacion = [0] * n

    tiempo_remanente = list(tiempo_ráfaga)
    tiempo_actual = 0

    while sum(tiempo_remanente) > 0:
        for i in range(n):
            if tiempo_remanente[i] > 0:
                if tiempo_remanente[i] > quantum_de_tiempo:
                    tiempo_actual += quantum_de_tiempo
                    tiempo_remanente[i] -= quantum_de_tiempo
                else:
                    tiempo_actual += tiempo_remanente[i]
                    tiempo_finalizacion[i] = tiempo_actual
                    tiempo_retorno[i] = tiempo_finalizacion[i] - 0
                    tiempo_espera[i] = tiempo_retorno[i] - tiempo_ráfaga[i]
                    proporcion_penalizacion[i] = tiempo_retorno[i] / tiempo_ráfaga[i]
                    tiempo_remanente[i] = 0

    tiempo_promedio_retorno = calcular_tiempo_promedio_finalizacion(tiempo_retorno)
    tiempo_promedio_espera = calcular_tiempo_promedio_espera(tiempo_espera)
    proporcion_penalizacion_promedio = calcular_proporcion_penalizacion_promedio(proporcion_penalizacion, tiempo_ráfaga)

    return tiempo_promedio_retorno, tiempo_promedio_espera, proporcion_penalizacion_promedio

# Algoritmo de planificación Shortest Job Next (SPN)
def spn(procesos, tiempo_ráfaga):
    n = len(procesos)
    tiempo_finalizacion = [0] * n
    tiempo_espera = [0] * n
    tiempo_retorno = [0] * n
    proporcion_penalizacion = [0] * n

    tiempo_remanente = list(tiempo_ráfaga)
    procesos_remanentes = list(range(n))

    for i in range(n):
        indice_minimo = min(procesos_remanentes, key=lambda x: tiempo_remanente[x])
        tiempo_finalizacion[indice_minimo] = tiempo_finalizacion[i] + tiempo_ráfaga[indice_minimo]
        tiempo_retorno[indice_minimo] = tiempo_finalizacion[indice_minimo] - 0
        tiempo_espera[indice_minimo] = tiempo_retorno[indice_minimo] - tiempo_ráfaga[indice_minimo]
        proporcion_penalizacion[indice_minimo] = tiempo_retorno[indice_minimo] / tiempo_ráfaga[indice_minimo]
        procesos_remanentes.remove(indice_minimo)

    tiempo_promedio_retorno = calcular_tiempo_promedio_finalizacion(tiempo_retorno)
    tiempo_promedio_espera = calcular_tiempo_promedio_espera(tiempo_espera)
    proporcion_penalizacion_promedio = calcular_proporcion_penalizacion_promedio(proporcion_penalizacion, tiempo_ráfaga)

    return tiempo_promedio_retorno, tiempo_promedio_espera, proporcion_penalizacion_promedio

# Algoritmo de planificación Feedback (FB)
def feedback(procesos, tiempo_ráfaga, quantum_de_tiempo, num_niveles):
    n = len(procesos)
    colas = [[] for _ in range(num_niveles)]
    tiempo_finalizacion = [0] * n
    tiempo_espera = [0] * n
    tiempo_retorno = [0] * n
    proporcion_penalizacion = [0] * n

    for i in range(n):
        colas[0].append(i)

    tiempo_actual = 0
    nivel = 0

    while any(colas):
        if not colas[nivel]:
            # Si la cola actual está vacía, pasa a la siguiente cola
            nivel = (nivel + 1) % num_niveles
            continue

        indice_proceso = colas[nivel][0]
        tiempo_ráfaga_proceso = tiempo_ráfaga[indice_proceso]

        if tiempo_ráfaga_proceso <= quantum_de_tiempo:
            tiempo_actual += tiempo_ráfaga_proceso
            tiempo_finalizacion[indice_proceso] = tiempo_actual
            tiempo_retorno[indice_proceso] = tiempo_finalizacion[indice_proceso]
            tiempo_espera[indice_proceso] = tiempo_retorno[indice_proceso] - tiempo_ráfaga_proceso
            proporcion_penalizacion[indice_proceso] = tiempo_retorno[indice_proceso] / tiempo_ráfaga_proceso
            colas[nivel].pop(0)
        else:
            tiempo_actual += quantum_de_tiempo
            tiempo_ráfaga[indice_proceso] -= quantum_de_tiempo
            # Mueve el proceso a la siguiente cola
            nivel = (nivel + 1) % num_niveles
            colas[nivel].append(indice_proceso)

    tiempo_promedio_retorno = calcular_tiempo_promedio_finalizacion(tiempo_retorno)
    tiempo_promedio_espera = calcular_tiempo_promedio_espera(tiempo_espera)
    proporcion_penalizacion_promedio = calcular_proporcion_penalizacion_promedio(proporcion_penalizacion, tiempo_ráfaga)

    return tiempo_promedio_retorno, tiempo_promedio_espera, proporcion_penalizacion_promedio

# Función para generar una carga aleatoria
def generar_tiempo_ráfaga_aleatorio(num_procesos, tiempo_ráfaga_maximo):
    return [random.randint(1, tiempo_ráfaga_maximo) for _ in range(num_procesos)]

def main():
    num_procesos = 20
    tiempo_ráfaga_maximo = 10
    quantum_de_tiempo = 4
    num_niveles = 4

    for ronda in range(5):
        procesos = [chr(65 + i) for i in range(num_procesos)]
        random.shuffle(procesos)  # Baraja la lista de procesos aleatoriamente

        tiempo_ráfaga = generar_tiempo_ráfaga_aleatorio(num_procesos, tiempo_ráfaga_maximo)

        print(f"Ronda {ronda + 1}:")
        print("Carga generada:", ''.join(procesos))
        print("\n")
        print("FCFS: ", end='')
        tiempo_promedio_retorno, tiempo_promedio_espera, proporcion_penalizacion_promedio = fcfs(procesos, tiempo_ráfaga)
        print(f"T={tiempo_promedio_retorno:.1f}, E={tiempo_promedio_espera:.1f}, P={proporcion_penalizacion_promedio:.2f}")

        print("RR1: ", end='')
        tiempo_promedio_retorno, tiempo_promedio_espera, proporcion_penalizacion_promedio = round_robin(procesos, tiempo_ráfaga, 1)
        print(f"T={tiempo_promedio_retorno:.1f}, E={tiempo_promedio_espera:.1f}, P={proporcion_penalizacion_promedio:.2f}")

        print("RR4: ", end='')
        tiempo_promedio_retorno, tiempo_promedio_espera, proporcion_penalizacion_promedio = round_robin(procesos, tiempo_ráfaga, 4)
        print(f"T={tiempo_promedio_retorno:.1f}, E={tiempo_promedio_espera:.1f}, P={proporcion_penalizacion_promedio:.2f}")

        print("SPN: ", end='')
        tiempo_promedio_retorno, tiempo_promedio_espera, proporcion_penalizacion_promedio = spn(procesos, tiempo_ráfaga)
        print(f"T={tiempo_promedio_retorno:.1f}, E={tiempo_promedio_espera:.1f}, P={proporcion_penalizacion_promedio:.2f}")

        print("FB: ", end='')
        tiempo_promedio_retorno, tiempo_promedio_espera, proporcion_penalizacion_promedio = feedback(procesos, tiempo_ráfaga, quantum_de_tiempo, num_niveles)
        print(f"T={tiempo_promedio_retorno:.1f}, E={tiempo_promedio_espera:.1f}, P={proporcion_penalizacion_promedio:.2f}")

        print("Se realizaron los cálculos \n")

if __name__ == "__main__":
    main()
