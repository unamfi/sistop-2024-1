#!/usr/bin/python3
from colorama import Fore, Back, Style
import threading
import random
import time

num_prod = 3
num_cons = 1
tamaño_banda = 3

colores = [Fore.RED, Fore.GREEN, Fore.BLUE]
fondos = [Back.YELLOW, Back.WHITE]

##### Elementos compartidos:
# banda: Una lista simple y sencillita
banda = []
# Mutex para proteger a banda de accesos concurrente
mutex_banda = threading.Semaphore(1)
# Semáforo que usamos para señalizar que hay _algún_ elemento, para obligar a
# que el consumidor _se duerma_ cuando lista está vacía
sem_num_elem = threading.Semaphore(0)
# Un "multiplex compartido", para asegurarnos de que en banda nunca haya más de
# tamaño_banda elementos
multiplex_banda = threading.Semaphore(tamaño_banda)

def productor(x):
    while True:
        time.sleep(random.random())
        # Generamos un valor
        elemento = random.random()
        print(colores[x] + fondos[0] + 'Produje: %f' % elemento)

        # Para poder poner el elemento en la banda, espero hasta que haya lugar
        # en la banda
        multiplex_banda.acquire()
        mutex_banda.acquire()
        banda.append(elemento)
        print(Style.RESET_ALL + 'La banda contiene %d elementos: %s' %
              (len(banda), banda))
        mutex_banda.release()

        sem_num_elem.release()


def consumidor(x):
    while True:
        time.sleep(random.random())

        sem_num_elem.acquire()
        print(colores[x] + fondos[1] + 'Me llegó una señal! A despertar.')

        mutex_banda.acquire()
        elemento = banda.pop(0)
        mutex_banda.release()
        # indico que hay un espacio disponible más en la banda
        multiplex_banda.release()

        print(colores[x] + fondos[1] + 'Recibí %f' % elemento)

for i in range(num_prod):
    threading.Thread(target=productor, args=[i]).start()


for i in range(num_prod):
    threading.Thread(target=consumidor, args=[i]).start()
