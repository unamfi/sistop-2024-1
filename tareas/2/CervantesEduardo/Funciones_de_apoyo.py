import random
import string

def tiempo_total(cargas):
    t = 0
    for i in range (len(cargas)):
        t = t + cargas[i][1]
    return t

def momento_de_llegada(cargas, id):
    if id == 0:
        return id
    else:
        duracion_actual = 0
        for j in range (id):
            duracion_actual = duracion_actual + cargas[j][1]
        momento = random.randint(1, duracion_actual)
        return momento

def encontrar_proceso(cargas, proceso):
    id = 0
    for i in range (len(cargas)):
        if cargas[i][0] == proceso:
            id = i
    return id

def promedio_tiempo_de_respuesta(tiempo_de_respuesta):
    suma_de_respuestas = 0
    for i in range (len(tiempo_de_respuesta)):
        suma_de_respuestas += tiempo_de_respuesta[i]
    promedio = suma_de_respuestas / len(tiempo_de_respuesta)
    return promedio

def calculo_de_esperas(cargas, tiempo_de_respuesta):
    esperas = []
    for i in range (len(cargas)):
        espera = tiempo_de_respuesta[i] - cargas[i][1]
        esperas.append(espera)
    
    suma_de_esperas = 0
    for i in range (len(esperas)):
        suma_de_esperas += esperas[i]
    promedio = suma_de_esperas / len(esperas)
    return esperas, promedio

def calculo_de_penalizaciones(cargas, tiempo_de_respuesta):
    penalizaciones = []
    for i in range (len(cargas)):
        penalizacion = tiempo_de_respuesta[i] / cargas[i][1]
        penalizaciones.append(penalizacion)
    
    suma_de_penalizaciones = 0
    for i in range (len(penalizaciones)):
        suma_de_penalizaciones += penalizaciones[i]
    promedio = suma_de_penalizaciones / len(penalizaciones)
    return penalizaciones, promedio

def entrega_de_resultados(cargas, cola_procesos, tiempo_de_respuesta,  esperas, penalizaciones, pt, pe, pp):
    cargas_ordenadas = sorted(cargas, key = lambda cargas: cargas[2])
    print('Proceso:\tT:\tE:\tP:')
    for i in range (len(cargas)):
        print('%c\t\t%d\t%d\t%d' % (cargas_ordenadas[i][0],tiempo_de_respuesta[i],esperas[i],penalizaciones [i]))
    print('\nPromedios:\tT:%f\tE:%f\tP:%f' % (pt,pe,pp))
    print('\nGráfico de la corrida:\n')
    print(cola_procesos)