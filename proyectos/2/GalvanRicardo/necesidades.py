import threading
import time
import random
from colorama import Fore, Style #permite imprimir lineas en color

numUsuarios = 5 #usuarios totales que usaran los mingitorios
numMings = 8;   #numero de mingitorios disponibles  
esquemaMings = ['-', '-', '-', '-', '-', '-', '-', '-'] #esquema visual para representar el estado
contador = 0 #para llevar un mejor seguimiento de los eventos que ocurren
mut_contador = threading.Semaphore(1) #mutex para que solo uno pueda modificar el contador a la vez
color_texto = [Fore.YELLOW, Fore.GREEN, Fore.BLUE, Fore.LIGHTRED_EX, Fore.LIGHTMAGENTA_EX, Fore.WHITE] #colores

mings = [threading.Semaphore(1) for i in range(numMings)] #por cada mingitorio se crea un semaforo

def mostrarEsquema(mings):  #imprime el esquema visual de mingitorios
    print(color_texto[5] + "\n  [", end = "")
    for i in range(0,8):
         print(mings[i], end = "") 
    print("]\n")

#las siguientes dos funciones sirven solo para liberar los lugares 'bloqueados'
def desbloqueaLugar(cual): #libera el semaforo
    mings[cual].release()

def bloqueaLugar(cual): #adquiere el semaforo
    mings[cual].acquire()

#las siguientes dos funciones manejan que un usuario ocupe y desocupe un mingitorio
def desocupaLugar(quien, cual):
    mings[cual].release() #el mingitorio utilizado se desocupa, se libera el semaforo
    dice(quien, '¡Que alivio! Desocupo el mingitorio %d' % cual)
    esquemaMings[cual] = '-' #se actualiza la representacion en el esquema visual
    mostrarEsquema(esquemaMings)

    #checar la posicion ocupada, para liberar los que corresponda
    if(cual == 0): #si es el mingitorio de la izquierda...
        desbloqueaLugar(cual+1) #se libera tambien el de la derecha
    if(cual == 7): #si el mingitorio es el de la derecha...
        desbloqueaLugar(cual-1) #...se libera tambien el de la izquierda
    if(cual > 0 and cual < 7): #si es un mingitorio 'intermedio'...
        desbloqueaLugar(cual-1) #...se libera el de la izquierda...
        desbloqueaLugar(cual+1) #... y el de la derecha

def ocupaLugar(quien, cual):
    global contador #globalizar la variable para visualizar cambios de estado
    mings[cual].acquire() #se ocupa el mingitorio; se adquiere el semaforo

    #checar la posicion ocupada, para ocupar los que corresponda
    if(cual == 0):
        bloqueaLugar(cual+1) 
    if(cual == 7):
        bloqueaLugar(cual-1) 
    if(cual > 0 and cual < 7): 
        bloqueaLugar(cual-1)
        bloqueaLugar(cual+1)

    #el hilo en proceso adquiere el mutex para modificar el contador, y lo libera despues
    mut_contador.acquire()
    contador += 1
    mut_contador.release()

    dice(quien, 'Ocupo el mingitorio %d' % cual) #el usuario informa su accion
    esquemaMings[cual] = 'X' #se actualiza el esquema visual
    mostrarEsquema(esquemaMings)
    time.sleep(random.randint(1,3)) #el usuario se toma su tiempo para hacer sus necesidades...
    desocupaLugar(quien, cual) #... y cuando termina, desocupa el mingitorio

#funcion que imprime mensaje de accion
def dice(quien, msg):
    mi_color = color_texto[quien % len(color_texto)]
    print(Style.DIM + mi_color + '[%d] || [Usuario %d] - %s' % (contador, quien, msg))

#funcion donde el usuario busca un mingitorio para hacer sus necesidades
def busca(quien):
    dice(quien, 'Buscando...')
    cual = random.randint(0,7) #selecciona un mingitorio
    ocupaLugar(quien, cual) #e intenta ocuparlo

#funcion donde el usuario entra al lugar; el hilo comienza sus actividades
def entra(quien): 
    dice(quien, '¡Tengo ganas!')
    busca(quien) #comienza a buscar un lugar

#funcion inicial donde el usuario existe; el hilo se inicia
def usuario(quien):
    dice(quien, 'Existo')

    #de manera indefinida, los usuarios hacen sus necesidades y vuelven; los hilos se ejecutan
    while True: 
        entra(quien)

#por cada usuario se inicia un hilo, y se inicializan.
usuarios = [threading.Thread(target=usuario, args=[i]) for i in range(numUsuarios)]
for i in usuarios:
    i.start() 