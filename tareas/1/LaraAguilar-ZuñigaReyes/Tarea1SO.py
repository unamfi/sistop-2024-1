# Tarea 1 de Sistemas Operativos
# Lara Aguilar Christian Abraham
# Zúñiga Reyes Lissett


import threading
import time
import random

# Número de trabajadores (hilos) que se pueden ejecutar simultáneamente
k = 3

# Semáforo para gestionar el acceso a los trabajadores
trabajadores = threading.Semaphore(k)

# Lista de trabajadores disponibles
trabajadores_disponibles = []

# Función que simula la ejecución de un trabajador
def trabajador(hilo):
    while True: # Ciclo infinito para que el trabajador no termine su ejecución nunca (a menos que se cierre el programa).
        print(f"Trabajador {hilo} está durmiendo porque no hay nada que hacer...")
        trabajadores.acquire()

        # Simula la atención de una solicitud de red
        pagina_solicitada = random.randint(1, 10)
        print(f"Trabajador {hilo} atiende la solicitud de la página {pagina_solicitada}.")
        time.sleep(random.uniform(0.5, 2.0))

        # Notificar el rendimiento del trabajador (hilos) al jefe (productor)
        print(f"Trabajador {hilo} ha terminado de atender la página {pagina_solicitada}.")

        # Volver a la lista de trabajadores disponibles para atender solicitudes
        trabajadores_disponibles.append(hilo)
        trabajadores.release()
        
# Inicialización de los trabajadores (hilos).
for i in range(k):
    t = threading.Thread(target = trabajador, args = (i,))
    t.start()
    trabajadores_disponibles.append(i)

# Función que simula el rol del jefe (productor) que asigna las solicitudes a los trabajadores (consumidores).
def jefe():
    while True:
        # Simula la recepción de una solicitud de red
        time.sleep(random.uniform(1, 3))


        if trabajadores_disponibles:
            # Elegir a un trabajador disponible para atender la solicitud
            trabajador_seleccionado = trabajadores_disponibles.pop()
            print(f"Jefe asigna la solicitud a Trabajador {trabajador_seleccionado}.")
            trabajadores.release()  # Despierta al trabajador seleccionado
        else:
            print("No hay trabajadores disponibles en este momento. Esperando...")
            time.sleep(1)

# Inicialización del jefe
jefe_thread = threading.Thread(target = jefe)
jefe_thread.start()

# Esperar a que el jefe y los trabajadores terminen
jefe_thread.join()
for i in range(k):
   trabajadores.acquire()

print("Todos los trabajadores han terminado.")