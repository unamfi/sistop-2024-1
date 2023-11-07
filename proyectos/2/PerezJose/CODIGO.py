import threading
import time
import random
import os
import queue

# Variables globales y bloqueos
personas_en_espera = queue.Queue()
copias_vendidas_total = 0
print_lock = threading.Lock() 

class ReadWriteLock:
    def __init__(self):
        self._readers = 0
        self._readers_lock = threading.Lock()
        self._writers_lock = threading.Lock()
    
    def acquire_read(self):
        self._readers_lock.acquire()
        self._readers += 1
        if self._readers == 1:
            self._writers_lock.acquire()
        self._readers_lock.release()
    
    def release_read(self):
        self._readers_lock.acquire()
        self._readers -= 1
        if self._readers == 0:
            self._writers_lock.release()
        self._readers_lock.release()
    
    def acquire_write(self):
        self._writers_lock.acquire()
    
    def release_write(self):
        self._writers_lock.release()

rw_lock = ReadWriteLock()

# Funciones para la venta de copias
def abrir_taquillas():
    while not personas_en_espera.empty():
        taquilla_id = personas_en_espera.get()
        rw_lock.acquire_write()
        copias_vendidas_total += 1
        rw_lock.release_write()
        personas_en_espera.task_done()

def vender_copias(taquilla_id):
    personas_en_espera.put(taquilla_id)

def llegada_personas():
    for i in range(random.randint(1, 10)):
        threading.Thread(target=vender_copias, args=(i % 3,)).start()

def mostrar_estado():
    os.system('clear')  # Esto es específico para sistemas tipo Unix

# Ejecución principal
while copias_vendidas_total < 150:
    mostrar_estado()
    llegada_personas()
    if not personas_en_espera.empty():
        threading.Thread(target=abrir_taquillas).start()
    time.sleep(10)  # Espera de 10 minutos simulada

    if input("Presiona Enter para continuar vendiendo o escribe 'cerrar' para cerrar las taquillas: ").lower() == 'cerrar':
        break
