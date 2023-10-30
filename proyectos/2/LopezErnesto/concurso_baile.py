import random
import time
from threading import Barrier, Semaphore, Thread

# Es fundamental definir el número de participantes 
num_mujeres = 25
num_hombres = 25

# Se utilizará una barrera para controlar el paso de 5 parejas
# Se utilizará Rendezvous para juntar a las respectivas parejas
mujerLista = Semaphore(0)
hombreListo = Semaphore(0)


# Parejas
# Tienen que pasar 5 mujeres y 5 hombres
parejas = Barrier(10)
mutex_mujeres = Semaphore()
mutex_hombres = Semaphore()

# Llegada de una mujer a la pista
def hombre(numParticipante):
    print(f"Participante hombre: {numParticipante}")
    mutex_hombres.acquire()
    # El hombre señaliza que está listo y a la espera de una pareja
    hombreListo.release()
    # Se espera a la respectiva pareja
    mujerLista.acquire()
    # Una vez listo deberá de pasar a la pista (únicamente pasan 5)
    mutex_hombres.release()
    bailar(numParticipante,'H')

# Llegada de un hombre a la pista
def mujer(numParticipante):
    print(f"Participante mujer: {numParticipante}")
    mutex_mujeres.acquire()
    # La mujer señaliza que está lista y a la espera de una pareja
    mujerLista.release()
    # Se espera a la respectiva pareja
    hombreListo.acquire()
    # Una vez lista deberá de pasar a la pista (únicamente pasan 5)
    mutex_mujeres.release()
    bailar(numParticipante,'M')

def bailar(numParticipante,sexo):
    print(f"{sexo}{numParticipante} listo para entrar a la pista")
    # Se espera a que lleguen los 10 participantes
    parejas.wait()
    # En este punto se tiene que utilizar un apagador para que nadie pueda entrar a la sala 
    print("Entraron las parejas a bailar!")


# Irán llegando los concursantes cada cierto intervalo de tiempo, considerando que se están preparando

while (num_hombres > 0) or (num_mujeres > 0):
    # Se manda a un hombre o una mujer de forma aleatoria
    sexo = random.randint(0,1)
    if sexo == 0 and num_hombres > 0 or num_mujeres == 0: # Se trata de un hombre
        Thread(target=hombre, args=[abs(num_hombres - 25)]).start()
        num_hombres -= 1
    elif num_mujeres > 0 or num_hombres == 0: # se trata de una mujer
        Thread(target=mujer, args=[abs(num_mujeres - 25)]).start()
        num_mujeres -= 1
    else:
        continue