#Alumno: Vazquez Reyes Sebastian
#Proyecto 2: Una situación cotidiana paralelizable
#Situacion: TicketMaster y el concierto de badbunny

import threading
import time
import random

# En esta parte se definen los patrones
accesoCompra = threading.Semaphore(12)
accesoPago = threading.Lock()
conciertosDisponibles = [[5, 'BadBunny', 500], [5, 'Coldplay', 350], [5, 'Imagine Dragons', 250]]
impresion = threading.Lock()

def comprador(id):
    tarjeta = random.randint(10, 20) * 50
    conciertoelegido = random.randint(0, 2)
    
    mensaje = f"Soy el comprador numero {id} y cuento con {tarjeta} pesos en mi tarjeta, y quiero ver a {conciertosDisponibles[conciertoelegido][1]}"
    imprimir(mensaje)
    
    # Cada hilo duerme un tiempo distinto y construido al azar, para simular que cada comprador maneja con diferente velocidad su PC, sumado a su conexion de Internet
    dormido = random.randint(1, 15) * 0.001
    time.sleep(dormido)
    compraBoleto(id, tarjeta, conciertoelegido)
    
    mensaje = f"Soy el comprador numero {id} y ya termine. Me salgo de la pagina"
    imprimir(mensaje)

# Un patrón para el acceso al sitio de compra y otro para el acceso al pago y disminución del producto
def compraBoleto(id, tarjeta, con):
    global accesoCompra
    accesoCompra.acquire()
    boletos = random.randint(1, 3)
    dormido = random.randint(1, 5) * 0.001
    time.sleep(dormido)
    mensaje = f"Soy el comprador numero {id} y quiero comprar {boletos} boleto(s)"
    imprimir(mensaje)
    
    precio = conciertosDisponibles[con][2] * boletos
    # Si el precio total de los boletos supera el valor de los fondos del comprador, no compra nada
    if tarjeta >= precio:
        if conciertosDisponibles[con][0] >= boletos:
            pagarBoleto(tarjeta, precio, con, boletos)
            
            mensaje = f"Soy el comprador numero {id} y tengo {boletos} boletos para ver a {conciertosDisponibles[con][1]}"
            imprimir(mensaje)
        else:
            mensaje = f"Ya no quedan tantos boletos de {conciertosDisponibles[con][1]}. Soy el comprador numero {id} y no puedo comprarlos"
            imprimir(mensaje)
    else:
        mensaje = f"Soy el comprador numero {id} y no puedo pagar el/los boleto(s), me falta dinerito"
        imprimir(mensaje)
    
    accesoCompra.release()

def pagarBoleto(tarjeta, precio, con, boletos):
    global accesoPago, conciertosDisponibles
    accesoPago.acquire()
    tarjeta -= precio
    conciertosDisponibles[con][0] -= boletos
    accesoPago.release()

def imprimir(mensaje):
    with impresion:
        print(mensaje)

def main():
    print("     ╔" + "═" * 17 + "╗")
    print('     ║  ' + '-' * 12 + '   ║')
    print("     ║  TicketMaster   ║")
    print('     ║  ' + '-' * 12 + '   ║')
    print("     ╚" + "═" * 17 + "╝")
    print("Estos son los conciertos disponibles:")
    for i in range(3):
        print("\n- " + conciertosDisponibles[i][1])
    numCompradores = int(input("\n¿Cuantos compradores en total hay hoy?: (de preferencia un numero mayor a 20)"))
    compradores = [threading.Thread(target=comprador, args=[i]).start() for i in range(numCompradores)]

main()