import threading
import time

def gato(gato_id):
    while True:
        plato_id = gato_id % num_platos
        platos[plato_id].acquire()
        if gato_viendo._value == 0:
            print(f"Gato {gato_id} está comiendo en el plato {plato_id}")
            gato_viendo.release()
            platos[plato_id].release()
            time.sleep(2)
            gato_viendo.acquire()
            print(f"Gato {gato_id} termino de comer en el plato {plato_id}")
        else:
            platos[plato_id].release()
            gato_viendo.acquire()
            print(f"Gato {gato_id} atrapo un raton en el plato {plato_id}")
            time.sleep(2)
            gato_viendo.release()

def raton(raton_id):
    while True:
        plato_id = raton_id % num_platos
        platos[plato_id].acquire()
        gato_viendo.release()
        platos[plato_id].release()
        time.sleep(3)


num_gatos = 8
num_ratones = 5
num_platos = 2

platos = [threading.Semaphore(1) for _ in range(num_platos)]
gato_viendo = threading.Semaphore(0)

hilos_gatos = [threading.Thread(target=gato, args=(i,)) for i in range(num_gatos)]
hilos_ratones = [threading.Thread(target=raton, args=(i,)) for i in range(num_ratones)]

for hilo in hilos_gatos + hilos_ratones:
    hilo.start()

for hilo in hilos_gatos + hilos_ratones:
    hilo.join()