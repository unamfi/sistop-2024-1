import tkinter as tk
from tkinter import ttk
import threading
import queue
import time
import random
# Simulación de una cocina de restaurante

class Restaurante:
    def __init__(self, num_chefs, num_meseros):
        self.pedidos = queue.Queue()
        self.lock_equipamiento = threading.Lock()
        self.sem_meseros = threading.Semaphore(num_meseros)
        self.cond_plato_listo = threading.Condition()
        self.todos_pedidos_servidos = False  # Agregada variable para controlar el flujo

    def chef(self, id_chef):
        while True:
            pedido = self.pedidos.get()
            if pedido is None:  # Si se recibe None, es la señal para detenerse
                self.pedidos.task_done()
                break
            with self.lock_equipamiento:
                print(f"Chef {id_chef} está preparando el pedido {pedido}")
                time.sleep(random.uniform(0.5, 2))
            with self.cond_plato_listo:
                print(f"Chef {id_chef} ha terminado el pedido {pedido}")
                self.cond_plato_listo.notify_all()
            self.pedidos.task_done()

    def mesero(self, id_mesero):
        while True:
            with self.cond_plato_listo:
                self.cond_plato_listo.wait()
                if self.todos_pedidos_servidos:  # Verificar si ya se sirvieron todos los pedidos
                    break
                with self.sem_meseros:
                    print(f"Mesero {id_mesero} está sirviendo un plato.")
                    time.sleep(random.uniform(0.5, 1))

    def nuevo_pedido(self, id_pedido):
        print(f"Recibido nuevo pedido: {id_pedido}")
        self.pedidos.put(id_pedido)

    def iniciar_servicio(self, num_pedidos):
        # Iniciar hilos de chefs
        for i in range(num_chefs):
            threading.Thread(target=self.chef, args=(i,)).start()

        # Iniciar hilos de meseros
        for i in range(num_meseros):
            threading.Thread(target=self.mesero, args=(i,)).start()

        # Simular llegada de pedidos
        for i in range(num_pedidos):
            time.sleep(random.uniform(0.1, 0.3))
            self.nuevo_pedido(i)

        # Colocar None en la cola para cada chef como señal de parada
        for i in range(num_chefs):
            self.pedidos.put(None)

        # Esperar a que todos los pedidos sean procesados
        self.pedidos.join()
        with self.cond_plato_listo:  # Asegurarse de que todos los meseros revisen la condición de salida
            self.todos_pedidos_servidos = True
            self.cond_plato_listo.notify_all()
        print("Todos los pedidos han sido preparados y servidos.")

# Crear instancia del restaurante
num_chefs = 3
num_meseros = 2
restaurante = Restaurante(num_chefs, num_meseros)

# Iniciar el servicio del restaurante
restaurante.iniciar_servicio(10)
