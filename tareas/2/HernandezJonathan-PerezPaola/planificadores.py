# Mensaje de introducción.
print("• SIMULACIÓN DE PLANIFICACIÓN DE PROCESOS.\n")
print("¡Bienvenido! Este programa compara los resultados de diferentes")
print("algoritmos de planificación, con tal de analizarlos debidamente.\n")

import os
import time

class Proceso:
    def __init__(self, nombre, tiempo_llegada, tiempo_ejecucion):
        # Clase que define un proceso con un nombre, tiempo de llegada y tiempo de ejecución.
        self.nombre = nombre
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_ejecucion = tiempo_ejecucion
        self.tiempo_restante = tiempo_ejecucion
        
# A partir de aquí, se definen tres algoritmos de planificación: FCFS, RR y SPN.

# FCFS (First-Come, First-Served).
def fcfs(planificacion):
    tiempo_actual = 0
    anterior =0
    fin =0
    inicio = 0
    acumulador_t = 0
    acumulador_e = 0
    acumulador_p = 0
    
    for proceso in planificacion:
        if tiempo_actual < proceso.tiempo_llegada:
            tiempo_actual = proceso.tiempo_llegada
            
        if (proceso.nombre == "A"):
            stiempo_t = proceso.tiempo_ejecucion - proceso.tiempo_llegada
            inicio = proceso.tiempo_llegada
            fin = proceso.tiempo_ejecucion
            anterior = fin
            
        if (proceso.nombre != "A"):
            fin = anterior + proceso.tiempo_ejecucion
            inicio = anterior
        anterior = fin
        
        # Cálculo de métricas de tiempo
        stiempo_t = fin - proceso.tiempo_llegada
        stiempo_e = stiempo_t - proceso.tiempo_ejecucion
        stiempo_p = stiempo_t / proceso.tiempo_ejecucion
        acumulador_t += stiempo_t
        acumulador_e += stiempo_e
        acumulador_p += stiempo_p
        
        # Imprimir el nombre del proceso multiplicado por su tiempo de ejecución.
        print(proceso.nombre * proceso.tiempo_ejecucion, end ="")
    
    tiempo_t = acumulador_t / len (planificacion)
    tiempo_e = acumulador_e / len(planificacion) 
    tiempo_p = acumulador_p / len(planificacion) 
  
    return tiempo_t,tiempo_e,tiempo_p

# RR (Round Robin).
def rr(planificacion, quantum):
    tiempo_espera_total = 0
    cola = list(planificacion)
    tiempo_actual = 0
    fin =0
    inicio = 0
    acumulador_t = 0
    acumulador_e = 0
    acumulador_p = 0
    
    while cola:
        proceso = cola.pop(0)
        
        if proceso.tiempo_restante > quantum:
            tiempo_actual += quantum
            proceso.tiempo_restante -= quantum
            cola.append(proceso)
        
        else:
            tiempo_actual += proceso.tiempo_restante
            tiempo_espera = tiempo_actual - proceso.tiempo_llegada - proceso.tiempo_ejecucion
            tiempo_espera_total += max(tiempo_espera, 0)
            
            # Imprimir el nombre del proceso multiplicado por su tiempo de ejecución.
            print(proceso.nombre * proceso.tiempo_ejecucion, end ="")

    #Falta calcular inicio y fin del algoritmo.    
    stiempo_t = fin - proceso.tiempo_llegada
    stiempo_e =  stiempo_t - proceso.tiempo_ejecucion
    stiempo_p = stiempo_t / proceso.tiempo_ejecucion
    acumulador_t += stiempo_t
    acumulador_e += stiempo_e
    acumulador_p += stiempo_p
    tiempo_promedio_espera = tiempo_espera_total / len(planificacion)
    return tiempo_promedio_espera

# SPN (Shortest Process Next).
def spn(planificacion):
    # Se ordena la planificación en función del tiempo de ejecución y tiempo de llegada.
    planificacion.sort(key=lambda x: (x.tiempo_ejecucion, x.tiempo_llegada))
    tiempo_espera_total = 0
    anterior =0
    fin =0
    inicio = 0
    acumulador_t = 0
    acumulador_e = 0
    acumulador_p = 0
    
    for proceso in planificacion:
        # Falta calcular el tiempo inicial.
        fin = inicio + proceso.tiempo_ejecucion
        
        # Cálculo de métricas de tiempo.
        stiempo_t = fin - proceso.tiempo_llegada
        stiempo_e =  stiempo_t - proceso.tiempo_ejecucion
        stiempo_p = stiempo_t / proceso.tiempo_ejecucion
        acumulador_t += stiempo_t
        acumulador_e += stiempo_e
        acumulador_p += stiempo_p
        
        # Imprimir el nombre del proceso multiplicado por su tiempo de ejecución.
        print(proceso.nombre * proceso.tiempo_ejecucion, end ="")

    tiempo_promedio_espera = tiempo_espera_total / len(planificacion)
    return tiempo_promedio_espera

# Definición de procesos.
proceso1 = Proceso("A", 0, 3)
proceso2 = Proceso("B", 1, 5)
proceso3 = Proceso("C", 3, 2)
proceso4 = Proceso("D", 9, 5)
proceso5 = Proceso("E", 12, 5)

# Definición de una segunda ronda de procesos.
proceso6 = Proceso("A", 0, 5)
proceso7 = Proceso("B", 3, 3)
proceso8 = Proceso("C", 3, 7)
proceso9 = Proceso("D", 7, 4)
proceso10 = Proceso("E", 8, 4)

# Añadimos los procesos a una variable.
# Asimismo, se agrupan los procesos en listas.
lista_procesos = [proceso1, proceso2, proceso3,proceso4,proceso5]
lista_procesos2 = [proceso6, proceso7, proceso8,proceso9,proceso10]

# Impresión de los resultados de cada algoritmo en la primera ronda.
# FCFS, RR1, RR4, y SPN se ejecutan con lista_procesos.
print("Comparación de algoritmos de planificación:\n")
print("• PRIMERA RONDA.")
print("Procesos: ", [(p.nombre ,p.tiempo_llegada, p.tiempo_ejecucion) for p in lista_procesos])

print("FCFS:")
tiempo_t,tiempo_e,tiempo_p= fcfs(lista_procesos)
print()
print(f"T = {tiempo_t:.1f}",end=" ")
print(f"E = {tiempo_e:.1f}",end =" ")
print(f"P = {tiempo_p:.2f}")

# RR1 (Round Robin con quantum 1).
print("RR1 (Quantum 1):")
tiempo_promedio_espera_rr = rr(lista_procesos, 1)
print(f"\nE (RR): {tiempo_promedio_espera_rr:.2f}")

# RR4 (Round Robin con quantum 4).
print("RR4 (Quantum 4):")
tiempo_promedio_espera_rr = rr(lista_procesos, 4)
print(f"\nE (RR): {tiempo_promedio_espera_rr:.2f}")

# SPN (Shortest Process Next).
print("SPN:")
tiempo_promedio_espera_spn = spn(lista_procesos)
print(f"\nE (SPN): {tiempo_promedio_espera_spn:.2f}")

total = sum(p.tiempo_ejecucion for p in lista_procesos)
print("tot : ", total)

# Impresión de los resultados de cada algoritmo en la segunda ronda.
# FCFS, RR1, RR4 y SPN se ejecutan con lista_procesos2.
print("\n• SEGUNDA RONDA.")
print("Procesos: ", [(p.nombre, p.tiempo_llegada , p.tiempo_ejecucion) for p in lista_procesos2])

# FCFS.
print("FCFS:")
tiempo_t,tiempo_e,tiempo_p= fcfs(lista_procesos)
print()
print(f"T = {tiempo_t:.1f}",end=" ")
print(f"E = {tiempo_e:.1f}",end =" ")
print(f"P = {tiempo_p:.2f}")

# RR1 (Round Robin con quantum 1).
print("RR1 (Quantum 1):")
tiempo_promedio_espera_rr = rr(lista_procesos, 1)
print(f"\nE (RR): {tiempo_promedio_espera_rr:.2f}")

# RR4 (Round Robin con quantum 4).
print("RR4 (Quantum 4):")
tiempo_promedio_espera_rr = rr(lista_procesos, 4)
print(f"\nE (RR): {tiempo_promedio_espera_rr:.2f}")

# SPN (Shortest Process Next).
print("SPN:")
tiempo_promedio_espera_spn = spn(lista_procesos2)
print(f"\nE (SPN): {tiempo_promedio_espera_spn:.2f}")

total = sum(p.tiempo_ejecucion for p in lista_procesos2)
print("tot : ", total)

# Pausa el programa durante 15 segundos.
time.sleep(15)
# Limpia la pantalla (sistema dependiente, se usa 'cls' en sistemas Windows).
os.system('cls')