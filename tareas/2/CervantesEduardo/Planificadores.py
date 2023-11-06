from Funciones_de_apoyo import *
from collections import deque

def FIFO(cargas):
    total = tiempo_total(cargas)
    cargas_ordenadas = sorted(cargas, key = lambda cargas: cargas[2]) #Se ordenan según el momento del tiempo en el que llegan.

    tiempo_de_respuesta = []
    for i in range (len(cargas_ordenadas)):
        tiempo_de_respuesta.append(cargas_ordenadas[i][1])

    cola_fifo = deque()
    i = 0
    t = 0

    while total > t:
        tiempo_de_proceso = cargas_ordenadas[i][1]
        tiempo_en_progreso = 0

        while tiempo_en_progreso != tiempo_de_proceso:
            cola_fifo.append(cargas_ordenadas[i][0])
            for j in range (len(cargas_ordenadas)):
                if cargas_ordenadas[j][2] <=  t and cola_fifo.count(cargas_ordenadas[j][0]) == 0:          
                    tiempo_de_respuesta[j] = tiempo_de_respuesta[j] + 1

            tiempo_en_progreso =  tiempo_en_progreso + 1
            t = t+1
                    
        i = i+1
    
    pt = promedio_tiempo_de_respuesta(tiempo_de_respuesta)
    esperas, pe = calculo_de_esperas(cargas_ordenadas, tiempo_de_respuesta)
    penalizaciones, pp = calculo_de_penalizaciones(cargas_ordenadas, tiempo_de_respuesta)

    return cola_fifo, tiempo_de_respuesta,  esperas, penalizaciones, pt, pe, pp

def RoundRobin(cargas, quantum):
    total = tiempo_total(cargas)
    cargas_ordenadas = sorted(cargas, key = lambda cargas: cargas[2])

    tiempo_de_respuesta = []
    tiempo_restante = []
    for i in range (len(cargas)):
        tiempo_de_respuesta.append(cargas_ordenadas[i][1])
        tiempo_restante.append(cargas_ordenadas[i][1])
    
    cola_RR = deque()
    cola_RR.append(cargas_ordenadas[0][0])
    RR = []
    t=0

    while total > t:
        p_en_trabajo = cola_RR.popleft()
        id_p = encontrar_proceso(cargas_ordenadas, p_en_trabajo)
        
        if tiempo_restante[id_p]  > 1:
            for i in range (quantum):
                if quantum - i == 1 and tiempo_restante[id_p] > 0:
                    for k in range (quantum):
                        RR.append(p_en_trabajo)
                        tiempo_restante[id_p] = tiempo_restante[id_p] - 1
                    cola_RR.append(p_en_trabajo)
                for j in range (len(cargas_ordenadas)):
                    if cargas_ordenadas[j][2] <=  t and cargas_ordenadas[j][0] != p_en_trabajo and tiempo_restante[j] > 0: 
                        tiempo_de_respuesta[j] = tiempo_de_respuesta[j] + 1
                        if cola_RR.count(cargas_ordenadas[j][0]) < 1:
                            cola_RR.append(cargas_ordenadas[j][0])
                t = t+1
        elif tiempo_restante[id_p]  ==  1:
                if tiempo_restante[id_p] > 0:
                    RR.append(p_en_trabajo)
                    tiempo_restante[id_p] = tiempo_restante[id_p] - 1
                    cola_RR.append(p_en_trabajo) 
                for j in range (len(cargas_ordenadas)):
                    if cargas_ordenadas[j][2] <=  t and cargas_ordenadas[j][0] != p_en_trabajo and tiempo_restante[j] > 0: 
                        tiempo_de_respuesta[j] = tiempo_de_respuesta[j] + 1
                        if cola_RR.count(cargas_ordenadas[j][0]) < 1:
                            cola_RR.append(cargas_ordenadas[j][0])
                t = t+1
        

    pt = promedio_tiempo_de_respuesta(tiempo_de_respuesta)
    esperas, pe = calculo_de_esperas(cargas_ordenadas, tiempo_de_respuesta)
    penalizaciones, pp = calculo_de_penalizaciones(cargas_ordenadas, tiempo_de_respuesta)

    return RR, tiempo_de_respuesta,  esperas, penalizaciones, pt, pe, pp

def SPN(cargas):
    total = tiempo_total(cargas)
    cargas_ordenadas = sorted(cargas, key = lambda cargas: cargas[2]) 
    tiempo_de_respuesta = []
    tiempo_restante = []
    for i in range (len(cargas_ordenadas)):
        tiempo_de_respuesta.append(cargas_ordenadas[i][1])
        tiempo_restante.append(cargas_ordenadas[i][1])

    cola_fifo = deque()
    i = 0
    t = 0

    while total > t:
        if t == 0:
            tiempo_de_proceso = cargas_ordenadas[i][1]
            id_p = 0
        else:
            for k in range (len(tiempo_restante)):
                if tiempo_restante[k] > 0 and cargas_ordenadas[k][2] <=  t:
                    comparador = tiempo_restante[k]
                    id_p = k
                    if tiempo_restante[k-1] < comparador and tiempo_restante[k-1] > 0:
                        comparador = tiempo_restante[k-1]
                        id_p = k - 1

            tiempo_de_proceso = comparador

        tiempo_en_progreso = 0

        while tiempo_en_progreso != tiempo_de_proceso:
            cola_fifo.append(cargas_ordenadas[id_p][0])
            for j in range (len(cargas_ordenadas)):
                if cargas_ordenadas[j][2] <=  t and cola_fifo.count(cargas_ordenadas[j][0]) == 0:          
                    tiempo_de_respuesta[j] = tiempo_de_respuesta[j] + 1

            tiempo_en_progreso =  tiempo_en_progreso + 1
            tiempo_restante[id_p] = tiempo_restante[id_p] - 1
            t = t+1
                    
        i = i+1
    
    pt = promedio_tiempo_de_respuesta(tiempo_de_respuesta)
    esperas, pe = calculo_de_esperas(cargas_ordenadas, tiempo_de_respuesta)
    penalizaciones, pp = calculo_de_penalizaciones(cargas_ordenadas, tiempo_de_respuesta)

    return cola_fifo, tiempo_de_respuesta,  esperas, penalizaciones, pt, pe, pp


    
