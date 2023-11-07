import tkinter as tk
from threading import Semaphore, Thread, Barrier
from time import sleep
from random import randint

N = 10  # Tolerancia de pasajeros en el metro
M = 5   # Tolerancia de pasajeros esperando afuera

# Semáforos y variables de condición
debeLevantarse = Semaphore(0) # Señalización
puedeSentarse = Semaphore(0)  # 'Apagador' 
puertaMetro = Semaphore(1)     # Control de acceso al metro
metroAbierto = False
pasajerosDentro = 0
barreraAbordo = Barrier(N, action=lambda: puedeSentarse.release())

# Variable compartida para almacenar el estado del metro
estado_metro = {"pasajeros_dentro": pasajerosDentro, "puertas_abiertas": metroAbierto}
mutex = Semaphore(1) # Mutex para proteger el acceso a la variable compartida

def pasajero(id):
    global pasajerosDentro, estado_metro

    puedeSentarse.acquire()
    print(f'Pasajero {id} intentando subir al metro...')

    puertaMetro.acquire()
    pasajerosDentro += 1
    estado_metro["pasajeros_dentro"] = pasajerosDentro

    if pasajerosDentro == N:
        puertaMetro.release()
        debeLevantarse.release()
    else:
        puertaMetro.release()

    barreraAbordo.wait()

    puertaMetro.acquire()
    pasajerosDentro -= 1
    estado_metro["pasajeros_dentro"] = pasajerosDentro
    if pasajerosDentro == 0:
        puertaMetro.release()
    else:
        puertaMetro.release()

    print(f'Pasajero {id} ha bajado del metro.')

def metro():
    global pasajerosDentro, metroAbierto, estado_metro

    while True:
        debeLevantarse.acquire()

        puertaMetro.acquire()
        pasajerosDentro = 0
        estado_metro["pasajeros_dentro"] = pasajerosDentro
        metroAbierto = True
        estado_metro["puertas_abiertas"] = metroAbierto
        puertaMetro.release()

        print('Metro abierto. Pasajeros subiendo...')

        sleep(randint(3, 5))

        puertaMetro.acquire()
        metroAbierto = False
        estado_metro["puertas_abiertas"] = metroAbierto
        puertaMetro.release()

        print('Metro llegó a la siguiente estación y cerró puertas.')

        barreraAbordo.wait()

# Hilo que controla la generación de pasajeros
def llegadaPasajeros():
    i = 1
    while True:
        if randint(0, 2) == 0:
            Thread(target=pasajero, args=[i]).start()
            i += 1
        sleep(1)

# Hilo de actualización de la GUI
def update_gui():
    global estado_metro

    root = tk.Tk()
    root.title("Simulación Metro")

    label1 = tk.Label(root, text="Estado del Metro")
    label1.pack()

    label2 = tk.Label(root, text="Pasajeros dentro: 0")
    label2.pack()

    label3 = tk.Label(root, text="Puertas abiertas: False")
    label3.pack()

    root.geometry("300x200")

    def refresh():
        mutex.acquire()
        label2.config(text="Pasajeros dentro: " + str(estado_metro["pasajeros_dentro"]))
        label3.config(text="Puertas abiertas: " + str(estado_metro["puertas_abiertas"]))
        mutex.release()
        root.after(1000, refresh)

    refresh()

    root.mainloop()

# Iniciar hilos
Thread(target=metro).start()
Thread(target=llegadaPasajeros).start()
Thread(target=update_gui).start()
