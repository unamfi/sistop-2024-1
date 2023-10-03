#!/usr/bin/python3
#
# ¡OJO!
#
# Esta versión tiene un bug ☹ Los lectores siguen entrando al cuarto incluso
# cuando el escritor está dentro. Investigo... Comprometo respuesta. Pero
# mientras tanto, aquí tienen el código.
import threading
import random
import time
from colorama import Fore, Back

num_lectores = 4
num_escritores = 1
colores = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.MAGENTA, Fore.WHITE]

pizarron = ''
mutex_pizarron = threading.Semaphore(1)
lectores_ahora = 0
mutex_lectores_ahora = threading.Semaphore(1)
torniquete = threading.Semaphore(1)

def lector(x):
    global pizarron
    global lectores_ahora

    torniquete.acquire()
    torniquete.release()

    while True:
#        time.sleep(0.01)
        # Al llegar, verifico si hay otro "de mi calaña" en el salón
        mutex_lectores_ahora.acquire()
        if lectores_ahora == 0:
            mutex_pizarron.acquire()
        lectores_ahora += 1
        mutex_lectores_ahora.release()

        print(Back.CYAN + colores[x % len(colores)] + 'El lector %d está leyendo' % x)
        print('Dice que «%s»' % pizarron)
        time.sleep(random.random())
        mutex_pizarron.release()

        # Al salir, veo si permanece algún colega, y si no, libero el salón
        mutex_lectores_ahora.acquire()
        lectores_ahora -= 1
        if lectores_ahora == 0:
            mutex_pizarron.release()
        mutex_lectores_ahora.release()


def escritor(x):
    global pizarron
    while True:
#        time.sleep(0.01)
        torniquete.acquire()
        mutex_pizarron.acquire()
        sabiduria = random.random()
        print(Back.YELLOW + colores[x] + 'El escritor %d está escribiendo «%s»' % (x, sabiduria))
        pizarron = 'Aquí estuvo el escritor %d y dijo que %f' % (x, sabiduria)
        time.sleep(3 + random.random())
        print(Back.YELLOW + colores[x] + 'El escritor %d ya se fue.' % x)
        mutex_pizarron.release()
        torniquete.release()

for i in range(num_lectores):
    threading.Thread(target=lector, args=[i]).start()

for i in range(num_escritores):
    threading.Thread(target=escritor, args=[i]).start()
