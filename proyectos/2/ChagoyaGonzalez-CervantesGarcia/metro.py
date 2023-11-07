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

# Semáforos para controlar la apertura de las puertas de cada carril
semPuertasA = threading.Semaphore(0)
semPuertasB = threading.Semaphore(0)
semPuertasC = threading.Semaphore(0)

#
listaEspera=[]

m_persona = threading.Lock()
m_listaEspera = threading.Lock()

# Función para que el metro elija por cual carril quiere entrar
def carrilEleccion():
    carril = random.choice(['A','B','C'])
    return carril

# Función que simula la estancia del metro en un carril y su salida
def gestiondeCarriles(numMetro, carril, c_id):
    print(f'\n---El estado de los carriles es:\t  A:{carriles [0]}\t B:{carriles [1]}\t C:{carriles [2]}---\n')
    carriles[id_carriles[carril]] = f'Ocupado por metro:{numMetro}'
    print(f'Metro {numMetro} llegó al carril {id_carriles_inv[c_id]}')
    m_eleccion.release()
    print(f'\n---El estado de los carriles es:\t  A:{carriles [0]}\t B:{carriles [1]}\t C:{carriles [2]}---\n')
    time.sleep(random.uniform(0.01, 0.05))
    salida(numMetro, c_id)
    print(f'\n---El estado de los carriles es:\t  A:{carriles [0]}\t B:{carriles [1]}\t C:{carriles [2]}---\n')

# Función para que un metro se coloque en un carril y se marche después de un tiempo
def llegaMetro(numMetro):           
    #el metro intenta entrar a la estación
    estacion.acquire()
    print(f'Metro {numMetro} puede entrar en la estación.')
    #el metro elige carril
    m_eleccion.acquire()
    carril = carrilEleccion()

    #el metro llega al carril
    if id_carriles[carril] == 0:
        with m_carrilA:
            gestiondeCarriles(numMetro, carril, 0)           
    elif id_carriles[carril] == 1:
        with m_carrilB:
            gestiondeCarriles(numMetro, carril, 1)
    elif id_carriles[carril] == 2:
        with m_carrilC:
            gestiondeCarriles(numMetro, carril, 2)

def salida(numMetro, carril):
    #el metro abre sus puertas
    print(f'Metro {numMetro} abre las puertas ')

    if(carril==0):
        semPuertasA.release()
    elif(carril==1):
        semPuertasB.release()
    elif(carril==2):
        semPuertasC.release()
    
    time.sleep(random.uniform(0.01, 0.05))  # Tiempo en que las puertas estan abiertas
    #el metro cierra sus puertas
    print(f'Metro {numMetro} cierra las puertas')
    print(f'\n---El estado de los carriles es:\t  A:{carriles [0]}\t B:{carriles [1]}\t C:{carriles [2]}---\n')

    # Controlamos la salida de los metros
    with m_salida: #este mutex nos ayuda a que no puedan salir dos carrilles al mismo tiempo 
        print(f'Metro {numMetro} sale de la terminal dejando libre el carril {id_carriles_inv[carril]}')
        carriles[carril] = 'Empty'
        estacion.release()
    
    
def persona(numPersona):
    with m_persona:
        print(f'Persona {numPersona} llega a la estación ')
        listaEspera.append(numPersona)
        llegadaPersona(numPersona)

def abordaPersona(numPersona, carril):
    print(f'**Persona {numPersona} decide abordar el metro del carril {carril}.')
    listaEspera.remove(numPersona)

def llegadaPersona(numPersona):
        time.sleep(random.uniform(0.01,0.05))
        carrilMetro = carrilEleccion()
        if (carrilMetro == 'A' and carriles[0]!='Empty'):
            semPuertasA.acquire()
            abordaPersona(numPersona, id_carriles_inv[0])
            semPuertasA.release()  # Liberar el semáforo después de abordar
        elif (carrilMetro == 'B' and carriles[1]!='Empty'):
            semPuertasB.acquire()
            abordaPersona(numPersona, id_carriles_inv[1])
            semPuertasB.release()  # Liberar el semáforo después de abordar
        elif (carrilMetro == 'C' and carriles[2]!='Empty' ):
            semPuertasC.acquire()
            abordaPersona(numPersona, id_carriles_inv[2])
            semPuertasC.release()  # Liberar el semáforo después de abordar
        else:
            print(f'Persona {numPersona} está esperando para abordar {carrilMetro}.')

def main ():
    for i in range(1,10):
        threading.Thread(target=persona, args=[i]).start()

    # Crear e iniciar los hilos de los metros, por cada metro un hilo
    var=1
    while(len(listaEspera)>0 and var==1):
        for i in range(5): 
            threading.Thread(target=llegaMetro, args=[i]).start()
            var=var+1
main()