from random import randint

def generar_procesos(procesos, n, p, tmin, tmax):
    t = 0
    nombre_ascii = 65 

    while n > 0:
        if randint(0, p-1) == 0:
            proceso = [t, randint(tmin, tmax), chr(nombre_ascii), 0, 0, 0, ""]
            procesos.append(proceso)
            nombre_ascii += 1
            n -= 1
        t += 1

def calcular_resultados(lista_tareas):
    for i in lista_tareas:
        i[4] = i[3] - i[1]
        i[5] = i[3] / i[1]

def calcular_promedios(lista_tareas):
    total_t = total_e = total_p = 0

    for i in lista_tareas:
        total_t += i[3]
        total_e += i[4]
        total_p += i[5]

    return total_t/len(lista_tareas), total_e/len(lista_tareas), total_p/len(lista_tareas)

def mostrar_tabla(lista_tareas, algoritmo):
    print("\n"+algoritmo)
    promedio_t, promedio_e, promedio_p = calcular_promedios(lista_tareas)
    print('Proceso\tt\tInicio\tFin\tT\tE\tP')

    for i in lista_tareas:
        print(f"{i[2]}\t{i[1]}\t{i[0]}\t{i[0]+i[3]}\t{i[3]}\t{i[4]}\t{i[5]}")

    print(f"Promedio:\t\t\tT={promedio_t}\tE={promedio_e}\tP={promedio_p}")

def mostrar_diagrama(lista_tareas):
    print("\nDiagrama: ")
    for i in lista_tareas:
        print((" " * i[0]) + i[6])

def fcfs(tareas):
    tareas_entrada = [proceso.copy() for proceso in tareas]
    t = 0
    esquema = ""
    tareas_cola = []
    tareas_entrada_ite = 0
    tareas_cola_ite = 0

    while tareas_entrada_ite < len(tareas_entrada) or len(tareas_cola) != 0:
        if tareas_entrada_ite < len(tareas_entrada):
            if tareas_entrada[tareas_entrada_ite][0] == t:
                tareas_cola.append(tareas_entrada[tareas_entrada_ite].copy())
                tareas_entrada_ite += 1

        if len(tareas_cola) > 0:
            esquema = esquema + tareas_cola[0][2] 
            for i in tareas_cola:
                i[3] += 1
            tareas_cola[0][1] -= 1
            tareas_cola[0][6] = tareas_cola[0][6] + tareas_cola[0][2]

            for i in range(1, len(tareas_cola)):
                tareas_cola[i][6] = tareas_cola[i][6] + '-'

            if tareas_cola[0][1] == 0:
                tareas_entrada[tareas_cola_ite][3] = tareas_cola[0][3]
                tareas_entrada[tareas_cola_ite][6] = tareas_cola[0][6]
                tareas_cola_ite += 1
                tareas_cola.pop(0) 
        else:
            esquema = esquema + "i"

        t += 1

    calcular_resultados(tareas_entrada)
    mostrar_tabla(tareas_entrada, "FCFS")
    mostrar_diagrama(tareas_entrada)
    print("ESQUEMA:")
    print(esquema)

def round_robin_n(tareas, n):
    tareas_entrada = [proceso.copy() for proceso in tareas]
    t = 0
    esquema = ""
    tareas_cola = []
    tareas_entrada_ite = 0
    quantum = n
    encolar = None

    while tareas_entrada_ite < len(tareas_entrada) or len(tareas_cola) != 0 or encolar is not None:
        if tareas_entrada_ite < len(tareas_entrada):
            if tareas_entrada[tareas_entrada_ite][0] == t:
                tareas_cola.append(tareas_entrada[tareas_entrada_ite].copy())
                tareas_entrada_ite += 1

        if len(tareas_cola) > 0:
            esquema = esquema + tareas_cola[0][2]
            for i in tareas_cola:
                i[3] += 1 
            tareas_cola[0][1] -= 1
            quantum -= 1

            tareas_cola[0][6] = tareas_cola[0][6] + tareas_cola[0][2]
            for i in range(1, len(tareas_cola)):
                tareas_cola[i][6] = tareas_cola[i][6] + '-'

            if tareas_cola[0][1] == 0:
                nombre = tareas_cola[0][2]
                for i in range(len(tareas_entrada)):
                    if tareas_entrada[i][2] == nombre:
                        tareas_entrada[i][3] = tareas_cola[0][3]
                        tareas_entrada[i][6] = tareas_cola[0][6]
                        break
                tareas_cola_ite += 1
                tareas_cola.pop(0)
                quantum = n 
            elif quantum == 0:
                encolar = tareas_cola.pop(0)
                quantum = n
        else:
            esquema = esquema + "i"

        t += 1

    calcular_resultados(tareas_entrada)
    mostrar_tabla(tareas_entrada, "RR" + str(n))
    mostrar_diagrama(tareas_entrada)
    print("\nESQUEMA:")
    print(esquema)

def shortest_process_next(tareas):
    tareas_entrada = [proceso.copy() for proceso in tareas]
    t = 0
    esquema = ""
    tareas_cola = []
    tareas_entrada_ite = 0
    ejec = 0

    while tareas_entrada_ite < len(tareas_entrada) or len(tareas_cola) != 0:
        if tareas_entrada_ite < len(tareas_entrada):
            if tareas_entrada[tareas_entrada_ite][0] == t:
                p = ejec
                for i in range(ejec, len(tareas_cola)):
                    if tareas_entrada[tareas_entrada_ite][1] < tareas_cola[i][1]:
                        p = i
                        break
                    p += 1
                tareas_cola.insert(p, tareas_entrada[tareas_entrada_ite].copy())
                tareas_entrada_ite += 1

        if len(tareas_cola) > 0:
            esquema = esquema + tareas_cola[0][2]
            for i in tareas_cola:
                i[3] += 1 
            tareas_cola[0][1] -= 1

            tareas_cola[0][6] = tareas_cola[0][6] + tareas_cola[0][2]
            for i in range(1, len(tareas_cola)):
                tareas_cola[i][6] = tareas_cola[i][6] + '-'

            ejec = 1
            if tareas_cola[0][1] == 0:
                nombre = tareas_cola[0][2]
                for i in range(len(tareas_entrada)):
                    if tareas_entrada[i][2] == nombre:
                        tareas_entrada[i][3] = tareas_cola[0][3]
                        tareas_entrada[i][6] = tareas_cola[0][6]
                        break
                tareas_cola.pop(0)
                ejec = 0
        else:
            esquema = esquema + "i"
        t += 1

    calcular_resultados(tareas_entrada)
    mostrar_tabla(tareas_entrada, "SPN")
    mostrar_diagrama(tareas_entrada)
    print("\nESQUEMA:")
    print(esquema)

def selfish_round_robin(tareas, a, b):
    tareas_entrada = [proceso.copy() for proceso in tareas]
    for proceso in tareas_entrada:
        proceso[4] = a 
    t = 0
    esquema = ""
    tareas_colas = []
    tareas_entrada_ite = 0

    while tareas_entrada_ite < len(tareas_entrada) or len(tareas_colas) != 0:
        if tareas_entrada_ite < len(tareas_entrada):
            if tareas_entrada[tareas_entrada_ite][0] == t:
                if not tareas_colas:
                    tareas_colas.append([])
                tareas_colas[0].append(tareas_entrada[tareas_entrada_ite].copy())
                tareas_entrada_ite += 1

        if len(tareas_colas) > 0: 
            sig_ejec = tareas_colas[len(tareas_colas) - 1].pop(0)
            sig_ejec[4] = b
            esquema = esquema + sig_ejec[2]
            sig_ejec[1] -= 1

            sig_ejec[6] = sig_ejec[6] + sig_ejec[2]
            for i in tareas_colas:
                for j in i:
                    j[6] = j[6] + '-'

            if sig_ejec[1] > 0:
                tareas_colas[len(tareas_colas) - 1].insert(0, sig_ejec)
            else:
                nombre = sig_ejec[2]
                sig_ejec[3] += 1
                for i in range(len(tareas_entrada)):
                    if tareas_entrada[i][2] == nombre:
                        tareas_entrada[i][3] = sig_ejec[3]
                        tareas_entrada[i][6] = sig_ejec[6]
                        break

            for i in reversed(range(0, len(tareas_colas))):
                for j in range(0, len(tareas_colas[i])):
                    p = tareas_colas[i].pop(0)
                    p[3] += 1
                    if len(tareas_colas) < i + 1 + p[4]:
                        for k in range(0, p[4]):
                            tareas_colas.append([])
                    tareas_colas[i + p[4]].insert(0, p)

            ultima = 0
            for i in reversed(range(0, len(tareas_colas))):
                if len(tareas_colas[i]) != 0:
                    ultima = i + 1
                    break
            for i in range(ultima, len(tareas_colas)):
                tareas_colas.pop(ultima)
        else:
            esquema = esquema + "i"

        t += 1

    calcular_resultados(tareas_entrada)
    mostrar_tabla(tareas_entrada, "SRR")
    mostrar_diagrama(tareas_entrada)
    print("\nESQUEMA:")
    print(esquema)

# Ejemplo de uso
tareas1 = []
generar_procesos(tareas1, 5, 3, 3, 12)

fcfs(tareas1)
round_robin_n(tareas1, 1)
round_robin_n(tareas1, 4)
shortest_process_next(tareas1)
selfish_round_robin(tareas1, 2, 1)
