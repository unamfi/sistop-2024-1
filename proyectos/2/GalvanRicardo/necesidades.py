import threading
import time
import random
from colorama import Fore, Style

numUsuarios = 5  
numMings = 8;     
esquemaMings = ['-', '-', '-', '-', '-', '-', '-', '-']
contador = 0
mut_contador = threading.Semaphore(1)
color_texto = [Fore.YELLOW, Fore.GREEN, Fore.BLUE, Fore.LIGHTRED_EX, Fore.LIGHTMAGENTA_EX]

mings = [threading.Semaphore(1) for i in range(numMings)] 

def mostrarEsquema(mings): 
    print("\n  [", end = "")
    for i in range(0,8):
         print(mings[i], end = "") 
    print("]\n")

def desbloqueaLugar(cual): 
    mings[cual].release()

def bloqueaLugar(cual): 
    mings[cual].acquire()

def desocupaLugar(quien, cual):
    mings[cual].release() 
    dice(quien, '¡Que alivio! Desocupo el mingitorio %d' % cual)
    esquemaMings[cual] = '-' 
    mostrarEsquema(esquemaMings)

    if(cual == 0):
        desbloqueaLugar(cual+1) 
    if(cual == 7):
        desbloqueaLugar(cual-1) 
    if(cual > 0 and cual < 7): 
        desbloqueaLugar(cual-1)
        desbloqueaLugar(cual+1)

def ocupaLugar(quien, cual):
    global contador
    mings[cual].acquire() 

    if(cual == 0):
        bloqueaLugar(cual+1) 
    if(cual == 7):
        bloqueaLugar(cual-1) 
    if(cual > 0 and cual < 7): 
        bloqueaLugar(cual-1)
        bloqueaLugar(cual+1)

    mut_contador.acquire()
    contador += 1
    #print("\n")
    mut_contador.release()

    dice(quien, 'Ocupo el mingitorio %d' % cual)
    esquemaMings[cual] = 'X' 
    mostrarEsquema(esquemaMings)
    time.sleep(random.randint(0,3)) 
    desocupaLugar(quien, cual) 

def dice(quien, msg):
    mi_color = color_texto[quien % len(color_texto)]
    print(Style.DIM + mi_color + '[%d] || [Usuario %d] - %s' % (contador, quien, msg))

def busca(quien):
    dice(quien, 'Buscando...')
    cual = random.randint(0,7)
    ocupaLugar(quien, cual) 

def entra(quien): 
    dice(quien, '¡Tengo ganas!')
    busca(quien)

def usuario(quien):
    dice(quien, 'Existo')

    while True: 
        entra(quien)

usuarios = [threading.Thread(target=usuario, args=[i]) for i in range(numUsuarios)]
for i in usuarios:
    i.start() 