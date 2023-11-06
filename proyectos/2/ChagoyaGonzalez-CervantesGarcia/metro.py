import threading
import time
import random

# Declaramos semaforos uno por cada carril 
semA = threading.Semaphore(1)
semB = threading.Semaphore(1)
semC = threading.Semaphore(1)

#mtex para controlar la salida de los metros
mutex = threading.Lock()

# Función para que el metro elija por cual carril quiere entrar
def metroElige(num):
    carril = random.choice(['A', 'B', 'C'])
    llegaMetro(num, carril)


# Función para que un metro se coloque en un carril y se marche después de un tiempo
def llegaMetro(numMetro, carril):

    #Deacuerdo a carril es e
    if carril == 'A':
        semA.acquire()
    elif carril == 'B':
        semB.acquire()
    elif carril == 'C':
        semC.acquire()

    #el metro llega al carril
    print(f'Metro {numMetro} llegó al carril {carril}.')
    time.sleep(random.randint(1,10))  # Tiempo para abrir las puertas

    #el metro abre sus puertas
    print(f'Metro {numMetro} abre las puertas ')
    time.sleep(random.randint(1,10))  # Tiempo en que las puertas estan abiertas
    
    #el metro cierra sus puertas
    print(f'Metro {numMetro} cierra las puertas')

    # Controlamos la salida de los metros
    with mutex: #este mutex nos ayuda a que no puedan salir dos carrilles al mismo tiempo 
        if carril == 'A':
            semA.release()
        elif carril == 'B':
            semB.release()
        elif carril == 'C':
            semC.release()
        print(f'Metro {numMetro} sale de la terminal dejando libre el carril {carril}')

        



# Lista para almacenar los hilos de los metros
threads_metros = []

# Crear e iniciar los hilos de los metros, por cada metro un hilo
for i in range(1, 10): 
    metro_thread = threading.Thread(target=metroElige, args=(i,))
    metro_thread.start() 
    threads_metros.append(metro_thread) #agregamos a aquellos que ya terminaron a una lista

# Esperar a que todos los hilos de los metros terminen su ejecución
for metro_thread in threads_metros:
    metro_thread.join()

print("Ejecución terminada.")