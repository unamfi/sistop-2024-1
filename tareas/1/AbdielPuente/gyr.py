import threading
import time

plato1_semaforo = threading.Semaphore(1)
plato2_semaforo = threading.Semaphore(1)

gato_semaforo = threading.Semaphore(2)
raton_semaforo = threading.Semaphore(1)

gatos_terminaron = threading.Condition()

def gato(id):
    print(f"Gato {id} quiere comer.")
    
    gato_semaforo.acquire()
    
    plato1_semaforo.acquire()
    print(f"Gato {id} está comiendo en el plato 1.")
    time.sleep(2)
    plato1_semaforo.release()
    
    plato2_semaforo.acquire()
    print(f"Gato {id} está comiendo en el plato 2.")
    time.sleep(2)
    plato2_semaforo.release()
    
    gato_semaforo.release()
    print(f"Gato {id} ha terminado de comer.")
    
    with gatos_terminaron:
        gatos_terminaron.notify()

def raton(id):
    print(f"Ratón {id} quiere comer.")
    
    with gatos_terminaron:
        gatos_terminaron.wait()
    
    raton_semaforo.acquire()
    
    if gato_semaforo._value > 0:
        print(f"Gato se comió al Ratón {id}.")
        raton_semaforo.release()
        return
    
    plato1_semaforo.acquire()
    print(f"Ratón {id} está comiendo en el plato 1.")
    time.sleep(2)
    plato1_semaforo.release()
    
    plato2_semaforo.acquire()
    print(f"Ratón {id} está comiendo en el plato 2.")
    time.sleep(2)
    plato2_semaforo.release()
    
    raton_semaforo.release()
    print(f"Ratón {id} ha terminado de comer.")

gatos = [threading.Thread(target=gato, args=(i,)) for i in range(2)]
ratones = [threading.Thread(target=raton, args=(i,)) for i in range(1)]

for gato_thread in gatos:
    gato_thread.start()

for raton_thread in ratones:
    raton_thread.start()

for gato_thread in gatos:
    gato_thread.join()
for raton_thread in ratones:
    raton_thread.join()
