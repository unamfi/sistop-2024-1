import threading
import time
import random

class Metro:
    def __init__(self):
        self.pasajeros_dentro = 0
        self.puertas_abiertas = False
        self.pasajeros_bajando = 0
        self.pasajeros_subiendo = 0
        self.mutex = threading.Lock()
        self.cond = threading.Condition(self.mutex)

    def abrir_puertas(self):
        with self.mutex:
            self.puertas_abiertas = True

    def cerrar_puertas(self):
        with self.mutex:
            self.puertas_abiertas = False

    def bajar_pasajero(self):
        with self.mutex:
            while not self.puertas_abiertas or self.pasajeros_subiendo > 0:
                self.cond.wait()
            self.pasajeros_bajando += 1

    def subir_pasajero(self):
        with self.mutex:
            while not self.puertas_abiertas or self.pasajeros_bajando > 0:
                self.cond.wait()
            self.pasajeros_subiendo += 1

    def terminar_bajar(self):
        with self.mutex:
            self.pasajeros_dentro -= 1
            self.pasajeros_bajando -= 1

    def terminar_subir(self):
        with self.mutex:
            self.pasajeros_dentro += 1
            self.pasajeros_subiendo -= 1

def pasajero(metro):
    while True:
        time.sleep(random.randint(1, 5))
        metro.bajar_pasajero()
        time.sleep(random.randint(1, 5))
        metro.terminar_bajar()
        time.sleep(random.randint(1, 5))
        metro.subir_pasajero()
        time.sleep(random.randint(1, 5))
        metro.terminar_subir()

def metro(metro):
    while True:
        time.sleep(random.randint(1, 5))
        metro.abrir_puertas()
        time.sleep(random.randint(1, 5))
        metro.cerrar_puertas()

if __name__ == "__main__":
    metro_obj = Metro()
    for i in range(10):
        threading.Thread(target=pasajero, args=(metro_obj,)).start()
    threading.Thread(target=metro, args=(metro_obj,)).start()
