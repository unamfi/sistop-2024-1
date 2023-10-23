import threading
import random
import time

x = 5  # número de sillas
y = 3  # número de estudiantes que pueden entrar al cubículo
z = 3  # número máximo de preguntas por estudiante

profesor = threading.Semaphore(1)  # profesor durmiendo o atendiendo a un estudiante
sillas = threading.Semaphore(x)   # sillas disponibles
cubiculo = threading.Semaphore(y) # capacidad del cubículo

def estudiante(id):
    print(f"El estudiante {id} llegó.")
    
    # Intentar entrar al cubículo
    if cubiculo.acquire(blocking=False):
        print(f"El estudiante {id} entró al cubículo.")
        
        num_preguntas = random.randint(1, z)
        for i in range(num_preguntas):
            # Tomar una silla
            sillas.acquire()
            print(f"El estudiante {id} tomó una silla.")
            
            # Preguntar al profesor
            profesor.acquire()
            print(f"El estudiante {id} está haciendo la pregunta {i + 1}.")
            time.sleep(1)  # Simulamos el tiempo que tarda en hacer la pregunta
            profesor.release()
            
            # Liberar la silla
            sillas.release()
            print(f"El estudiante {id} liberó una silla.")
            
            if i != num_preguntas - 1:
                print(f"El estudiante {id} permite a otros preguntar.")
                time.sleep(1)  # Esperar para dar oportunidad a otros de preguntar
        
        cubiculo.release()
        print(f"El estudiante {id} salió del cubículo.")
    else:
        print(f"El estudiante {id} no encontró espacio en el cubículo y se fue.")

def monitor_profesor():
    while True:
        if profesor.acquire(blocking=False):
            print("El profesor está durmiendo.")
            profesor.release()
            time.sleep(1800)  # Checar cada 1800 segundos

# Iniciar el hilo del profesor
threading.Thread(target=monitor_profesor).start()

# Simulamos la llegada de 10 estudiantes
for i in range(10):
    threading.Thread(target=estudiante, args=(i,)).start()
    time.sleep(0.5)  # Espera entre la llegada de estudiantes
