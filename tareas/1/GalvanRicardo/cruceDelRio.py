# Galvan Ricardo - Sistemas Operativos, Tarea 1.
import threading
import time
import random

numPasajeros = 4
totalPasajeros = 20

multiplex = threading.Semaphore(numPasajeros)
barrera = threading.Semaphore(0)

pasajerosDentro = []

hackersDentro = []
serfsDentro = []
mut_activos = threading.Semaphore(1)

def multiplexado(x):
    print('[%02d]: Inicio ejecución' % x)
    multiplex.acquire()
    
    if(x%2 == 0):
        print('[%02d]: Soy hacker, Me subo a la balsa' % (x))
        hackersDentro.append(x)
    if(x%2 != 0):
        print('[%02d]: Soy serf, Me subo a la balsa' % (x))
        serfsDentro.append(x)
    
    mut_activos.acquire()
    pasajerosDentro.append(x)
    
    if len(pasajerosDentro) == numPasajeros:
        barrera.release()
    mut_activos.release()
    
    barrera.acquire()
    barrera.release()

    print('\n')
    print('Viajamos en la balsa: %s ' % (pasajerosDentro))
    print('Viajamos los hackers: %s y los serfs: %s' % (hackersDentro, serfsDentro))

    time.sleep(random.random())

    mut_activos.acquire()
    pasajerosDentro.remove(x)
    mut_activos.release()

    if(x%2 == 0):
        print('[%02d]: Soy hacker, Me bajo de la balsa' % (x))
        hackersDentro.remove(x)
    if(x%2 != 0):
        print('[%02d]: Soy serf, Me bajo de la balsa' % (x))
        serfsDentro.remove(x)
    multiplex.release()
    

print('|------------------<[ CRUZANDO EL RIO ]>------------------|\n')
print('A continuación, los desarrolladores (hackers y serfs) cruzarán el río en una balsa.\n')
print('Deben cruzar de %d en %d, sólo con las siguientes configuraciones:' % (numPasajeros, numPasajeros))
print('  - El mismo número de hackers y serfs')
print('  - %d desarrolladores del mismo bando\n' % (numPasajeros))

for i in range(totalPasajeros):
    threading.Thread(target=multiplexado, args=[i]).start()