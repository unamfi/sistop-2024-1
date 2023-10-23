import threading
import random
import time
from queue import Queue

# Clase Elevador para representar el elevador
class Elevador:
    def __init__(self):
        self.piso_actual = 1
        self.usuarios = []  # Lista de usuarios en el elevador
        self.direccion = 1  # 1 para subir, -1 para bajar
        self.capacidad_maxima = 5
        self.bloqueo = threading.Lock()  # Cerrojo para sincronización
        self.cola = Queue()  # Cola para controlar el acceso de los usuarios al elevador
        self.todos_han_llegado = threading.Event()  # Evento para rastrear si todos los usuarios han llegado

    # Método para mover el elevador
    def mover(self):
        while True:
            time.sleep(1)
            if self.direccion == 1:
                self.piso_actual += 1
            else:
                self.piso_actual -= 1

            print(f'Elevador en el piso {self.piso_actual}')

            with self.bloqueo:
                for usuario in self.usuarios:
                    if usuario.destino == self.piso_actual:
                        print(f'Usuario {usuario.id} ha llegado a su destino en el piso {self.piso_actual}')
                        self.usuarios.remove(usuario)

            if not self.usuarios and self.todos_han_llegado.is_set():
                print(Todos los usuarios han llegado a su destino. Deteniendo el elevador.)
                break

            if self.piso_actual == 5:
                self.direccion = -1
            elif self.piso_actual == 1:
                self.direccion = 1

            self.cola.put(None)

    # Método para agregar un usuario al elevador
    def agregar_usuario(self, usuario):
        with self.bloqueo:
            if len(self.usuarios) < self.capacidad_maxima:
                self.usuarios.append(usuario)
                print(f'Usuario {usuario.id} ha abordado el elevador en el piso {self.piso_actual}')
            else:
                print(f'Elevador lleno, usuario {usuario.id} debe esperar.')

# Clase Usuario para representar a los usuarios
class Usuario:
    def __init__(self, id, origen, destino):
        self.id = id
        self.origen = origen
        self.destino = destino

    # Método para que un usuario ingrese al elevador
    def ingresar_elevador(self, elevador):
        elevador.cola.get()
        elevador.agregar_usuario(self)
        print(f'Usuario {self.id} esperando a llegar al piso {self.destino}')
        if self.origen == self.destino:
            elevador.todos_han_llegado.set()  # Indicar que este usuario ha llegado a su destino

# Función principal para simular el elevador
def simular_elevador():
    elevador = Elevador()
    hilo_elevador = threading.Thread(target=elevador.mover)
    hilo_elevador.daemon = True
    hilo_elevador.start()

    for i in range(10):
        origen = random.randint(1, 5)
        destino = random.randint(1, 5)
        while destino == origen:
            destino = random.randint(1, 5)

        usuario = Usuario(i, origen, destino)
        hilo_usuario = threading.Thread(target=usuario.ingresar_elevador, args=(elevador,))
        hilo_usuario.start()

    hilo_elevador.join()

if __name__ == '__main__':
    simular_elevador()

