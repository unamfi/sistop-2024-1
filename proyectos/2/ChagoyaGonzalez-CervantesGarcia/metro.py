import threading
import time
import random

# Multiplex para que 3 trenes puedan entrar a la estacion
estacion  = threading.Semaphore(3)

#mutex para evitar que un tren quiera entrar donde hay otro
m_carrilA  = threading.Lock()
m_carrilB  = threading.Lock()
m_carrilC  = threading.Lock()
id_carriles = {'A':0, 'B':1, 'C':2}
id_carriles_inv = {0:'A', 1:'B', 2:'C'}
carriles = ['Empty','Empty','Empty']

#Para proteger la variable que asigna carrriles
m_eleccion = threading.Semaphore(1)

#mutex para controlar la salida de los metros
m_salida  = threading.Lock()

# Función para que el metro elija por cual carril quiere entrar
def metroElige(num):
    #METER AQUI LA ELECCIPON DE CARRIL PARA QUE SE COMPAGINE CON EL MULTIPLEX
    carril = random.choice(['A','B','C'])
    return carril

# Función para que un metro se coloque en un carril y se marche después de un tiempo
def llegaMetro(numMetro):

    #el metro intenta entrar a la estación
    estacion.acquire()
    print(f'Metro {numMetro} puede entrar en la estación.')

    #el metro elige carril
    m_eleccion.acquire()
    carril = metroElige(numMetro)

    #el metro llega al carril
    if id_carriles[carril] == 0:
        with m_carrilA:
            print(f'\n---El estado de los carriles es:\t  A:{carriles [0]}\t B:{carriles [1]}\t C:{carriles [2]}---\n')
            carriles[id_carriles[carril]] = 'Carril A: ocupado por metro:%d' % numMetro
            print(f'Metro {numMetro} llegó al carril A')
            m_eleccion.release()
            print(f'\n---El estado de los carriles es:\t  A:{carriles [0]}\t B:{carriles [1]}\t C:{carriles [2]}---\n')
            time.sleep(random.uniform(0.01, 0.05))
            salida(numMetro, 0)
            print(f'\n---El estado de los carriles es:\t  A:{carriles [0]}\t B:{carriles [1]}\t C:{carriles [2]}---\n')
        
    elif id_carriles[carril] == 1:
        with m_carrilB:
            print(f'\n---El estado de los carriles es:\t  A:{carriles [0]}\t B:{carriles [1]}\t C:{carriles [2]}---\n')
            carriles[id_carriles[carril]] = 'Carril B: ocupado por metro:%d' % numMetro
            print(f'Metro {numMetro} llegó al carril B')
            m_eleccion.release()
            print(f'\n---El estado de los carriles es:\t  A:{carriles [0]}\t B:{carriles [1]}\t C:{carriles [2]}---\n')
            time.sleep(random.uniform(0.01, 0.05))
            salida(numMetro, 1)
            print(f'\n---El estado de los carriles es:\t  A:{carriles [0]}\t B:{carriles [1]}\t C:{carriles [2]}---\n')

    elif id_carriles[carril] == 2:
        with m_carrilC:
            print(f'\n---El estado de los carriles es:\t  A:{carriles [0]}\t B:{carriles [1]}\t C:{carriles [2]}---\n')
            carriles[id_carriles[carril]] = 'Carril C: ocupado por metro:%d' % numMetro
            print(f'Metro {numMetro} llegó al carril C')
            m_eleccion.release()
            print(f'\n---El estado de los carriles es:\t  A:{carriles [0]}\t B:{carriles [1]}\t C:{carriles [2]}---\n')
            time.sleep(random.uniform(0.01, 0.05))
            salida(numMetro, 2)
            print(f'\n---El estado de los carriles es:\t  A:{carriles [0]}\t B:{carriles [1]}\t C:{carriles [2]}---\n')
    

def salida(numMetro, carril):
    #el metro abre sus puertas
    print(f'Metro {numMetro} abre las puertas ')
    time.sleep(random.uniform(0.01, 0.05))  # Tiempo en que las puertas estan abiertas
    #el metro cierra sus puertas
    print(f'Metro {numMetro} cierra las puertas')
    print(f'\n---El estado de los carriles es:\t  A:{carriles [0]}\t B:{carriles [1]}\t C:{carriles [2]}---\n')

    # Controlamos la salida de los metros
    with m_salida: #este mutex nos ayuda a que no puedan salir dos carrilles al mismo tiempo 
        print(f'Metro {numMetro} sale de la terminal dejando libre el carril {id_carriles_inv[carril]}')
        carriles[carril] = 'Empty'
        estacion.release()

def main ():
    # Crear e iniciar los hilos de los metros, por cada metro un hilo
    for i in range(1, 15): 
        threading.Thread(target=llegaMetro, args=[i]).start()

main()