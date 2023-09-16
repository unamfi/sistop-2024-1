#!/usr/bin/python3
from threading import Thread, Lock
from time import sleep
from random import random

llave_del_baño = Lock()

def funcion_concurrente(yo):
    for i in range(5):
        print("%3d quiere entrar a la sección crítica!" % yo)
        llave_del_baño.acquire()
        print("%3d entrando a la sección crítica por %d-ésima vez..." % (yo, i))
        sleep(random())
        print("%3d sale de la sección crítica" % yo)
        llave_del_baño.release()
        sleep(random())

for i in range(5):
    Thread(target=funcion_concurrente, args=[i]).start()
