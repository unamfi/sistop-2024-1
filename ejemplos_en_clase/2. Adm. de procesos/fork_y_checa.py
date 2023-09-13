#!/usr/bin/python3
import os
import time

variable = 5
def dime_cuanto_es():
    print(variable)

def fork_y_checa():
    global variable
    pid = os.fork()
    if pid > 0:
        time.sleep(2)
        dime_cuanto_es()
    else:
        variable = 10
        dime_cuanto_es()
        exit()

fork_y_checa()
