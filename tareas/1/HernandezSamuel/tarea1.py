import threading
import time
import random

num_sillas = 3
cubiculo = threading.Semaphore(num_sillas)
mutex = threading.Semaphore(1)
preguntas_por_estudiante = 3
preguntas_totales = 10  # Número total de preguntas para la simulación

def profesor():
    preguntas_respondidas = 0
    while preguntas_respondidas < preguntas_totales:
        # El profesor está durmiendo
        print("El profesor está durmiendo...zzz")

        # Espera a que un estudiante toque la puerta
        cubiculo.acquire()

        # El profesor se despierta cuando un estudiante toca la puerta
        print("El profesor se despierta y atiende al estudiante.")
        time.sleep(1)  # Simula la respuesta del profesor
        print("El profesor ha terminado de atender al estudiante.")
        cubiculo.release()
        preguntas_respondidas += 1
        
def estudiante(numero):
    preguntas_hechas = 0
    while preguntas_hechas < preguntas_por_estudiante:
        # El estudiante quiere hacer una pregunta
        print(f"Estudiante {numero} quiere hacer una pregunta.")
        cubiculo.acquire()

        # El estudiante entra al cubículo
        print(f"Estudiante {numero} entra al cubículo.")

        # El profesor se despierta y atiende al estudiante
        mutex.acquire()
        print("El profesor se despierta y atiende al estudiante.")

        # Realiza su pregunta
        print(f"Estudiante {numero} pregunta al profesor.")
        time.sleep(1)  # Simula la respuesta del profesor
        preguntas_hechas += 1

        # Termina su turno
        print("El profesor ha terminado de atender al estudiante.")
        mutex.release()

        # Sale del cubículo
        print(f"Estudiante {numero} sale del cubículo.")
        cubiculo.release()

        # Espera un tiempo aleatorio antes de hacer otra pregunta
        time.sleep(random.uniform(1, 5))  # Espera aleatoria

# Crear al profesor
profesor_thread = threading.Thread(target=profesor)

# Crear estudiantes
estudiantes = []
num_estudiantes = 5
for i in range(num_estudiantes):
    estudiante_thread = threading.Thread(target=estudiante, args=(i + 1,))
    estudiantes.append(estudiante_thread)

# Iniciar al profesor
profesor_thread.start()

# Iniciar los hilos de los estudiantes
for estudiante_thread in estudiantes:
    estudiante_thread.start()

# Esperar a que los estudiantes terminen
for estudiante_thread in estudiantes:
    estudiante_thread.join()

# Finaliza el hilo del profesor cuando todos los estudiantes han terminado
profesor_thread.join()
