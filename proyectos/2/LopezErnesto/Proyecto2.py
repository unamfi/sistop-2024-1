# Import Module 
from tkinter import *
from time import sleep
import random
from threading import *

# Número de familias esperadas
num_familias = 50

# Tamaños de familia
tamaños = [1,2,4]

# Definimos el número de mesas por tamaño
mesaParaCuatro = 4
mesaParaDos = 4
mesaParaUno = 2
multiplexCuatro = Semaphore(mesaParaCuatro)
multiplexDos = Semaphore(mesaParaDos)
multiplexUno = Semaphore(mesaParaUno)

mutexLlegada = Semaphore(1)

# Cola de gente esperando por categoria
colaUno = {}
colaDos = {}
colaCuatro = {}

# Comiendo
comiendo = {}

def threading(): 
    # Call work function 
    for i in range(10):
        # La familia tendrá un tamaño aleatorio de 4, 2 o 1
        Thread(target=work,args=[i,tamaños[random.randint(0,2)]]).start()
  
# work function 
def work(fam,tam): 
    mutexLlegada.acquire() # Se entra a una zona crítica
    print(comiendo)
    print(f"La familia {fam} de tamaño {tam} llegó al establecimiento")
    # Se deberá de validar la disponibilidad para este tamaño de familia
    if tam == 1:
        # Se debe de verificar que haya mesa para una persona
        mutexLlegada.release()
        colaUno[fam] = tam
        print(colaUno)
        multiplexUno.acquire()
        comiendo[fam] = tam
        del colaUno[fam]
        # Tendrá un tiempo específico
        sleep(random.random() * 20) # Modificar el tiempo
        print(f"La familia {fam} de tamaño {tam} terminó de comer")
        # En este caso, se desocupa el lugar y se van 
        del comiendo[fam]
        multiplexUno.release()
        pass
    elif tam == 2:
        # Se debe de verificar que haya mesa para dos personas
        mutexLlegada.release()
        colaDos[fam] = tam
        print(colaDos)
        multiplexDos.acquire()
        comiendo[fam] = tam 
        del colaDos[fam]
        sleep(random.random() * 20)
        print(f"La familia {fam} de tamaño {tam} terminó de comer")
        del comiendo[fam]
        multiplexDos.release()
        pass
    else:
        # Se debe de verificar que haya mesa para cuatro personas
        mutexLlegada.release()
        colaCuatro[fam] = tam
        print(colaCuatro)
        multiplexCuatro.acquire()
        comiendo[fam] = tam
        del colaCuatro[fam]
        sleep(random.random() * 20)
        print(f"La familia {fam} de tamaño {tam} terminó de comer")
        del comiendo[fam]
        multiplexCuatro.release()
        pass
    pass
    
# Create Object 
root = Tk() 
  
# Definiendo la interfaz gráfica

root.title("Casa de Toño")
# Crear un frame para el borde del restaurante
frame_restaurante = Frame(root,bg="dark green")
frame_restaurante.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="nsew",padx=30,pady=30)

frame_mesas = Frame(frame_restaurante,bg="white")
frame_mesas.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="nsew",padx=10,pady=10)

# Configuración de las filas y columnas del frame_mesas
for i in range(1,5):
    frame_mesas.grid_rowconfigure(i, weight=1)
for i in range(3):
    frame_mesas.grid_columnconfigure(i, weight=1)

# Crear botones para representar las mesas dentro del frame
mesas = []
for fila in range(4):
    for columna in range(3):
        mesa_numero = fila * 3 + columna + 1
        mesa_button = Button(
            frame_mesas,
            text=f"Mesa {mesa_numero}",
            width=20,
            height=6,
        )
        mesa_button.grid(row=fila, column=columna, padx=40, pady=30)
        mesas.append(mesa_button)

# Agregamos un botón más para comenzar a realizar el procedimiento:
abrir = Button(
            frame_mesas,
            text=f"Abrir restaurante",
            width=10,
            height=3,
            # command=lambda: abrirRestaurante(self),
            command=threading
        )
abrir.grid(row=6,column=1)
  
# Execute Tkinter 
root.mainloop()
