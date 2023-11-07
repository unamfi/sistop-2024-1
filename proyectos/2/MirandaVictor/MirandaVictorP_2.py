# Miranda Barajas Victor
import threading
import time
import random
import queue
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Aeropuerto:
    def __init__(self):
        self.pistas = [threading.Semaphore(1) for _ in range(3)]  # Tres pistas disponibles
        self.torre_control = queue.PriorityQueue()  # Torre de control gestiona prioridades
        self.espera_pistas = threading.Condition()  # Condición para esperar pistas disponibles
    
    def asignar_pista(self, avion):
        asignada = False
        while not asignada:
            with self.espera_pistas:
                for i, pista in enumerate(self.pistas):
                    if pista.acquire(blocking=False):
                        logging.info(f"Avión {avion.avion_id} asignado a la pista {i}.")
                        asignada = True
                        avion.pista_asignada = i
                        break
                if not asignada:
                    logging.info(f"Avión {avion.avion_id} esperando por una pista.")
                    self.espera_pistas.wait()  # Espera hasta que una pista se libere
    
    def liberar_pista(self, avion_id, pista_asignada):
        self.pistas[pista_asignada].release()
        with self.espera_pistas:
            logging.info(f"Avión {avion_id} liberó la pista {pista_asignada}.")
            self.espera_pistas.notify()  # Notifica a los aviones en espera que una pista se ha liberado

class Avion(threading.Thread):
    def __init__(self, avion_id, aeropuerto, prioridad):
        super().__init__()
        self.avion_id = avion_id
        self.aeropuerto = aeropuerto
        self.prioridad = prioridad
        self.pista_asignada = None
    
    def run(self):
        # Espera en la torre de control basado en la prioridad
        self.aeropuerto.torre_control.put((self.prioridad, self))
        self.aeropuerto.torre_control.get((self.prioridad, self))
        
        # Asignar pista
        self.aeropuerto.asignar_pista(self)
        
        # Simular despegue/aterrizaje
        time.sleep(random.uniform(1, 2))
        
        # Liberar pista
        self.aeropuerto.liberar_pista(self.avion_id, self.pista_asignada)
        
        # Notificar a la torre de control que ha terminado
        self.aeropuerto.torre_control.task_done()

# Simulación
aeropuerto = Aeropuerto()
aviones = [Avion(i, aeropuerto, random.randint(1, 3)) for i in range(10)]  # Diez aviones con prioridades aleatorias

for avion in aviones:
    avion.start()

for avion in aviones:
    avion.join()
