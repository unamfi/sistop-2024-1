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

num_lectores = 10
num_escritores = 2
color_texto = [Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.WHITE, Fore.BLACK]
fondo_texto = [Back.BLUE, Back.RED]

pizarron = ''
mutex_pizarron = threading.Semaphore(1)
lectores_ahora = 0
mutex_lectores_ahora = threading.Semaphore(1)
torniquete = threading.Semaphore(1)

def digo(rol, num, msg):
    mi_color = fondo_texto[rol % len(fondo_texto)] + color_texto[num % len(color_texto)]
    print(mi_color + msg)

def lector(x):
    global pizarron
    global lectores_ahora

    while True:
        time.sleep(0.01)

        torniquete.acquire()
        torniquete.release()

        # Al llegar, verifico si hay otro "de mi calaña" en el salón
        mutex_lectores_ahora.acquire()
        if lectores_ahora == 0:
            mutex_pizarron.acquire()
        lectores_ahora += 1
        mutex_lectores_ahora.release()

        digo(0, x, 'El lector %d está leyendo (y somos %d)' % (x, lectores_ahora))
        digo(0, x, 'Dice que «%s»' % pizarron)
        time.sleep(random.random())

        # Al salir, veo si permanece algún colega, y si no, libero el salón
        mutex_lectores_ahora.acquire()
        lectores_ahora -= 1
        if lectores_ahora == 0:
            mutex_pizarron.release()
        mutex_lectores_ahora.release()


def escritor(x):
    global pizarron
    while True:
        time.sleep(0.01)
        torniquete.acquire()
        mutex_pizarron.acquire()
        sabiduria = random.random()
        digo(1, x, 'El escritor %d está escribiendo «%s»' % (x, sabiduria))
        pizarron = 'Aquí estuvo el escritor %d y dijo que %f' % (x, sabiduria)
        time.sleep(3 + random.random())
        digo(1, x, 'El escritor %d ya se fue.' % x)
        mutex_pizarron.release()
        torniquete.release()

for i in range(num_escritores):
    threading.Thread(target=escritor, args=[i]).start()
    time.sleep(random.random())

for i in range(num_lectores):
    threading.Thread(target=lector, args=[i]).start()
    time.sleep(random.random())

