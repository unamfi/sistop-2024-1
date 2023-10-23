import threading
import random
import time

# Variables para la sincronización
mutex = threading.Semaphore(1)
elfos_esperando = threading.Semaphore(0)
renos_de_vuelta = threading.Semaphore(0)

def elfo_trabajo():
    while True:
        # Simula el tiempo que un elfo trabaja
        time.sleep(random.randint(1, 5))
        with mutex:
            print("Elfo necesita ayuda")
            elfos_esperando.release()
        with mutex:
            print("Elfo recibe ayuda")
            elfos_esperando.acquire()

def reno_vuelta():
    while True:
        # Simula el tiempo que un reno está de vuelta
        time.sleep(random.randint(20, 30))
        with mutex:
            print("Reno de vuelta")
            renos_de_vuelta.release()

def santa_claus():
    while True:
        # Esperar hasta que 9 renos estén de vuelta
        for _ in range(9):
            renos_de_vuelta.acquire()
        print("Santa despierta y prepara el trineo")

        # Ayudar a tres elfos
        for _ in range(3):
            elfos_esperando.release()
            print("Santa ayuda a un elfo")
            elfos_esperando.acquire()

        print("Santa vuelve a dormir")
        time.sleep(5)

# Crear hilos para Santa, elfos y renos
santa_thread = threading.Thread(target=santa_claus)
santa_thread.start()

elfo_threads = [threading.Thread(target=elfo_trabajo) for _ in range(10)]
for thread in elfo_threads:
    thread.start()

reno_threads = [threading.Thread(target=reno_vuelta) for _ in range(9)]
for thread in reno_threads:
    thread.start()

# Esperar a que todos los hilos terminen
santa_thread.join()
for thread in elfo_threads:
    thread.join()
for thread in reno_threads:
    thread.join()
