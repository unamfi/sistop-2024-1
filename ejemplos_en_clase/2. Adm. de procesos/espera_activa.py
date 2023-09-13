#!/usr/bin/python3
import time
import threading

datos = 0
def demora_y_entrega():
    global datos
    time.sleep(3)
    datos = 1234

threading.Thread(target=demora_y_entrega).start()

while datos == 0:
    pass
print("Listo. Datos vale %d" % datos)
