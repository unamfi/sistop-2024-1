import random
import string
from collections import deque
from Funciones_de_apoyo import *
from Planificadores import *

nombres = list(string.ascii_uppercase)
'''
Tuplas - (Nombre,número de ticks, momento de llegada)
se usan enteros para obsevar el tiempo discreto
Se añade como tupla el número de ticks del proceso para tenerlo como información en SPN
'''
def generador_de_cargas():
    cantidad = random.randint(4, 6)
    cargas = []
    for i in range (cantidad):
        cargas.append((nombres[i], random.randint(1,15), momento_de_llegada(cargas, i)))
    return cargas

def main():
    for i in range (5):
        cargas = generador_de_cargas()
        cola_FIFO, tiempo_de_respuesta_f,  esperas_f, penalizaciones_f, pt_f, pe_f, pp_f = FIFO(cargas)
        cola_RR, tiempo_de_respuesta_r,  esperas_r, penalizaciones_r, pt_r, pe_r, pp_r = RoundRobin(cargas,2)
        cola_SPN, tiempo_de_respuesta_s,  esperas_s, penalizaciones_s, pt_s, pe_s, pp_s = SPN(cargas)
        print('\t\t\t----RONDA %d----\t\t\t\n' % (i))
        print('Estas son las cargas de la prueba de la ronda:')
        print(cargas)
        print('\n')
        print('\t\t\t---FCFS---\t\t\t')
        entrega_de_resultados(cargas, cola_FIFO, tiempo_de_respuesta_f,  esperas_f, penalizaciones_f, pt_f, pe_f, pp_f)
        print('\t\t\t---ROUND ROBIN---\t\t\t')
        entrega_de_resultados(cargas, cola_RR, tiempo_de_respuesta_r,  esperas_r, penalizaciones_r, pt_r, pe_r, pp_r)
        print('\t\t\t---SPN---\t\t\t')
        entrega_de_resultados(cargas, cola_SPN, tiempo_de_respuesta_s,  esperas_s, penalizaciones_s, pt_s, pe_s, pp_s)
        print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')

main()

