import threading
import time
import random
import numpy as np
#[2,3]
#Matriz inicial (Sin tráfico).
Calle = np.matrix([['www', "| : |" , "| : |", 'www'],
               ["¯¯¯¯", ".:. " , " .:.", "¯¯¯¯"],
               ["____", ".:. " , " .:.", "____"],
               ['www', "| : |" , "| : |", 'www']])

#Matrix que solo sirve para representar las posiciones de los semáforos (los Números)
#, las posiciones que no se ocupan (los 0), y las posiciones dónde incia cada carril
#(X) dentro de la matriz.
GuiaPos = np.matrix([[0, "X" , "0", 0],
               ["1", "2" , "3", "X"],
               ["X", "4" , "5", "6"],
               [0, "7" , "X", 0]])
#Variables para determinar la duración del programa

    #Variable que lleva la cuenta de cuantas veces se realizo la función Moverse()
contador = 0
    #Se crea mutex para contador de veces que se ha realizado el ciclo
contador_mutex = threading.Semaphore(1)
    #Se crea mutex para la duración del programa 
dur_mutex = threading.Semaphore(1)
    #Variable que controla el ciclo de repeticiones del programa 
dur_prog = True

    #Numero de coches totales que correran en el programa (ejecuciones de la función 
    # Moverse() )
num_coches = 10

#Semáforos utilizados:

    #Numero de semáforos para limitar la entrada a cada una de las posiciones 
    #compartidas según "GuiaPos"
num_semaforos = 8

    #Variable que contiene la cantidad máxima de lineas que pueden ir recto a la vez.
    #Esta será usada por un semáforo para evitar un bloqueo mutuo cuando los 4
    #carriles quieran ir recto y se encuentren en las posicones centrales.
num_direcciones_rectas = 3

    #Se crea tanto semáforos como lo indique "num_direcciones_rectas (Multiplex)"
dir_semaphore = threading.Semaphore(num_direcciones_rectas)

#Se crea un mutex para matriz
mutex = threading.Lock()

#Cantidad de hilos que se van a usar
num_carriles = 8

#Se crea un arreglo que contiene a los semáforos que limitan la entrada a las
#posicones de los coches compartidas según "GuiaPos"
posicion = [threading.Semaphore(1) for i in range (num_semaforos)]


#Función principal compartida por todos los hilos.

def Moverse(auto):

    print(f'\n {auto} Quiero moverme\n')
    time.sleep(1)
    if(auto == 0):
        dir0 = random.randint(0,1)
        #Se mueve recto
        if(dir0 == 1):
            print(f'\n [{auto}] Quiero ir recto\n')
            time.sleep(1)
            #Toma Multiplex
            dir_semaphore.acquire() 
            #Chequeo
            posicion[4].acquire()           
            #Mutex
            mutex.acquire()
            Calle[2,1] = ".X. "
            
            print("\n")
            print(Calle)
            print("\n")

            mutex.release()
 
            #Fin mutex         

            time.sleep(1)
            #Chequeo 2
            posicion[5].acquire()
            
            #Mutex
            mutex.acquire()
            Calle[2,2] = " .X."
            Calle[2,1] = ".:. "
            print("\n")
            print(Calle)
            print("\n")
            mutex.release()           
            #Fin mutex
            posicion[4].release()
            #Liberamos ticket
            dir_semaphore.release()   
            time.sleep(1)
            #Chequeo 3
            posicion[6].acquire()
            
            #Mutex
            mutex.acquire()
            Calle[2,3] = "__X_"
            Calle[2,2] = " .:."
            print("\n")
            print(Calle)
            print("\n")
            mutex.release() 
            #Fin mutex
            posicion[5].release()
            time.sleep(1)
            print(f'{auto} Me voy !!')

            #Mutex
            mutex.acquire() 
            Calle[2,3] = "____"
            print("\n")
            print(Calle)
            print("\n")
            mutex.release()            
            #Fin mutex
            time.sleep(1)
            posicion[6].release()

        if(dir0 == 0):
            print(f'\n [{auto}] Quiero girar a la derecha \n')
            time.sleep(1)
            #Chequeo
            posicion[4].acquire()
            #Mutex
            mutex.acquire() 
            Calle[2,1] = ".X. "
            print("\n")
            print(Calle)
            print("\n")
            mutex.release()
            #Fin mutex   
            time.sleep(1)      
            #Chequeo 2
            posicion[7].acquire()
            
            #Mutex
            mutex.acquire()
            Calle[3,1] = "| X |"
            Calle[2,1] = ".:. "
            print("\n")
            print(Calle)
            print("\n")
            mutex.release()          
            #Fin mutex
            posicion[4].release() 
            time.sleep(1)
             
            print(f'{auto} Me voy !!')
            
            #Mutex
            mutex.acquire()
            Calle[3,1] = "| : |"
            print("\n")
            print(Calle)
            print("\n")            
            mutex.release()
            #Fin mutex
            time.sleep(1)
            posicion[7].release()

    if(auto == 1):
        dir1 = random.randint(0 ,1)
        #Se mueve recto
        if(dir1 == 1):
            print(f'\n [{auto}] Quiero ir recto\n')
            time.sleep(1)
            #Ticket
            dir_semaphore.acquire() 
            #Chequeo
            posicion[3].acquire()
            
            #Mutex
            mutex.acquire()
            Calle[1,2] = " .0."
            
            print("\n")
            print(Calle)
            print("\n")

            mutex.release()
 
            #Fin mutex         

            time.sleep(1)
            #Chequeo 2
            posicion[2].acquire()
            
            #Mutex
            mutex.acquire()
            Calle[1,1] = ".0. "
            Calle[1,2] = " .:."
            print("\n")
            print(Calle)
            print("\n")
            mutex.release()           
            #Fin mutex
            posicion[3].release()
            #Ticket
            dir_semaphore.release()   
            time.sleep(1)
            #Chequeo 3
            posicion[1].acquire()
            
            #Mutex
            mutex.acquire()
            Calle[1,0] = "¯0¯¯"
            Calle[1,1] = ".:. "
            print("\n")
            print(Calle)
            print("\n")
            mutex.release() 
            #Fin mutex
            posicion[2].release() 
            time.sleep(1)
            print(f'\n {auto} Me voy !! \n')

            #Mutex
            mutex.acquire() 
            Calle[1,0] = "¯¯¯¯"
            print("\n")
            print(Calle)
            print("\n")
            mutex.release()            
            #Fin mutex
            time.sleep(1)
            posicion[1].release()

        if(dir1 == 0):
            print(f'\n [{auto}] Quiero girar a la derecha \n')
            time.sleep(1)
            #Chequeo
            posicion[3].acquire()
            #Mutex
            mutex.acquire() 
            Calle[1,2] = " .0."
            print("\n")
            print(Calle)
            print("\n")
            mutex.release()
            #Fin mutex   
            time.sleep(1)      
            #Chequeo 2
            posicion[0].acquire()
            
            #Mutex
            mutex.acquire()
            Calle[0,2] = "| 0 |"
            Calle[1,2] = " .:."
            print("\n")
            print(Calle)
            print("\n")
            mutex.release()          
            #Fin mutex
            posicion[3].release()
            time.sleep(1)
             
            print(f'\n {auto} Me voy !! \n')
            
            #Mutex
            mutex.acquire()
            Calle[0,2] = "| : |"
            print("\n")
            print(Calle)
            print("\n")            
            mutex.release()
            #Fin mutex
            time.sleep(1)
            posicion[0].release()
    if(auto == 2):
        dir2 = random.randint(0,1)
        #Se mueve recto
        if(dir2 == 1):
            print(f'\n [{auto}] Quiero ir recto \n')
            time.sleep(1)
            #Ticket
            dir_semaphore.acquire() 
            #Chequeo
            posicion[2].acquire()
            
            #Mutex
            mutex.acquire()
            Calle[1,1] = ".B. "
            
            print("\n")
            print(Calle)
            print("\n")

            mutex.release()
 
            #Fin mutex         

            time.sleep(1)
            #Chequeo 2
            posicion[4].acquire()
            
            #Mutex
            mutex.acquire()
            Calle[2,1] = ".B. "
            Calle[1,1] = ".:. "
            print("\n")
            print(Calle)
            print("\n")
            mutex.release()           
            #Fin mutex
            posicion[2].release()
            #Ticket
            dir_semaphore.release() 
            time.sleep(1)
            #Chequeo 3
            posicion[7].acquire()
            
            #Mutex
            mutex.acquire()
            Calle[3,1] = "| B |"
            Calle[2,1] = ".:. "
            print("\n")
            print(Calle)
            print("\n")
            mutex.release() 
            #Fin mutex
            posicion[4].release() 
            time.sleep(1)
            print(f'\n {auto} Me voy !! \n')

            #Mutex
            mutex.acquire() 
            Calle[3,1] = "| : |"
            print("\n")
            print(Calle)
            print("\n")
            mutex.release()            
            #Fin mutex
            time.sleep(1)
            posicion[7].release()

        if(dir2 == 0):
            print(f'\n [{auto}] Quiero girar a la derecha \n')
            time.sleep(1)
            #Chequeo
            posicion[2].acquire()
            #Mutex
            mutex.acquire() 
            Calle[1,1] = ".B. "
            print("\n")
            print(Calle)
            print("\n")
            mutex.release()
            #Fin mutex   
            time.sleep(1)      
            #Chequeo 2
            posicion[1].acquire()
            
            #Mutex
            mutex.acquire()
            Calle[1,0] = "¯B¯¯"
            Calle[1,1] = ".:. "
            print("\n")
            print(Calle)
            print("\n")
            mutex.release()          
            #Fin mutex
            posicion[2].release()
            time.sleep(1)
             
            print(f'\n {auto} Me voy !! \n')
            
            #Mutex
            mutex.acquire()
            Calle[1,0] = "¯¯¯¯"
            print("\n")
            print(Calle)
            print("\n")            
            mutex.release()
            #Fin mutex
            time.sleep(1)
            posicion[1].release()
    if(auto == 3):
        dir3 = random.randint(0,1)
        #Se mueve recto
        if(dir3 == 1):
            print(f'\n [{auto}] Quiero ir recto \n')
            #Ticket
            dir_semaphore.acquire() 
            time.sleep(1)
            #Chequeo
            posicion[5].acquire()
            
            #Mutex
            mutex.acquire()
            Calle[2,2] = " .S."
            
            print("\n")
            print(Calle)
            print("\n")

            mutex.release()
 
            #Fin mutex         

            time.sleep(1)
            #Chequeo 2
            posicion[3].acquire()
            
            #Mutex
            mutex.acquire()
            Calle[1,2] = " .S."
            Calle[2,2] = " .:."
            print("\n")
            print(Calle)
            print("\n")
            mutex.release()                    
            #Fin mutex 
            posicion[5].release()
            #Ticket
            dir_semaphore.release() 
            time.sleep(1)
            #Chequeo 3
            posicion[0].acquire()
            
            #Mutex
            mutex.acquire()
            Calle[0,2] = "| S |"
            Calle[1,2] = " .:."
            print("\n")
            print(Calle)
            print("\n")
            mutex.release() 
            #Fin mutex
            posicion[3].release()
            time.sleep(1)
            print(f'\n {auto} Me voy !! \n')

            #Mutex
            mutex.acquire() 
            Calle[0,2] = "| : |"
            print("\n")
            print(Calle)
            print("\n")
            mutex.release()            
            #Fin mutex
            time.sleep(1)
            posicion[0].release()

        if(dir3 == 0):
            print(f'\n [{auto}] Quiero girar a la derecha \n')
            time.sleep(1)
            #Chequeo
            posicion[5].acquire()
            #Mutex
            mutex.acquire() 
            Calle[2,2] = " .S."
            print("\n")
            print(Calle)
            print("\n")
            mutex.release()
            #Fin mutex   
            time.sleep(1)      
            #Chequeo 2
            posicion[6].acquire()
            
            #Mutex
            mutex.acquire()
            Calle[2,3] = "_S__"
            Calle[2,2] = " .:."
            print("\n")
            print(Calle)
            print("\n")
            mutex.release()          
            #Fin mutex
            posicion[5].release() 
            time.sleep(1)
             
            print(f'\n {auto} Me voy !! \n')
            
            #Mutex
            mutex.acquire()
            Calle[2,3] = "¯¯¯¯"
            print("\n")
            print(Calle)
            print("\n")            
            mutex.release()
            #Fin mutex
            time.sleep(1)
            posicion[6].release()


#Función que ejecutan todos los hilos.
#Está dentro de un ciclo que se limita el número de ejecuciones del método
# Moverse() a la cantidad "num_coches" para simular el tráfico durante 
# el tiempo deseado.

def Inicio(auto):
    global dur_prog
    global contador
    while dur_prog:
        #Inicio mutex contador
        contador_mutex.acquire()
        contador = contador + 1
        contador_mutex.release()
        #Fin mutex contador
        if(contador >= num_coches):
            #Inicio mutex duracion
            dur_mutex.acquire()
            dur_prog = False
            dur_mutex.release()
        Moverse(auto)
        
     
#Creamos e inciamos los hilos indicados usando un ciclo for.
#Se usa la variable "n" para que después de asignar los 4 carriles a 4 hilos, 
# el resto sean asignados de forma aleatoria.
for i in range(num_carriles):  
    n=i
    if(i > 3):
        n = random.randint(0,3)
    t = threading.Thread(target=Inicio,args = (n,))
    t.start()