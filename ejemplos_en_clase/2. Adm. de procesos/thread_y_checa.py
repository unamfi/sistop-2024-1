#!/usr/bin/python3
import threading
import time

variable = 5
def dime_cuanto_es():
    print(variable)

def modifica_e_imprime():
    global variable
    variable = 10
    dime_cuanto_es()


threading.Thread(target=modifica_e_imprime).start()
time.sleep(2)
dime_cuanto_es()
