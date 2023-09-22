#!/usr/bin/python3
import threading
import time
import random

num_jugadores = 5
total_jugadores = 20
multiplex = threading.Semaphore(num_jugadores)
barrera = threading.Semaphore(0)
activos = []
mut_activos = threading.Semaphore(1)

def multiplexado(x):
    print('%02d: Inicio ejecución' % x)
    multiplex.acquire()

    # ↓ Manejo de mutex para modificar el arreglo activos
    mut_activos.acquire()
    activos.append(x)
    if len(activos) == num_jugadores:
        barrera.release()
    mut_activos.release()

    # ↓ 'barrera' es una barrera, pero es también una implementación de un
    # torniquete
    barrera.acquire()
    barrera.release()

    print('%02d: inicio porción compartida; estamos: %s' % (x, activos))
    time.sleep(random.random())

    # ↓ Manejo de mutex para modificar el arreglo activos
    mut_activos.acquire()
    activos.remove(x)
    mut_activos.release()

    print('%02d: termino porción compartida' % x)
    multiplex.release()

print('- = { ¡ COMBATE MULTIJUGADOR ! } = -')
print('¡Bienvenidos concursantes! Ahora van a agarrarse a catorrazos...')
print('¡De %d en %d!' % (num_jugadores, num_jugadores))

for i in range(num_jugadores):
    threading.Thread(target=multiplexado, args=[i]).start()
