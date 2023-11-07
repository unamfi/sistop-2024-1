import threading
import time

LINES = 5 # Se define las líneas disponibles (depende de la compañía)
llamadas = [] # Cola para llamadas en espera 
linesAccess = threading.Semaphore(LINES) # Semáforo para controlar el acceso a las líneas disponibles

# Clase para representar a los usuarios (receptores)
"""
        Inicializa un usuario con un nombre y un estado inicial no ocupado.

        Args:
            name (str): El nombre del usuario.
"""
class User:
    def __init__(self, name):
        self.name = name
        self.busy = False

# Función para realizar una llamada
"""
    Simula una llamada telefónica entre un emisor y un receptor.

    Args:
        sender (str): El nombre del emisor.
        receiver (User): El receptor que recibe la llamada.
"""
def llamar(emisor, receptor):
    linesAccess.acquire()
    if not receptor.busy:
        receptor.busy = True
        print(f"{emisor} está llamando a {receptor.name}") #
        time.sleep(2)  # Simular el tiempo de una llamada
        receptor.busy = False
        linesAccess.release()
        print(f"{receptor.name} ha respondido la llamada de {emisor}") #
    else:
        print(f"La línea de {receptor.name} está ocupada. {emisor} ha sido encolado.") #
        llamadas.append((emisor, receptor))

# Función para encolar llamadas pendientes
"""
    Gestiona las llamadas en cola y las asigna cuando los receptores están disponibles.
"""
def manejador():
    while True:
        if llamadas:
            emisor, receptor = llamadas.pop(0)
            llamar(emisor, receptor)

# Crear objetos usuarios
user1 = User("Pepe el grillo")
user2 = User("Toño marinela")

# Iniciar un hilo para gestionar las llamadas en cola
llamadasGestion = threading.Thread(target=manejador)
llamadasGestion.start()

# Simular múltiples emisores tratando de contactarse con múltiples receptores
emisores = ["Abuelita", "Hermano", "Prima"]
receptores = [user1, user2]

# Simular llamadas
print(f"Bienvenido!")
print(f"Son las 08:00 am y empezó la jornada laboral, hoy tenemos {LINES} disponibles y nuestros usuarios son: {user1.name} y {user2.name}.")
print(f"Importante considerar los emisores de hoy: {emisores}\n")

print(f"Importante saber que ")
for _ in range(10):
    emisor = emisores.pop(0)
    receptor = receptores.pop(0)
    emisores.append(emisor)
    receptores.append(receptor)
    llamar(emisor, receptor)
    time.sleep(1)  # Esperar antes de realizar la siguiente llamada
