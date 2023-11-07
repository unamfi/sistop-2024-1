import threading
import time
import random
from queue import Queue

# Definición del teatro con 50 asientos
num_asientos = 50
asientos_disponibles = list(range(1, num_asientos + 1))
bloqueo = threading.Lock()
cola_reservas = Queue()

# Función para que un cliente reserve un asiento
def reserva_asiento(cliente):
    global asientos_disponibles
    while True:
        if not asientos_disponibles:
            break  # Todos los asientos están reservados
        asiento = None
        with bloqueo:
            if asientos_disponibles:
                asiento = asientos_disponibles.pop(0)
        if asiento is not None:
            print(f"Cliente {cliente} reservó el asiento {asiento}")
            time.sleep(random.uniform(0.1, 0.5))  # Simula el tiempo que lleva la reserva
        else:
            print(f"Cliente {cliente} no pudo reservar. Todos los asientos están ocupados.")
            break
        cola_reservas.put(asiento)  # Agrega el asiento a la cola de reservas

# Función para mostrar el estado actual de las reservas
def estado_reservas():
    while not cola_reservas.empty():
        print(f"Asiento {cola_reservas.get()} está reservado.")

# Crear clientes (hilos) que intentarán reservar asientos
clientes = []
for i in range(10):  # 10 clientes
    cliente = threading.Thread(target=reserva_asiento, args=(i,))
    clientes.append(cliente)
    cliente.start()

# Esperar a que todos los clientes terminen de reservar
for cliente in clientes:
    cliente.join()

# Mostrar el estado final de las reservas
estado_reservas()
