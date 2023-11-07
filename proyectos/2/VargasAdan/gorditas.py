# @author: Adan Vargas
# Proyecto 2 Sistemas Operativos
# Gorditas Laguneras

#importar modulos

from tkinter import *
from time import sleep
import random
from threading import *

#definicion de variables

#para representar cuantas gorditas tiene que hacer cada empleado segun el tipo
pedidosCocedor = 0
pedidosCarbon = 0
pedidosComal = 0
mutex = Semaphore(1)
mutexTomaPedidos = Semaphore(1)

#contador de todos los pedidos que ha terminado el local
contadorTotal = 0

def comenzarHilos():
    Thread(target=tomaOrdenes,args=[],daemon=True).start()
    Thread(target=cocinarCocedor,args=[pedidosCocedor],daemon=True).start()
    Thread(target=cocinarComal,args=[pedidosComal],daemon=True).start()
    Thread(target=cocinarCarbon,args=[pedidosCarbon],daemon=True).start()
    #para cerrar programa
    cerrar_btn = Button(
            frame_botones,
            text="Cerrar",
            width=20,
            height=3,
            bg = "red",
            command=quit,
        )
    cerrar_btn.grid(row=5,column=1)

def actualizarInterfaz(tipo:int,pedidos:int):
	#para actualizar el texto de los botones de cada puesto de trabajo segun los pedidos que tengan
	btn_aux = puestos[tipo] 
	#if tipo == 0:
		#btn_aux.Button(text="Gorditas de cocedor -> {pedidos}", state="normal")
	#elif tipo == 1:
		#btn_aux.Button(text="Gorditas de harina o maiz -> {pedidos}", state="normal")
	#else: 
		#btn_aux.Button(text="Gorditas de carbon -> {pedidos}", state="normal")

def tomaOrdenes(): 
	print("tomando ordenes")
	#se deben tomar pedidos cada cierto tiempo aleatorio
	sleep(random.random() * random.randint(10,20))
	#segun el numero son la cantidad de gorditas que tienen que realizar
	mutexTomaPedidos.acquire()
	pedido = random.randint(1,4)
	tipo = random.randint(0,2)
	actualizarInterfaz(tipo,pedido)
	if tipo == 0:		
		pedidosCocedor += pedido
		pedido_txt = "Se pidieron " + pedido + " de cocedor"
		print(pedido_txt.text) 
	elif tipo == 1:
		pedidosComal += pedido
		pedido_txt = "Se pidieron " + pedido + " de maiz o harina"
		print(pedido_txt.text)
	else:
		mutex.acquire()
		pedidosCarbon += pedido
		pedido_txt = "Se pidieron " + pedido + " al carbon"
		print(pedido_txt.text)
		mutex.release()
	mutexTomaPedidos.release()
	

def cocinarCocedor(pedidos:int):
	while (pedidos > 0):
		sleep(random.random() * random.randint(5,9))
		print("cocinando gorditas de cocedor")	
		pedidos-=1
		mutex.acquire()
		contadorTotal+=1
		mutex.release()
		cocinarCocedor(pedidos)
def cocinarCarbon(pedidos:int):
	while (pedidos > 0):
		sleep(random.random() * random.randint(3,6))
		print("cocinando gorditas de carbon")	
		pedidos-=1
		mutex.acquire()
		contadorTotal+=1
		mutex.release()
		cocinarCarbon(pedidos)
def cocinarComal(pedidos:int):
	while (pedidos > 0):
		sleep(random.random() * random.randint(3,6))
		print("cocinando gorditas de comal")	
		pedidos-=1
		mutex.acquire()
		contadorTotal+=1
		mutex.release()
		cocinarComal(pedidos)

#creacion de ventana principal
root = Tk() 

#Titulo de ventana con nombre del local de las gorditas
root.title("Gorditas Doña Lipa")

# Crear un frame para el borde del local
frame = Frame(root,bg="orange")
frame.grid(row=2, column=0, rowspan=2, columnspan=3, sticky="nsew")
# Se crea el interior del local
frame_botones = Frame(frame,bg="white")
frame_botones.grid(row=2, column=0, rowspan=2, columnspan=3, sticky="nsew",padx=10,pady=10)

# Arreglo que almacenara los 4 botones de tipos de gorditas y la cajera
puestos = {}
#variable auxiliar para representar el texto que tendra cada boton
texto = ""

for fila in range(2):
    for columna in range(3):
        if columna == 0:
            texto = "Gorditas de Cocedor"
        elif columna == 1 and fila == 1:
            texto = "Cajera"
        elif columna == 1:
            texto = "Gorditas de Harina o Maiz"
        else:
        	texto = "Gorditas al carbon"
        if fila == 0 or (fila == 1 and columna == 1):
	        btn_nuevo = Button(frame_botones,text=texto,justify="center",width=24,height=6,bg="yellow",fg="black",state="normal")
	        btn_nuevo.grid(row=fila, column=columna, padx=40, pady=30)
	        puestos[len(puestos)] = [True,btn_nuevo]

# Leyenda que se debe actualizar al dar click en Cajera
pedido_txt = Label(frame_botones,text="Gorditas que se pidieron : 0 de ",width=50,height=3)
pedido_txt.grid(row=2,column=1)
# Leyenda que se debe actualizar cuando ya acaben de realizar un pedido 
total_txt = Label(frame_botones,text="Gorditas vendidas : 0 ",width=30,height=3)
total_txt.grid(row=3,column=1)

# Dando click debe iniciar a recibir pedidos la cajera
abrir_btn = Button(frame_botones,text="Abriendo local", width=20,height=3,bg = "yellow",command=lambda: comenzarHilos())
abrir_btn.grid(row=4,column=1)
# Execute Tkinter 
root.mainloop()



