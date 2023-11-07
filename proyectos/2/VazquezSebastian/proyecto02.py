#Alumno: Vazquez Reyes Sebastian
#Proyecto 2: Una situación cotidiana paralelizable
#Situacion: TicketMaster y el concierto de badbunny

import threading
import time
import random

accesoCompra = threading.Semaphore(20)
accesoPago = threading.Lock()

conciertosDisponibles= [[10,'BadBunny', 500],[8,'Coldplay', 350], [8,'Imagine Dragons', 250]]

def comprador(id): 
    tarjeta = random.randint(10, 20) * 50   
    conciertoelegido = random.randint(0, 2) 
    print ("Soy el comprador numero "+ id + " y cuento con " + tarjeta +" pesos en mi tarjeta, y quiero ver a "+ conciertosDisponibles[conciertoelegido][1])
    dormido = random.randint(1, 9) * 0.015
    time.sleep(dormido) 
    compraBoleto(id,tarjeta, conciertoelegido)

def compraBoleto(id, tarjeta, con):
    global accesoCompra, accesoPago
    accesoCompra.acquire
    boletos = random.randint(1, 3)
    print ("Soy el comprador numero "+ id + " y quiero comprar " + boletos +" boleto(s)")
    precio = conciertosDisponibles[con][2] * boletos
    if(tarjeta>=precio):
        if (conciertosDisponibles[con][0]>=boletos):
            pagarBoleto(tarjeta, precio, con, boletos)
            print ("Soy el comprador numero "+ id + " y tengo " + boletos +" boletos para ver a "+ conciertosDisponibles[con][1])
        else:
            print ("Ya no quedan tantos boletos, no puedo comprarlos")
    else:
        print ("No puedo pagar el/los boleto(s), salgo de la cola")
    accesoCompra.release

def pagarBoleto(tarjeta, precio, con, boletos):
    global accesoPago
    accesoPago.acquire
    tarjeta -= precio
    conciertosDisponibles[con][0] -= boletos
    accesoPago.release
	
def main():
    numCompradores = int(input("¿Cuantos compradores en total hay hoy?: (de preferencia un numero mayor a 20)"))
    compradores = [threading.Thread(target = comprador, args=[i]).start() for i in range (numCompradores)]

main()