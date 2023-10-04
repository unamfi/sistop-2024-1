#!/usr/bin/python3
import threading
from colorama import Fore
import time
import random

color_texto = [Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.WHITE, Fore.BLACK]

num_filosofos = 5
contador = 0
mut_contador = threading.Semaphore(1)

palillos = [threading.Semaphore(1) for i in range(num_filosofos)]

def digo(num, msg):
    mi_color = color_texto[num % len(color_texto)]
    # mut_contador.acquire()
    print(mi_color + '%4d // %d: %s' % (contador, num, msg))
    # mut_contador.release()

def levanta_palillo_der(quien):
    digo(quien, 'Quiero levantar el palillo derecho')
    palillos[quien].acquire()
    digo(quien, 'Tengo el palillo derecho')

def levanta_palillo_izq(quien):
    digo(quien, 'Quiero levantar el palillo izquierdo')
    palillos[(quien + 1) % num_filosofos].acquire()
    digo(quien, 'Tengo el palillo izquierdo')

def baja_palillo_izq(quien):
    palillos[(quien + 1) % num_filosofos].release()

def baja_palillo_der(quien):
    palillos[quien].release()

def piensa(quien):
    digo(quien, 'Pensando...')
    digo(quien, 'Como que hace hambrita, ¿no?')

def come(quien):
    global contador
    digo(quien, '¡Comamos algo!')
    if (quien % 2 == 0):
        levanta_palillo_der(quien)
        levanta_palillo_izq(quien)
    else:
        levanta_palillo_izq(quien)
        levanta_palillo_der(quien)

    mut_contador.acquire()
    contador += 1
    mut_contador.release()

    digo(quien, '¡ÑAM ÑAM ÑAM!')
    baja_palillo_izq(quien)
    baja_palillo_der(quien)

def filosofo(num):
    digo(num, 'Despertando a la vida en un mundo nuevo lleno de cosas en qué pensar')
    while True:
        piensa(num)
        come(num)

filosofos = [threading.Thread(target=filosofo, args=[i]) for i in range(num_filosofos)]
for i in filosofos:
    i.start()
