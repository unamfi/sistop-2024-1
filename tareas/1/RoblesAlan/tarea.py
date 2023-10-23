import threading
import time
import random

# Número de gatos, ratones, platos y turnos
k = 3  # Cantidad de gatos
l = 3  # Cantidad de ratones
m = 3  # Cantidad de platos
turnos = 10 # Cantidad de turnos

# Semáforos
mutex_platos = threading.Semaphore(m)
gato_come = threading.Semaphore(0)
raton_come = threading.Semaphore(0)
gato_observa = threading.Semaphore(0)

def gato(id):
    for turno in range(turnos):
        time.sleep(random.uniform(0, 1))  # Gato haciendo sus cosas
        mutex_platos.acquire()
        print(f"Gato {id} empieza a comer en el turno {turno + 1}")
        gato_come.release()
        mutex_platos.release()
        gato_observa.acquire()
        time.sleep(random.uniform(0, 1))  # Gato termina de comer
        print(f"Gato {id} termina de comer en el turno {turno + 1}")

def raton(id):
    for turno in range(turnos):
        time.sleep(random.uniform(0, 1))  # Ratón haciendo sus cosas
        mutex_platos.acquire()
        if gato_come._value > 0:
            print(f"¡Ratón {id} es visto por un gato y es comido en el turno {turno + 1}!")
            gato_observa.release()
        else:
            print(f"Ratón {id} empieza a comer en el turno {turno + 1}")
            raton_come.release()
        mutex_platos.release()
        time.sleep(random.uniform(0, 1))  # Ratón termina de comer
        print(f"Ratón {id} termina de comer en el turno {turno + 1}")

# Crear hilos de gatos y ratones
threads = []
for i in range(k):
    threads.append(threading.Thread(target=gato, args=(i,)))
for i in range(l):
    threads.append(threading.Thread(target=raton, args=(i,)))

# Iniciar los hilos
for thread in threads:
    thread.start()

# Esperar a que todos los hilos terminen
for thread in threads:
    thread.join()

print("Todos los gatos y ratones han terminado.")