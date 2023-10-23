# El servidor web
# Se enfoca en hacer el modelo de programación Jefe-Trabajador

# Cruz Vargas Emilio
# Garciliano Díaz Giovanni Alfredo

from colorama import Fore, Back, Style
import threading
import random
import time
import sys
import string

def imprime_t(idx, cad):
    print(f"{Fore.MAGENTA}{Style.BRIGHT}Trabajador {idx}:{Style.RESET_ALL} {cad}")
def imprime_j(cad):
    print(f"{Fore.YELLOW}{Style.BRIGHT}Jefe:{Style.RESET_ALL} {cad}")

class servidor():
    
    # Comportamiento del trabajador    
    def trabajador(self, idx):
        while True:
            self.mutex.acquire()
            peticion = len(self.peticiones)
            if peticion is not None:
                imprime_t(idx, f"Atendiendo petición {peticion}")
                time.sleep(random.uniform(1, 3))
                byte_size = random.randint(1, 2323243)
                self.peticiones.append(byte_size)
                imprime_t(idx, f"Terminó de ejecutarse {print(''.join(random.choices(string.ascii_lowercase, k=5)))}, se enviaron {byte_size} bytes.")
            self.mutex.release()

    # Asignar una petición
    def asignar_peticion(self, peticion):
        # self.peticiones.append(None)
        self.mutex.release()
        #print(self.peticiones)
        imprime_j("Recibiendo petición " + str(peticion))

    # Crear instancia de la clase e inicializar atributos
    def __init__(self, numTrabajadores):
        self.numTrabajadores = numTrabajadores
        self.peticiones = []
        self.mutex = threading.Semaphore(0)
        self.worker_threads = []

        # Inicializar hilos
        for i in range(numTrabajadores):
            t = threading.Thread(target=self.trabajador, args=[i])
            self.mutex.release()
            self.worker_threads.append(t) # lista para llevar un registro de los hilos trabajadores
            t.start()

try:
    if len(sys.argv) != 2:
        raise RuntimeException()
    numTrabajadores = int(sys.argv[1])
except:
    print("Tarea 1: El servidor web")
    print("Integrantes:")
    print("  - Cruz Vargas Emilio")
    print("  - Garciliano Díaz Giovanni Alfredo")
    print("\nUso: " + sys.argv[0] + " NUM_HILOS")
    sys.exit(1)

try:
    jefe_trabajador = servidor(numTrabajadores)

    peticion = 0
    while True:
        # Pasar peticiones
        jefe_trabajador.asignar_peticion(peticion)
        peticion += 1
        time.sleep(random.uniform(.1,.3))
except:
    print("adiós")