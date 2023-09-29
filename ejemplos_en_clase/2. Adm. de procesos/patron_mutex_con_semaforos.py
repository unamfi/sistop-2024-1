#!/usr/bin/python3
import threading
import time

sem = threading.Semaphore(1)

def no_me_interrumpas(x):
    print('Soy el hilo %d, inicio ejecución' % x)
    with sem:
        print('Soy el hilo %d, inicio sección crítica' % x)
        time.sleep(1)
        print('Soy el hilo %d, termino sección crítica' % x)

# La función anterior es EXACTAMENTE equivalente a la que presento (comentada) a
# continuación, es equivalente semánticamente.

# def no_me_interrumpas(x):
#     print('Soy el hilo %d, inicio ejecución' % x)
#     sem.acquire()
#     print('Soy el hilo %d, inicio sección crítica' % x)
#     time.sleep(1)
#     print('Soy el hilo %d, termino sección crítica' % x)
#     sem.release()

for i in range(10):
    threading.Thread(target=no_me_interrumpas, args=[i]).start()
