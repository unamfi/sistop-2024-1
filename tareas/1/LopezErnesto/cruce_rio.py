from colorama import Fore
import threading
import time
import random

"""
    Problema "El cruce del río": Para llegar a un encuentro de desarrolladores de sistemas operativos, hace
    falta cruzar un río en balsa.

    Los desarrolladores podrían pelearse entre sí, hay que cuidar que vayan con un balance adecuado.

    Reglas:

    -   En la balsa caben cuatro (y sólo cuatro) personas (con menos de cuatro se puede volcar).
    
    -   Al encuentro están invitados hackers (desarrolladores de Linux) y serfs (desarrolladores de Microsoft)
        - Para evitar peleas, debe mantenerse un buen balance: No debes permitir que aborden tres hackers y un serf,
          o tres serfs y un hacker. Pueden subir cuatro del mismo bando o dos y dos

    - Hay sólo una balsa.

    - No tenemos que preocuparnos por devolver la balsa.
"""

# Variables necesarias

"""
    En este caso se tienen los siguientes elementos:
    1. Balsa -> Es una barrera que permitirá el acceso de 4 hilos para llegar a la convención
    2. Las filas ayudan a llvear un conteo de los hilos que están dormidos de cada tipo de desarrollador
    3. La lista de los cruzados se utiliza para dar una representación gráfica de lo que está sucediendo
    4. Mutex -> Nos ayuda a tener un control de la zona crítica de acceso de los desarrolladores
"""
balsa = threading.Barrier(4)
filaHackers = []
filaSerfs = []
serfsCruzados = []
hackersCruzados = []
colaHackers = threading.Semaphore(0)
colaSerfs = threading.Semaphore(0)
mutex = threading.Semaphore(1)

# El verde será para los Serfs, el rojo para los hackers, el azul para el agua, el amarillo para la arena y el blanco para la balsa
colores = [Fore.GREEN, Fore.RED, Fore.BLUE, Fore.WHITE, Fore.YELLOW]

# Es importante considerar el órden en el que llegan los respectivos desarrolladores
# Hay dos tipos de hilos principales: Hackers y serfs.

def hacker(x):
    # En este caso, llega un hacker
    global filaHackers, filaSerfs
    hilo_jefe = False
    mutex.acquire()
    pasajeros = []
    filaHackers.append(x)
    # clear()
    imprimirASCII()
    # Debemos analizar los posibles casos
    if (len(filaHackers) >= 2 and len(filaSerfs) >= 2):
        # En este caso, la fila tiene la posibilidad de un balance 2 y 2, por lo que se procede a utilizar la balsa
        """
            - La lista de pasajeros es de utilidad para la representación gráfica que se realiza del problema.
            - Con esto, se liberan dos hilos de cada uno de los programadores y se eliminan de la cola de espera.
            - Se asigna un hilo jefe que servirá para liberar el mutex, el cual se encuentra bloqueado mientras se realiza
            la navegación
        """
        pasajeros = [2,2]
        colaHackers.release(2)
        hackersCruzados.append(filaHackers.pop(0))
        hackersCruzados.append(filaHackers.pop(0))
        colaSerfs.release(2)
        serfsCruzados.append(filaSerfs.pop(0))
        serfsCruzados.append(filaSerfs.pop(0))
        hilo_jefe = True
    elif len(filaHackers) >= 4:
        # En este caso, hay insuficiencia de desarrolladores Microsoft, por lo mismo, mandamos a puros hackers
        """
            - En este caso se liberan 4 hilos asociados a hackers y se procede de la misma manera
        """
        pasajeros = [4,0]
        colaHackers.release(4)
        hackersCruzados.append(filaHackers.pop(0))
        hackersCruzados.append(filaHackers.pop(0))
        hackersCruzados.append(filaHackers.pop(0))
        hackersCruzados.append(filaHackers.pop(0))
        hilo_jefe = True
    else:
        """
            Cuando no se cumple ninguna condición, el hilo libera el mutex y se queda en la zona de espera para abordar la balsa
        """
        mutex.release()
    
    # Aquí estarán los hilos esperando a subir a la balsa
    colaHackers.acquire()
    # Aquí se recibirá el número de hilos adecuados
    balsa.wait()
    """
        En este punto ingresan los 4 desarrolladores y abordar la balsa
    """
    if hilo_jefe:
        hilo_jefe = False
        navegar(pasajeros)
        """Una vez que se navegó, se libera el mutex"""
        mutex.release()


def serf(x):
    """
        El caso de los desarrolladores de Windows sigue el mismo comportamiento que los desarrolladores de Linux.
    """
    # En este caso, llega un serf
    global filaHackers, filaSerfs
    hilo_jefe = False
    mutex.acquire()
    pasajeros = []
    filaSerfs.append(x)
    # clear()
    imprimirASCII()
    # Debemos analizar los posibles casos
    if (len(filaHackers) >= 2 and len(filaSerfs) >= 2):
        # En este caso, la fila tiene la posibilidad de un balance 2 y 2, por lo que se procede a utilizar la balsa
        pasajeros = [2,2]
        colaHackers.release(2)
        hackersCruzados.append(filaHackers.pop(0))
        hackersCruzados.append(filaHackers.pop(0))
        colaSerfs.release(2)
        serfsCruzados.append(filaSerfs.pop(0))
        serfsCruzados.append(filaSerfs.pop(0))
        hilo_jefe = True
    elif len(filaSerfs) >= 4:
        # En este caso, hay insuficiencia de desarrolladores Microsoft, por lo mismo, mandamos a puros hackers
        pasajeros = [0,4]
        colaSerfs.release(4)
        serfsCruzados.append(filaSerfs.pop(0))
        serfsCruzados.append(filaSerfs.pop(0))
        serfsCruzados.append(filaSerfs.pop(0))
        serfsCruzados.append(filaSerfs.pop(0))
        hilo_jefe = True
    else:
        mutex.release()
    
    # Aquí estarán los hilos esperando a subir a la balsa
    colaSerfs.acquire()
    # Aquí se recibirá el número de hilos adecuados
    balsa.wait()
    if hilo_jefe:
        hilo_jefe = False
        navegar(pasajeros)
        mutex.release()
    
def imprimirASCII():
    """
        Esta función imprime un pequeño esquema de la situación con la fila, la balsa y el otro lado del río.
    """
    print(colores[4] + "XXXXXX" + colores[2] + "XXXXXXXXXX" + colores[4] + "XXXXXX")
    print(colores[4] + "XXXXXX" + colores[2] + "XXXXXXXXXX" + colores[4] + "XXXXXX")
    print(colores[4] + "XXXXXX" + colores[2] + "XXXXXXXXXX" + colores[4] + "XXXXXX")
    print(colores[0] + f"   {len(filaSerfs)}  " + colores[3] + "XXXXX" + colores[2] + "XXXXX" + colores[0] + f"   {len(serfsCruzados)}  ")
    print(colores[1] + f"   {len(filaHackers)}  " + colores[3] + "XXXXX" + colores[2] + "XXXXX" + colores[1] + f"   {len(hackersCruzados)}  ")
    print(colores[4] + "XXXXXX" + colores[2] + "XXXXXXXXXX" + colores[4] + "XXXXXX")
    print(colores[4] + "XXXXXX" + colores[2] + "XXXXXXXXXX" + colores[4] + "XXXXXX")
    print(colores[4] + "XXXXXX" + colores[2] + "XXXXXXXXXX" + colores[4] + "XXXXXX")
    print(end="\n\n")

# Revisar
def navegar(pasajeros):
    """
        Se imprime el comportamiento de la navegación
    """
    print("Navegando!", end="\n\n")

    print(colores[4] + "XXXXXX" + colores[2] + "XXXXXXXXXX" + colores[4] + "XXXXXX")
    print(colores[4] + "XXXXXX" + colores[2] + "XXXXXXXXXX" + colores[4] + "XXXXXX")
    print(colores[4] + "XXXXXX" + colores[2] + "XXXXXXXXXX" + colores[4] + "XXXXXX")
    print(colores[0] + f"   {len(filaSerfs)}  " + colores[3] + "XX" + colores[0] + f"{pasajeros[1]}" + colores[3] + "XX" + colores[2] + "XXXXX" + colores[0] + f"   {len(serfsCruzados) - pasajeros[1]}  ")
    print(colores[1] + f"   {len(filaHackers)}  " + colores[3] + "XX" + colores[1] + f"{pasajeros[0]}" + colores[3] + "XX" + colores[2] + "XXXXX" + colores[1] + f"   {len(hackersCruzados) - pasajeros[0]}  ")
    print(colores[4] + "XXXXXX" + colores[2] + "XXXXXXXXXX" + colores[4] + "XXXXXX")
    print(colores[4] + "XXXXXX" + colores[2] + "XXXXXXXXXX" + colores[4] + "XXXXXX")
    print(colores[4] + "XXXXXX" + colores[2] + "XXXXXXXXXX" + colores[4] + "XXXXXX")
    print(end="\n\n")

    print("Llegando!", end="\n\n")
    
    print(colores[4] + "XXXXXX" + colores[2] + "XXXXXXXXXX" + colores[4] + "XXXXXX")
    print(colores[4] + "XXXXXX" + colores[2] + "XXXXXXXXXX" + colores[4] + "XXXXXX")
    print(colores[4] + "XXXXXX" + colores[2] + "XXXXXXXXXX" + colores[4] + "XXXXXX")
    print(colores[0] + f"   {len(filaSerfs)}  " + colores[2] + "XXXXX" + colores[3] + "XXXXX" + colores[0] + f"   {len(serfsCruzados)}  ")
    print(colores[1] + f"   {len(filaHackers)}  " + colores[2] + "XXXXX" + colores[3] + "XXXXX" + colores[1] + f"   {len(hackersCruzados)}  ")
    print(colores[4] + "XXXXXX" + colores[2] + "XXXXXXXXXX" + colores[4] + "XXXXXX")
    print(colores[4] + "XXXXXX" + colores[2] + "XXXXXXXXXX" + colores[4] + "XXXXXX")
    print(colores[4] + "XXXXXX" + colores[2] + "XXXXXXXXXX" + colores[4] + "XXXXXX")
    print(end="\n\n")

# Quitar el comentario si se desea un comportamiento predefinido de los hilos

"""entrada = "LLWLWLLL"

imprimirASCII()
time.sleep(0.5)
for w in entrada:
    time.sleep(random.random())
    if w == "L":
        threading.Thread(target=hacker,args=["L"]).start()
    else:
        threading.Thread(target=serf,args=["S"]).start()"""


# Mandando hilos de forma aleatoria

imprimirASCII()
time.sleep(0.5)
while True:
    time.sleep(random.random())
    if random.randint(0,1) == 0:
        threading.Thread(target=hacker,args=["L"]).start()
    else:
        threading.Thread(target=serf,args=["S"]).start()