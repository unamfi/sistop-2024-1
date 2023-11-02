import random
from threading import Thread, Barrier, Semaphore
from time import sleep

"""
    Se tiene el caso del restaurante Casa de Toño. En este, se tiene un total de 4 mesas para 4 personas,
    4 mesas para 2 personas y 4 mesas para 1 persona. Conforme van llegando los clientes, se tiene que validar que haya una mesa
    disponible para la cantidad de personas que forman el grupo. El problema siguiente se encarga de gestionar la fila de Casa
    de Toño.

    En este caso se quiere evitar que el restaurante sobrepase el límite de personas que pueden estar dentro. Igualmente, se requiere que
    únicamente se vaya avisando a cada una de las familias con el respectivo turno (siempre que se libere una mesa para esa cantidad) que
    puede acceder al restaurante.
"""
# Número de familias esperadas
num_familias = 50

# Tamaños de familia
tamaños = [1,2,4]

# Definimos el número de mesas por tamaño
mesaParaCuatro = 4
mesaParaDos = 4
mesaParaUno = 2
multiplexCuatro = Semaphore(mesaParaCuatro)
multiplexDos = Semaphore(mesaParaDos)
multiplexUno = Semaphore(mesaParaUno)

mutexLlegada = Semaphore(1)

# Cola de gente esperando por categoria
colaUno = {}
colaDos = {}
colaCuatro = {}

# Comiendo
comiendo = {}

def llegaFamilia(fam,tam):
    mutexLlegada.acquire() # Se entra a una zona crítica
    print(comiendo)
    print(f"La familia {fam} de tamaño {tam} llegó al establecimiento")
    # Se deberá de validar la disponibilidad para este tamaño de familia
    if tam == 1:
        # Se debe de verificar que haya mesa para una persona
        mutexLlegada.release()
        colaUno[fam] = tam
        multiplexUno.acquire()
        comiendo[fam] = tam
        del colaUno[fam]
        # Tendrá un tiempo específico
        sleep(random.random() * 20)
        print(f"La familia {fam} de tamaño {tam} terminó de comer")
        # En este caso, se desocupa el lugar y se van 
        del comiendo[fam]
        multiplexUno.release()
        pass
    elif tam == 2:
        # Se debe de verificar que haya mesa para dos personas
        mutexLlegada.release()
        colaDos[fam] = tam
        print(colaDos)
        multiplexDos.acquire()
        comiendo[fam] = tam 
        del colaDos[fam]
        sleep(random.random() * 20)
        print(f"La familia {fam} de tamaño {tam} terminó de comer")
        del comiendo[fam]
        multiplexDos.release()
        pass
    else:
        # Se debe de verificar que haya mesa para cuatro personas
        mutexLlegada.release()
        colaCuatro[fam] = tam
        print(colaCuatro)
        multiplexCuatro.acquire()
        comiendo[fam] = tam
        del colaCuatro[fam]
        sleep(random.random() * 20)
        print(f"La familia {fam} de tamaño {tam} terminó de comer")
        del comiendo[fam]
        multiplexCuatro.release()
        pass
    pass


# Consideraremos un flujo de 50 familias que irán llegando al restaurante:
for i in range(50):
    sleep(random.random())
    # La familia tendrá un tamaño aleatorio de 4, 2 o 1
    Thread(target=llegaFamilia,args=[i,tamaños[random.randint(0,2)]]).start()