import threading
import time
import random

#MULTIPLEX PARA QUE 3 TRENES PUEDAN ENTRAR A LA ESTACIÓN
estacion  = threading.Semaphore(3)

#Para proteger la variable que asigna carrriles
m_eleccion = threading.Semaphore(1)

#MUTEXES PARA QUE SOLO PUEDA HABER UN TREN POR CARRIL
m_carrilA  = threading.Lock()
m_carrilB  = threading.Lock()
m_carrilC  = threading.Lock()
id_carriles = {'A':0, 'B':1, 'C':2}
id_carriles_inv = {0:'A', 1:'B', 2:'C'}
carriles = ['Empty','Empty','Empty']

#MUTEX PARRA QUE SOLO UN METRO PUEDA SALIR
m_salida  = threading.Lock()

# Semáforos para controlar la apertura de las puertas de cada carril
semPuertasA = threading.Semaphore(0)
semPuertasB = threading.Semaphore(0)
semPuertasC = threading.Semaphore(0)

#SEÑALIZACIONES  PARA SINCRONIZACION DE TRENES Y ABORDO DE PERSONAS
semAndenA = threading.Semaphore(0)
semAndenB = threading.Semaphore(0)
semAndenC = threading.Semaphore(0)
listaEspera=[] #Lista de espera general, sirve para informar a los trenes o hilos de metros si aún deben ejecutarse o no
listaEsperaA=[]
listaEsperaB=[]
listaEsperaC=[]

#Semaforos para proteger la llegada de personas de duplicaciones o eliminaciones no correctas
m_persona = threading.Lock()
m_listaEspera = threading.Lock()

# Función para que el metro elija por cual carril quiere entrar
def carrilEleccion():
    carril = random.choice(['A','B','C'])
    return carril

# Función que simula la estancia del metro en un carril y lo prepara para su salida
def gestiondeCarriles(numMetro, carril, c_id):
    print(f'\n---El estado de los carriles es:\t  A:{carriles [0]}\t B:{carriles [1]}\t C:{carriles [2]}---\n')
    if len(listaEspera) == 1:
        listaEspera.remove(0)
        print(f'\n\t\t !!!LA ESTACION ESTA TERMINANDO OPERACIONES, EL METRO DEL CARRIL: {id_carriles_inv[c_id]}, SALDRÁ VACÍO O NO SALDRÁ Y LOS SIGUIENTES TRENES TAMBIÉN!!!\t\t\n')
    else:
        carriles[id_carriles[carril]] = f'Ocupado por metro:{numMetro}'
        print(f'Metro {numMetro} llegó al carril {id_carriles_inv[c_id]}')
        m_eleccion.release()
        print(f'\n---El estado de los carriles es:\t  A:{carriles [0]}\t B:{carriles [1]}\t C:{carriles [2]}---\n')
        print(f'Metro {numMetro} abre las puertas ')
        time.sleep(random.uniform(0.01, 0.05))

# Función para que un metro se coloque en un carril y se marche después de un tiempo o de haber recibido a algunas personas
def llegaMetro(numMetro): 
    while len(listaEspera) >= 1: #LOS HILOS DE TRENES  SE EJECUTARAN MIENTRRAS HAYA 1 O MÁS PASAJEROS          
        estacion.acquire() #el metro intenta entrar a la estación, si hay algún lugar disponible
        print(f'Metro {numMetro} puede entrar en la estación.')
        m_eleccion.acquire() #el metro elige carril, la variable carril se protege para que no haya cambios o elecciones inesperadas
        carril = carrilEleccion()

        #el metro llega a su carril asigando y realiza operaciones
        if id_carriles[carril] == 0:
            with m_carrilA:   
                gestiondeCarriles(numMetro, carril, 0)
                salida(numMetro, 0, listaEsperaA)        
        elif id_carriles[carril] == 1:
                with m_carrilB:   
                    gestiondeCarriles(numMetro, carril, 1)
                    salida(numMetro, 1, listaEsperaB)
        elif id_carriles[carril] == 2:
                with m_carrilC:
                    gestiondeCarriles(numMetro, carril, 2)
                    salida(numMetro, 2, listaEsperaC)

def salida(numMetro, carril, listaCarril):
    time.sleep(random.uniform(0.01, 0.05))  # Tiempo en que las puertas estan abiertas
    if(carril==0): #EL METRO PIDE PERMISO PARA SALIR, ES DECIR, ESPERA QUE LOS HILOS DE GENTE LE SEÑALIZEN --SEÑALZIACION
        semAndenA.acquire()
    elif(carril==1):
        semAndenB.acquire()
    elif(carril==2):
        semAndenC.acquire()

    #el metro cierra sus puertas
    print(f'Metro {numMetro} cierra las puertas')
    print(f'\n---El estado de los carriles es:\t  A:{carriles [0]}\t B:{carriles [1]}\t C:{carriles [2]}---\n')

    # Controlamos la salida de los metros
    with m_salida: #este mutex nos ayuda a que no puedan salir dos carrilles al mismo tiempo 
        print(f'\n\t\tMetro {numMetro} sale de la terminal dejando libre el carril {id_carriles_inv[carril]}\t\t')
        print(f'Las personas con los ID de tarjeta:{listaCarril} salen de la terminal por el carril {id_carriles_inv[carril]}')
        global listaEspera
        if len(listaEspera) == 1:
            listaEspera.remove(0)
            print(f'\n\t\t !!!LA ESTACION ESTA TERMINANDO OPERACIONES, EL METRO DEL CARRIL: {id_carriles_inv[carril]}, SALDRÁ VACÍO O NO SALDRÁ Y LOS SIGUIENTES TRENES TAMBIÉN!!!\t\t\n')
        else:
            for i in range (len(listaCarril)):
                listaEspera.remove(listaCarril.pop()) #Se vacía la lista de espera del anden con los que se fueron en el metro y también se quitan de la lista general
        carriles[carril] = 'Empty' #Se libera el carril en el arreglo que representa la estación
        estacion.release() #El metro sale de la estación
    print(f'\n---El estado de los carriles es:\t  A:{carriles [0]}\t B:{carriles [1]}\t C:{carriles [2]}---\n')
    #QUIZÁ AQUÍ SE PUEDE AGREGARR UN WAIT PARA SIMULAR EL TIEMPO QUE TARDA EL METRO EN VOLVER A LA TERMINAL
    
    
def llegadaPersona(numPersona):
    with m_persona:
        print(f'Persona {numPersona} llega a la estación ')
        global listaEspera
        listaEspera.append(numPersona)
        gestionPersona(numPersona)

def abordaPersona(numPersona, carril, listaEspera):
    print(f'**Persona {numPersona} decide abordar el metro en el anden {carril}.')
    listaEspera.append(numPersona)

def gestionPersona(numPersona):
    time.sleep(random.uniform(0.01,0.05))
    carrilMetro = carrilEleccion()
    if (carrilMetro == 'A' and numPersona not in listaEsperaA): #Se entrará en cada opción si la persona decide el anden de la opción y no esta ya esperando en el vagon
        abordaPersona(numPersona, id_carriles_inv[0], listaEsperaA)
        semAndenA.release() #LA PERSONA ESTA DENTRO DEL VAGON, POR TANTO EL METRO PUEDE CERRAR PUERTAS SI NO HAY OTRA PERSONA EN LA PUERTA, SEÑALIZA  --- SEÑALIZACION
    elif (carrilMetro == 'B'and numPersona not in listaEsperaB):
        abordaPersona(numPersona, id_carriles_inv[1], listaEsperaB)
        semAndenB.release()
    elif (carrilMetro == 'C' and numPersona not in listaEsperaC):
        abordaPersona(numPersona, id_carriles_inv[2], listaEsperaC)
        semAndenC.release()
    else:
        print(f'Persona {numPersona} está esperando para salir en un metro en el anden:{carrilMetro}.')

def main ():
    global listaEspera
    listaEspera.append(0) #Se inicia con un elemento, para que los trrenes o hilos de metro puedan funcionar constantemnete mientras haya personas que atender
    for i in range(100):
        threading.Thread(target=llegadaPersona, args=[i]).start()
    for j in range(3): 
        threading.Thread(target=llegaMetro, args=[j]).start()
main()