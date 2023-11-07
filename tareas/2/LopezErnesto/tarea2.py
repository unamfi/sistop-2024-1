import random
"""
    Trabajo realizado por Ernesto Danjiro López Sugahara
    Fecha de entrega 26/10/2023
"""
# Cargas
# Carga predeterminada de la primera ronda:
# A: 0, t=3; B: 1, t=5; C: 3, t=2; D: 9, t=5; E: 12, t=5
# Total: 20
""" 
    Resultados esperados:
    FCFS: T=6.2, E=2.2, P=1.74
    RR1: T=7.6, E=3.6, P=1.98
    RR4: T=7.2, E=3.2, P=1.88
    SPN: T=5.6, E=1.6, P=1.32

    Tomar en cuenta las expresiones:

    T(t) -> Tiempo total para finalizar el proceso
    E(t) = T  - t -> Tiempo en espera
    P = T/t -> Proporción de penalización

    A: 0, t=5; B: 3, t=3; C: 3, t=7; D: 7, t=4; E:8, t=4 (tot:23)
"""
# tiempo_llegada - t - tiempo_restante - inicio - fin - T - E - P
administrador_procesos = {"A":[0,3,0,0,0,0,0,0],
                          "B":[1,5,0,0,0,0,0,0],
                          "C":[3,2,0,0,0,0,0,0],
                          "D":[9,5,0,0,0,0,0,0],
                          "E":[12,5,0,0,0,0,0,0]}

# tiempo_llegada - t - tiempo_restante - inicio - fin - T - E - P - n
pruebaFB =  {"A":[0,3,0,0,0,0,0,0,0],
             "B":[1,5,0,0,0,0,0,0,0],
             "C":[3,2,0,0,0,0,0,0,0],
             "D":[9,5,0,0,0,0,0,0,0],
             "E":[12,5,0,0,0,0,0,0,0]}

def FCFS(carga):
    resultados = {"T":0, "E":0, "P":0}
    # Se genera la cola inicial para la carga dada para el método RR:
    cola = []
    # Salida
    resultado_grafico = ""
    # Calculando el tiempo total de procesamiento:
    t_total = tiempoTotal(carga)
    # Agregamos todos aquellos procesos que entran al inicio
    for key,value in list(carga.items()):
        if value[0] == 0:
            cola.append(key)
            carga[key][2] = carga[key][1]
    tik = 0
    while tik < t_total:
        # Se trabaja el proceso
        if (len(cola) != 0): # Hay proceso activo
            carga[cola[0]][2] = carga[cola[0]][2] - 1  
            resultado_grafico += cola[0]
            if carga[cola[0]][2] == 0:
                # se terminó el proceso
                carga[cola[0]][4] = tik + 1
                # Se calculan los valores
                # Para T se tiene lo siguiente:
                carga[cola[0]][5] = carga[cola[0]][4] - carga[cola[0]][0]
                # Para E se tiene lo siguiente:
                carga[cola[0]][6] = carga[cola[0]][5] - carga[cola[0]][1]
                # Para P se tiene lo siguiente:
                carga[cola[0]][7] = carga[cola[0]][5]/carga[cola[0]][1]
                # Se elimina de la cola de procesos
                cola.pop(0)
        else:
            t_total += 1
        # Se tiene que revisar si llega un proceso
        for key,value in list(carga.items()):
            if value[0] == (tik + 1):
                cola.append(key)
                carga[key][2] = carga[key][1]
        tik += 1

    # Se calculan los resultados:
    for tiempos in carga.values():
        resultados["T"] += tiempos[5]
        resultados["E"] += tiempos[6]
        resultados["P"] += tiempos[7]
    # Se calcula el promedio para el número de procesos
    resultados['T'] /= len(carga)
    resultados['E'] /= len(carga)
    resultados['P'] /= len(carga)
    print(f"FCFS: T = {resultados['T']:0.2f}, E = {resultados['E']:0.2f}, P = {resultados['P']:0.2f}")
    print(resultado_grafico)

def RR(carga, quantum):
    resultados = {"T":0, "E":0, "P":0}
    # Se genera la cola inicial para la carga dada para el método RR:
    cola = []
    # Salida
    resultado_grafico = ""
    # Calculando el tiempo total de procesamiento:
    t_total = tiempoTotal(carga)
    # Conta_tik nos ayudará a determinar si ya pasó el quantum dado
    conta_tik = 0
    # Agregamos todos aquellos procesos que entran al inicio
    for key,value in list(carga.items()):
        if value[0] == 0:
            cola.append(key)
            carga[key][2] = carga[key][1]
    tik = 0
    while tik < t_total:
        # Se trabaja el proceso
        if (len(cola) != 0): # Hay proceso activo
            carga[cola[0]][2] = carga[cola[0]][2] - 1  
            resultado_grafico += cola[0]
            if carga[cola[0]][2] == 0:
                # se terminó el proceso
                carga[cola[0]][4] = tik + 1
                # Se calculan los valores
                # Para T se tiene lo siguiente:
                carga[cola[0]][5] = carga[cola[0]][4] - carga[cola[0]][0]
                # Para E se tiene lo siguiente:
                carga[cola[0]][6] = carga[cola[0]][5] - carga[cola[0]][1]
                # Para P se tiene lo siguiente:
                carga[cola[0]][7] = carga[cola[0]][5]/carga[cola[0]][1]
                # Se elimina de la cola de procesos
                cola.pop(0)
                conta_tik = 0
            else:
                # En caso contrario
                conta_tik += 1
        else:
            t_total += 1
        # Se tiene que revisar si llega un proceso
        for key,value in list(carga.items()):
            if value[0] == (tik + 1):
                cola.append(key)
                carga[key][2] = carga[key][1]
        
        # Se revisa el tiempo de trabajo del proceso actual con respecto a los quantums
        if conta_tik == quantum:
            cola.append(cola.pop(0))
            conta_tik = 0

        tik += 1

    # Se calculan los resultados:
    for tiempos in carga.values():
        resultados["T"] += tiempos[5]
        resultados["E"] += tiempos[6]
        resultados["P"] += tiempos[7]
    # Se calcula el promedio para el número de procesos
    resultados['T'] /= len(carga)
    resultados['E'] /= len(carga)
    resultados['P'] /= len(carga)
    print(f"RR{quantum}: T = {resultados['T']:0.2f}, E = {resultados['E']:0.2f}, P = {resultados['P']:0.2f}")
    print(resultado_grafico)

def SPN(carga):
    # En este caso, se tiene que ir dando paso al proceso más corto después de la finalización del actual
    # El primero siempre se ejecuta sin problemas
    resultados = {"T":0, "E":0, "P":0}
    # Se genera la cola inicial para la carga dada para el método RR:
    cola = []
    # Salida
    resultado_grafico = ""
    # Calculando el tiempo total de procesamiento:
    t_total = tiempoTotal(carga)
    # Agregamos todos aquellos procesos que entran al inicio (analizar cual es el más corto)
    for key,value in list(carga.items()):
        if value[0] == 0:
            cola.append(key)
            carga[key][2] = carga[key][1]
    if len(cola) != 0: 
        min = carga[cola[0]][1]
        for i,elemento in enumerate(cola):
            if carga[elemento][1] < min:
                cola.insert(0,cola.pop(i))
    # Se comienzan a desarrollar los procesos:
    tik = 0
    while tik < t_total:
        # Se trabaja el proceso
        if (len(cola) != 0):
            carga[cola[0]][2] = carga[cola[0]][2] - 1  
            resultado_grafico += cola[0]
        
            if carga[cola[0]][2] == 0:
                # se terminó el proceso
                carga[cola[0]][4] = tik + 1
                # Se calculan los valores
                # Para T se tiene lo siguiente:
                carga[cola[0]][5] = carga[cola[0]][4] - carga[cola[0]][0]
                # Para E se tiene lo siguiente:
                carga[cola[0]][6] = carga[cola[0]][5] - carga[cola[0]][1]
                # Para P se tiene lo siguiente:
                carga[cola[0]][7] = carga[cola[0]][5]/carga[cola[0]][1]
                # Se elimina de la cola de procesos
                cola.pop(0)
                # Se revisa si llega un proceso nuevo, y cual de los siguientes se debería de ejecutar
                for key,value in list(carga.items()):
                    if value[0] == (tik + 1):
                        cola.append(key)
                        carga[cola[len(cola) - 1]][2] = carga[cola[len(cola) - 1]][1]
                        # Se tiene que colocar al proceso más corto como el siguiente en la cola
                        min = carga[cola[0]][1]
                        for i,elemento in enumerate(cola):
                            if carga[elemento][1] < min:
                                cola.insert(0,cola.pop(i))
            else:
                # Se revisa si llega un proceso nuevo, los cuales se tienen que ordenar considerando su duración
                for key,value in list(carga.items()):
                    if value[0] == (tik + 1):
                        cola.append(key)
                        carga[cola[len(cola) - 1]][2] = carga[cola[len(cola) - 1]][1]
                        # Se tiene que colocar al proceso más corto como el siguiente en la cola
                        procesos_esperando = cola[1:]
                        min = carga[procesos_esperando[0]][1]
                        for i,elemento in enumerate(procesos_esperando):
                            if carga[elemento][1] < min:
                                procesos_esperando.insert(0,procesos_esperando.pop(i))
                        cola[1:] = procesos_esperando 
        else:
            t_total += 1
            # Se revisa si llega un proceso nuevo, los cuales se tienen que ordenar considerando su duración
            for key,value in list(carga.items()):
                if value[0] == (tik + 1):
                    cola.append(key)
                    carga[cola[len(cola) - 1]][2] = carga[cola[len(cola) - 1]][1]
        tik += 1


    # Se calculan los resultados:
    for tiempos in carga.values():
        resultados["T"] += tiempos[5]
        resultados["E"] += tiempos[6]
        resultados["P"] += tiempos[7]
    # Se calcula el promedio para el número de procesos
    resultados['T'] /= len(carga)
    resultados['E'] /= len(carga)
    resultados['P'] /= len(carga)
    print(f"SPN: T = {resultados['T']:0.2f}, E = {resultados['E']:0.2f}, P = {resultados['P']:0.2f}")
    print(resultado_grafico)

def FB(carga,n,num_colas):
    # En la primera ejecución, todos tendrán un quantum de ejecución, posteriormente se aplica q
    # Se coloca n para el número de ejecuciones para ser degradado a otra cola
    for proceso in list(carga.keys()):
        carga[proceso][8] = n
    # Se crean las colas de prioridad deseadas (0 máxima prioridad - n mínima)
    colas = []
    for _ in range(num_colas):
        colas.append(list())
    # Se guardarán los resultados en un diccionario
    resultados = {"T":0, "E":0, "P":0}

    # Bandera
    rotar = False
    # Salida
    resultado_grafico = ""
    # Calculando el tiempo total de procesamiento:
    t_total = tiempoTotal(carga)
    # Agregamos todos aquellos procesos que entran al inicio
    for key,value in list(carga.items()):
        if value[0] == 0:
            colas[0].append(key)
            carga[key][2] = carga[key][1]

    # Se lleva a cabo la administración de los procesos
    tik = 0
    while tik < t_total:
        # Se tiene que ir recorriendo cada cola para ver qué proceso debe de ser atendido
        for i in range(len(colas)):
            # Revisamos que cola es la que tiene un proceso en mayor prioridad
            if len(colas[i]) != 0: # Hay un proceso que tiene que ser atendido
                carga[colas[i][0]][2] = carga[colas[i][0]][2] - 1
                carga[colas[i][0]][8] = carga[colas[i][0]][8] - 1
                resultado_grafico += colas[i][0]
                # Se tiene que analizar dos cosas: 1) Se terminó el proceso 2) No se terminó y ya paso n veces en dicha cola 
                if carga[colas[i][0]][2] == 0:
                    # El proceso termino y se tiene que sacar de las colas
                    carga[colas[i][0]][4] = tik + 1
                    carga[colas[i][0]][5] = carga[colas[i][0]][4] - carga[colas[i][0]][0]
                    carga[colas[i][0]][6] = carga[colas[i][0]][5] - carga[colas[i][0]][1]
                    carga[colas[i][0]][7] = carga[colas[i][0]][5] / carga[colas[i][0]][1]
                    colas[i].pop(0)
                else:
                    # El proceso no ha terminado. Se tiene que analizar si se moverá a la siguiente cola
                    if carga[colas[i][0]][8] == 0:
                        # Si el proceso está en la cola de menor prioridad, se vuelve a encolar ahí mismo. En caso contrario, se mueve a 
                        # una cola superior
                        rotar = False
                        if i == len(colas) - 1:
                            # El proceso está en la cola de menor prioridad (ahí se queda)
                            carga[colas[i][0]][8] = n # Se reseta el número de ejecuciones
                            colas[i].append(colas[i].pop(0))
                        else:
                            carga[colas[i][0]][8] = n
                            colas[i + 1].append(colas[i].pop(0))
                    else:
                        rotar = True
                # Una vez analizados dichos casos, se sigue con la ejecución (analizar lo de los quantums)
                break
            if i == (len(colas) - 1):
                t_total += 1
    
        # Se tiene que revisar si llega un proceso
        for key,value in list(carga.items()):
            if value[0] == (tik + 1):
                # Se agrega le proceso a la cola de máxima prioridad
                colas[0].append(key)
                # Se ajusta el tiempo restante de ejecución del proceso 
                carga[colas[0][len(colas[0]) - 1]][2] = carga[colas[0][len(colas[0]) - 1]][1] 
        if rotar == True:
            colas[i].append(colas[i].pop(0))
            rotar = False
        tik += 1
        
        
    # Se calculan los resultados:
    for tiempos in carga.values():
        resultados["T"] += tiempos[5]
        resultados["E"] += tiempos[6]
        resultados["P"] += tiempos[7]
    # Se calcula el promedio para el número de procesos
    resultados['T'] /= len(carga)
    resultados['E'] /= len(carga)
    resultados['P'] /= len(carga)
    print(f"FB: T = {resultados['T']:0.2f}, E = {resultados['E']:0.2f}, P = {resultados['P']:0.2f}")
    print(resultado_grafico)

    # NOTA: No se considera la duración de los quantums.

def tiempoTotal(carga):
    tiempo = 0
    for t in list(carga.values()):
        tiempo += t[1]
    return tiempo

# Imprimimos la carga:
for key,value in administrador_procesos.items():
    print(f"{key}: {value[0]}, t = {value[1]}; ", end = "")
print()
print("Ronda 1:")
print("Realizando FCFS: ")
FCFS(administrador_procesos)
print("\n\nRealizando RR1: ")
RR(dict(administrador_procesos),1)
print("\n\nRealizando RR4: ")
RR(dict(administrador_procesos),4)
print("\n\nRealizando SPN: ")
SPN(dict(administrador_procesos))
print("\n\nRealizando FB: ")
FB(pruebaFB,1,5)

# Probando cargas aleatorias
contador = 0
while contador < 5:
    print("\n\n<-------------------------------------------->")
    print(f"Ronda {contador + 2}:")
    carga_aleatoria={"A":[random.randint(0,10),random.randint(1,10),0,0,0,0,0,0],
                     "B":[random.randint(0,10),random.randint(1,10),0,0,0,0,0,0],
                     "C":[random.randint(0,10),random.randint(1,10),0,0,0,0,0,0],
                     "D":[random.randint(0,10),random.randint(1,10),0,0,0,0,0,0],
                     "E":[random.randint(0,10),random.randint(1,10),0,0,0,0,0,0]}
    max = carga_aleatoria['A'][0]
    tiempo_total = tiempoTotal(carga_aleatoria)
    for key,value in carga_aleatoria.items():
        if value[0] > max:
            max = value[0]
    if max > tiempo_total:
        continue
    contador += 1
    # Imprimimos la carga:
    for key,value in carga_aleatoria.items():
        print(f"{key}: {value[0]}, t = {value[1]}; ", end = "")
    print()
    carga_aleatoria_fb=dict(carga_aleatoria)
    carga_aleatoria_fb['A'].append(0)
    carga_aleatoria_fb['B'].append(0)
    carga_aleatoria_fb['C'].append(0)
    carga_aleatoria_fb['D'].append(0)
    carga_aleatoria_fb['E'].append(0)
    print("Realizando FCFS: ")
    FCFS(carga_aleatoria)
    print("\n\nRealizando RR1: ")
    RR(dict(carga_aleatoria),1)
    print("\n\nRealizando RR4: ")
    RR(dict(carga_aleatoria),4)
    print("\n\nRealizando SPN: ")
    SPN(dict(carga_aleatoria))
    print("\n\nRealizando FB: ")
    FB(carga_aleatoria_fb,1,5)