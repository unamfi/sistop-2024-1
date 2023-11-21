import threading
import time
import random

# Clase que representa una parada de autobuses
class Parada:
    def __init__(self):
        self.pasajeros_esperando = 0
        self.lock = threading.Lock()  # Controlar el acceso a la parada
        self.esperando = [0,0,0,0,0,0]

    # Método para que un pasajero llegue a la parada
    def llegar_pasajero(self,ruta):
        #with self.lock:  # Adquirir el cerrojo antes de que llegue un pasajero
        for espera in range (buses):
            self.esperando[espera] = self.pasajeros_esperando + 1
            print(f"Un pasajero llegó a la parada de ruta {ruta[espera]}. Pasajeros esperando: {self.esperando[espera]}\n")

    # Método para que un Pumabus recoja pasajeros de la parada
    def recoger_pasajeros(self, autobus, capacidad):
        with self.lock:  # Adquirir el cerrojo antes de que el Pumabus recoja pasajeros
            if (capacidad == 0):
                print(f"{autobus} ya no tiene lugares\n")
            time.sleep(5)
            pasajeros_a_subir = random.randint(0,10)
            capacidad -= pasajeros_a_subir
            self.esperando[buses[]] = self.pasajeros_esperando - pasajeros_a_subir
            print(f"{autobus} recogió a {pasajeros_a_subir} pasajeros. Pasajeros esperando: {self.pasajeros_esperando}\n")
            print(f"El Autobus {autobus} cuenta con {capacidad} lugares\n")
# Función que simula un Pumabus llegando a la parada y recogiendo pasajeros
def autobus(parada, nombre, capacidad):
    for _ in range(buses):  # Simulamos tres visitas del Pumabus
        print(f"{nombre} llegó a la parada.")
        parada.recoger_pasajeros(nombre, capacidad)
        time.sleep(2)   # Simulamos un breve tiempo de espera entre visitas

# Función que simula un pasajero llegando a la parada
def pasajero(parada):
    while True:  # Simulamos cinco pasajeros llegando a la parada
        parada.llegar_pasajero(ruta)
        time.sleep(5)
        
capacidad = [40,50,30,48,60,41]
# Crear una instancia de la parada de autobuses
parada1 = Parada()

ruta = ["Pumabus Ruta 9","Pumabus Ruta 1","Pumabus Ruta 7","Pumabus Ruta 6","Pumabus Ruta 2","Pumabus Ruta 10"]
buses = len(ruta)
# Crear tres hilos para simular tres autobuses que llegan a la parada
for pumabus in range(5):
    autobuses=[threading.Thread(target = autobus, args =(parada1,ruta[pumabus],capacidad[pumabus])).start() for pumabus in range (5)]
# Crear un hilo para simular la llegada de pasajeros a la parada
hilo_pasajeros1 = threading.Thread(target=pasajero, args=(parada1,)).start()



print("Todas las operaciones de llegada y recogida han terminado.")

