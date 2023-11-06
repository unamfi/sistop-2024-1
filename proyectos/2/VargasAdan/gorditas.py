# @author: Adan Vargas
# Proyecto 2 Sistemas Operativos
# Gorditas Laguneras

#importar modulos

from tkinter import *
from time import sleep
import random
from threading import *

#creacion de ventana principal
root = Tk() 

#Titulo de ventana con nombre del local de las gorditas
root.title("Gorditas Doña Lipa")

# Crear un frame para el borde del local
frame = Frame(root,bg="red")
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
            texto = f"Gorditas de Cocedor"
        elif columna == 1 and fila == 1:
            texto = f"Cajera, da click y toma ordenes"
        elif columna == 1:
            texto = f"Gorditas de Harina y Maiz"
        else:
        	texto = f"Gorditas al carbon"
        if fila == 0 or (fila == 1 and columna == 1):
	        btn_nuevo = Button(
	            frame_botones,
	            text=texto,
	            justify="center",
	            width=24,
	            height=6,
	            bg="yellow",
	            fg="black",
	            state="normal"
	        )
	        btn_nuevo.grid(row=fila, column=columna, padx=40, pady=30)
	        puestos[len(puestos)] = [True,btn_nuevo] # Al inicio, todas las mesas están disponibles
	    
# Execute Tkinter 
root.mainloop()
