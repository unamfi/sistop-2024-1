# -*- coding: utf-8 -*-
# Esta linea la utilice para que el interprete de pythonque sea capaz de manejar
# más caracteres, es que me daba error a la hora de compilar, solo porque usaba '#'.

# Alumno: Martínez Villegas Pedro
# Sistemas operativos

#Tarea:
# Resolver un problema de programación concurrente en el que sea necesario emplear algún
# mecanismo de sincronización.

# Problema a resolver: 'De gatos y ratones'.
# Método a uttilizar: Semaforos.

import threading
import time

# Definimos los semaforos
mutex = threading.Semaphore(1)  # Para garantizar exclusión mutua
gato_comiendo = threading.Semaphore(0)  # Inicializado en 0 para que el gato espere a que termine el ratón
raton_comiendo = threading.Semaphore(0)  # Inicializado en 0 para que el ratón espere a que termine el gato

# Contador para llevar la cuenta de cuántos están comiendo
comiendo = 0

def gato(id):
    global comiendo
    while True:
        # Gato intentando comer
        mutex.acquire()
        if comiendo > 0:
            # Si hay alguien comiendo, espera
            print("Gato " + str(id) + " esperando a comer...")
            mutex.release()
            gato_comiendo.acquire()
        else:
            # Si no hay nadie comiendo, empieza a comer
            comiendo += 1
            mutex.release()

            # Simulamos al gato comiendo :3
            print("Gato " + str(id) + " comiendo, no molestar...")
            time.sleep(2)  # Simulación de comer
            print("Gato " + str(id) + " terminó de comer.")

            mutex.acquire()
            comiendo -= 1
            if comiendo == 0:
                # Si no hay nadie más comiendo, liberamos a los ratones
                raton_comiendo.release()
            mutex.release()

def raton(id):
    global comiendo
    while True:
        # Ratón intentando comer
        mutex.acquire()
        if comiendo > 0:
            # Si hay alguien comiendo, espera
            print("Ratón " + str(id) + " esperando a comer...")
            mutex.release()
            raton_comiendo.acquire()
        else:
            # Si no hay nadie comiendo, empieza a comer
            comiendo += 1
            mutex.release()

            # Simulamos al ratón comiendo
            print("Ratón " + str(id) + " comiendo...")
            time.sleep(1)  # Simulación de comer
            print("Ratón " + str(id) + " terminó de comer.")

            mutex.acquire()
            comiendo -= 1
            if comiendo == 0:
                # Si no hay nadie más comiendo, liberamos a los gatos
                gato_comiendo.release()
            mutex.release()

# Creamos hilos para gatos y ratones, en este caso 3 y 3
threading.Thread(target=gato, args=(1,)).start()
threading.Thread(target=gato, args=(2,)).start()
threading.Thread(target=gato, args=(3,)).start()
threading.Thread(target=raton, args=(1,)).start()
threading.Thread(target=raton, args=(2,)).start()
threading.Thread(target=raton, args=(2,)).start()