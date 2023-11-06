#Alumno: Vazquez Reyes Sebastian
#Proyecto 2: Una situación cotidiana paralelizable
#Situacion: TicketMaster y el concierto de badbunny

import threading
import time
import random

accesoCompra = threading.Semaphore(10)
accesoPago1 = threading.Lock()
accesoPago2 = threading.Lock()
accesoPago3 = threading.Lock()

conciertosDisponibles= [['15','BadBunny'],['20','Coldplay'], ['10','Imagine Dragons']]

def comprador(id): 
    global accesoCompra, accesoPago1, accesoPago2, accesoPago3

	
def main():
    numCompradores = int(input("¿Cuantos compradores en total hay hoy?: (de preferencia un numero mayor a 20)"))

    compradores = [threading.Thread(target = comprador, args=[i]).start() for i in range (numCompradores)]

main()