#Reglas:
# -Al inicializar, le proceso jefe lanza 'k' hilos trabajadores
#   -Los trabajadores ue no tienen nada que hacer se van a dormir 
# -El proceso jefe recibe una conexion de red, y elige a cualquiera de los trabajadores para que la atienda
#   -Se le asigna a un trabajador y lo despierta
# -El jefe va a buscar mantener siempre a 'k' hilos disponibles y listos para atender las solicitudes que van llegando 

import threading
from threading import Semaphore
import time
import random

k = 5 #Hilos trabajadores en espera
wakeWorker = Semaphore(0)
requestClient = Semaphore(0)
workers = 0
mut_workers = Semaphore(1)


def worker():
    global wakeWorker, workers, mut_workers
    mut_workers.acquire()
    workers += 1
    amI = workers
    mut_workers.release()
    print('Trabajador%2d: Listo, ¡Esperando ordenes!\n'% amI)
    wakeWorker.acquire()
    print ('Trabajador%2d:  Atendiendo la solicitud...\n'% amI)
    time.sleep(random.random())
    print ('Trabajador%2d: Ya termine, ire a descansar\n'% amI)


def Boss():
    global k , requestClient
    # En la inicializacion lanzamos 'k' hilos trabajadores
    print('      Boss: Empezando, lanzo %d hilos trabajador\n' %k)
    for i in range(k):
        threading.Thread(target=worker, args=[]).start()
    while True:
        print('      Boss: Esperando conexion de red...\n')
        requestClient.acquire()
        print('      Boss: Despertando a un trabajador...\n')
        wakeWorker.release
        print('      Boss: Creando nuevo trabajador...\n')
        threading.Thread(target=worker, args=[]).start()


def clientLauncher():
    global requestClient
    while True:
        time.sleep(random.random())
        print('  Cliente: ¡Tengo una nueva solicitud!\n')
        requestClient.release()


threading.Thread(target=Boss, args=[]).start()
clientLauncher() 