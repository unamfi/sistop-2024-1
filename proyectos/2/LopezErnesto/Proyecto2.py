# Import Module 
from tkinter import *
from time import sleep
import random
from threading import *



# Número de familias esperadas
num_familias = 15

# Tamaños de familia
tamaños = [1,2,4]

# Definimos el número de mesas por tamaño
mesaParaCuatro = 4
mesaParaDos = 4
mesaParaUno = 4
multiplexCuatro = Semaphore(mesaParaCuatro)
multiplexDos = Semaphore(mesaParaDos)
multiplexUno = Semaphore(mesaParaUno)
mesasCuatro = {}
mesasDos = {}
mesasUno = {}

mutexLlegada = Semaphore(1)
mutexAsignacionMesa = Semaphore(1)
mutexLiberacionMesa = Semaphore(1)
# Cola de gente esperando por categoria
colaUno = {}
colaDos = {}
colaCuatro = {}

# Determinar qué famila está utilizando qué mesa
mesa_familia = {}

def update_gui(key,fam,tamanio,diccionario):
    if diccionario[key][0] == True:
        diccionario[key][1].config(text=f"Mesa para {tamanio}: ocupada por familia {fam}", state="disabled", fg="red")
        diccionario[key][0] = False
    else:
        diccionario[key][1].config(text=f"Mesa para {tamanio}: disponible", state="active", fg="green")
        diccionario[key][0] = True

def threading(num): 
    # Call work function 
    abrir.destroy()
    for i in range(num):
        # La familia tendrá un tamaño aleatorio de 4, 2 o 1
        Thread(target=work,args=[i,tamaños[random.randint(0,2)]],daemon=True).start()

    cerrar = Button(
            frame_mesas,
            text=f"Cerrar restaurante",
            width=10,
            height=3,
            command=quit,
        )
    cerrar.grid(row=6,column=1)

def llegadaFamilia(fam,tam,mutex,mesas):
    # Se debe de verificar que haya mesa para una persona
    mutex.acquire()
    # En caso de haber mesa, se debe de señalar en el mapa que está utilizada
    mutexAsignacionMesa.acquire()
    for key,value in mesas.items():
        if value[0] == True: # Se toma la mesa
            root.after(0,update_gui,key,fam,tam,mesas)
            # mesa = key
            mesa_familia[fam] = key
            print(mesa_familia)
            break

    mutexAsignacionMesa.release()
    # Tendrá un tiempo específico
    sleep(random.random() * 20) # Modificar el tiempo
    #mutexLiberacionMesa.acquire() # Se va a desocupar la mesa -- OJO
    print(f"La familia {fam} de tamaño {tam} terminó de comer")
    # En este caso, se desocupa el lugar y se van 
    root.after(0,update_gui,mesa_familia[fam],fam,tam,mesas)
    # del mesa_familia[fam]
    #mutexLiberacionMesa.release() -- OJO
    mutex.release()

  
# work function 
def work(fam,tam): 
    sleep(random.random() * random.randint(20,40))
    print(f"La familia {fam} de tamaño {tam} llegó al establecimiento")
    # Se deberá de validar la disponibilidad para este tamaño de familia
    if tam == 1:
        llegadaFamilia(fam,tam,multiplexUno,mesasUno)
    elif tam == 2:
        llegadaFamilia(fam,tam,multiplexDos,mesasDos)
    else:
        llegadaFamilia(fam,tam,multiplexCuatro,mesasCuatro)
    
# Create Object 
root = Tk() 
  
# Definiendo la interfaz gráfica

root.title("Casa de Toño")
# Crear un frame para el borde del restaurante
frame_restaurante = Frame(root,bg="dark green")
frame_restaurante.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="nsew",padx=30,pady=30)

frame_mesas = Frame(frame_restaurante,bg="light goldenrod")
frame_mesas.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="nsew",padx=10,pady=10)

# Configuración de las filas y columnas del frame_mesas
for i in range(1,5):
    frame_mesas.grid_rowconfigure(i, weight=1)
for i in range(3):
    frame_mesas.grid_columnconfigure(i, weight=1)

# Crear botones para representar las mesas dentro del frame
mesasCuatro = {}
mesasDos = {}
mesasUno = {}
estado = ["disponible", "ocupada"]
texto = ""
for fila in range(4):
    for columna in range(3):
        if columna == 0:
            texto = f"Mesa para 4: {estado[0]}"
        elif columna == 1:
            texto = f"Mesa para 2: {estado[0]}"
        else:
            texto = f"Mesa para 1: {estado[0]}"
        mesa_numero = fila * 3 + columna + 1
        mesa_button = Button(
            frame_mesas,
            text=texto,
            width=20,
            height=6,
            bg="brown",
            fg="green",
            state="active"
        )
        if columna == 0:
            mesasCuatro[len(mesasCuatro)] = [True,mesa_button] # Al inicio, todas las mesas están disponibles
        elif columna == 1:
            mesasDos[len(mesasDos)] = [True,mesa_button] # Al inicio, todas las mesas están disponibles
        else:
            mesasUno[len(mesasUno)] = [True,mesa_button]
            pass
        mesa_button.grid(row=fila, column=columna, padx=40, pady=30)

# Agregamos un botón más para comenzar a realizar el procedimiento:
abrir = Button(
            frame_mesas,
            text=f"Abrir restaurante",
            width=10,
            height=3,
            command=lambda: threading(num_familias),
        )
abrir.grid(row=6,column=1)
  
# Execute Tkinter 
root.mainloop()