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

mutexAsignacionMesa = Semaphore(1)
mutexLiberacionMesa = Semaphore(1)
mutexAcceso = Semaphore(1)
# Cola de gente esperando por categoria
colaUno = {}
colaDos = {}
colaCuatro = {}

# Determinar qué famila está utilizando qué mesa
mesa_familia = {}

def update_gui(key,fam,tamanio,diccionario):
    """
        Esta función se encarga de actualizar la interfaz gráfica para mostrar la llegada y salida de los diferentes grupos.
        Para esto se analiza el estado de la mesa para transformarlo al estado opuesto.
    """
    if diccionario[key][0] == True:
        diccionario[key][1].config(text=f"Mesa para {tamanio}: ocupada por familia {fam}", state="normal", fg="red")
        diccionario[key][0] = False
    else:
        diccionario[key][1].config(text=f"Mesa para {tamanio}: disponible", state="normal", fg="green")
        diccionario[key][0] = True

def threading(num): 
    """
        Esta función comienza a mandar los diferentes hilos asociados a las diferentes familias que van llegando al establecimiento.
        En este caso, se agrega un botón para terminar el proceso en caso de falla.
        En total se está mandando un número "num" de familias que llegarán en tiempos aleatorios al restaurante.
    """
    abrir.destroy()
    for i in range(num):
        # La familia tendrá un tamaño aleatorio de 4, 2 o 1
        Thread(target=llegada,args=[i,tamaños[random.randint(0,2)]],daemon=True).start()

    # El botón permite terminar el hilo principal para poder cerrar el programa sin problemas
    cerrar = Button(
            frame_mesas,
            text="Cerrar restaurante",
            width=10,
            height=3,
            command=quit,
        )
    cerrar.grid(row=6,column=1)

    global evento 
    evento = Button(
            frame_mesas,
            text="Llegada de productos",
            width=15,
            height=3,
            command=threadLlegada
    )
    evento.grid(row=6,column=2)

def threadLlegada():
    """
        Este caso considera un evento en donde se brinda al restaurante con más alimento para poder atender a más clientes. 
        Para esto se cambiará el botón para mostrar un mensaje de que el restaurante se está surtiendo.

    """
    # En este caso se debe de tomar el mutex de acceso al restaurante
    evento.destroy()
    global surtiendo
    surtiendo = Button(
            frame_mesas,
            text=f"Surtiendo restaurante",
            width=15,
            height=3,
            fg="red"
        )
    surtiendo.grid(row=6,column=2)  
    Thread(target=surtiendoRestaurante,args=[],daemon=True).start()
    
def surtiendoRestaurante():
    """
        En este caso se toma el mutex de la puerta de acceso, lo que bloquea la entrada de nuevos grupos.
        Dado un tiempo, se estará surtiendo al restaurante con nuevos alimentos para los próximos grupos.
        El mutex de acceso sirve como torniquete para los grupos que van llegando al restaurante
    """
    global surtiendo
    global evento
    # En este punto ya no puede acceder nadie hasta que el surtidor haya terminado de realizar su tarea
    mutexAcceso.acquire()
    # En este punto se tiene que bloquear la salida
    print("Se está surtiendo al restaurante")
    sleep(20)
    print("Se terminó se surtir al restaurante")
    surtiendo.destroy()
    evento = Button(
            frame_mesas,
            text="Llegada de productos",
            width=15,
            height=3,
            command=threadLlegada
    )
    evento.grid(row=6,column=2)
    mutexAcceso.release()


def llegadaFamilia(fam,tam,mutex,mesas):
    """
        Esta función se  encarga de gestionar la concurrencia de los hilos representados por las familias. Cada uno de los hilos llegará 
        y deberá de analizar si es posible ingresar al rstaurante, es decir, si hay una mesa para el tamaño de su grupo que permita el acceso
        al establecimiento. 

        En este caso, se utilizaron varios mutex para zonas críticas de operación en donde se llegaban a utilizar variables globales, como 
        lo son: mesa_familia. Igualmente, como se observa por la naturaleza del problema, en este caso fue necesario tener un multiplex para 
        cada uno de los tamaños de grupo, ya que solo puede haber cierto número de una categoría de grupo dentro del establecimiento. Por lo mismo,
        la solución se realizó mediante un multiplex que pone en espera a los grupos que van llegando hasta que termine de comer un grupo del mismo tamaño.

        Las variables que se reciben son:
        1. El identificador de la familia
        2. El tamaño de la familia
        3. El multiplex asociado al tamaño de grupo
        4. La información de las mesas para el tamaño de grupo señalizado. Esto con el fin de modificar la interfaz gráfica    
    """
    mutex.acquire()
    mutexAcceso.acquire()
    mutexAcceso.release()
    # Como se trabajará con una variable global, se toma un mutex para realizar la asignación de la mesa respectiva
    mutexAsignacionMesa.acquire()
    for key,value in mesas.items():
        if value[0] == True: # Hay mesas disponibles
            root.after(0,update_gui,key,fam,tam,mesas)
            # Se asigna la mesa al grupo respectivo
            mesa_familia[fam] = key
            break
    mutexAsignacionMesa.release()

    # El grupo estará un tiempo aleatorio dentro del establecimiento
    sleep(random.random() * 20)
    print(f"La familia {fam} de tamaño {tam} terminó de comer")
    # En este caso, se desocupa el lugar y se van 
    root.after(0,update_gui,mesa_familia[fam],fam,tam,mesas)
    mutex.release()

  
# Se analiza el tamaño de la familia para atender su llegada
def llegada(fam,tam): 
    """ 
        Esta función se encarga de gestar la llegada de las diferentes familias. Dado a la forma en la que trabaja Tkinter fue necesario 
        agregar el tiempo aleatorio de llegada en el hilo secundario (ya que, si se colocaba en el principal, generaba una espera 
        dentro del hilo principal, pausando la interfaz gráfica).

        Dentro de esta función, lo único que se analiza es el tamaño de la familia para mandar a llamar la función que se encarga de gestionar
        la llegada de dicha familia.
    """
    sleep(random.random() * random.randint(20,40))
    print(f"La familia {fam} de tamaño {tam} llegó al establecimiento")
    # Se deberá de validar la disponibilidad para este tamaño de familia
    if tam == 1:
        llegadaFamilia(fam,tam,multiplexUno,mesasUno)
    elif tam == 2:
        llegadaFamilia(fam,tam,multiplexDos,mesasDos)
    else:
        llegadaFamilia(fam,tam,multiplexCuatro,mesasCuatro)
    


    
# Se crea la ventana principal de la interfaz gráfica
root = Tk() 
  
# Se definen los elementos de la interfaz gráfica
root.title("Restaurante concurrido")

# Crear un frame para el borde del restaurante
frame_restaurante = Frame(root,bg="dark green")
frame_restaurante.grid(row=2, column=0, rowspan=4, columnspan=3, sticky="nsew")


# Se crea el interior del restaurante
frame_mesas = Frame(frame_restaurante,bg="light goldenrod")
frame_mesas.grid(row=2, column=0, rowspan=4, columnspan=3, sticky="nsew",padx=10,pady=10)

# Crear botones para representar las mesas dentro del frame
mesasCuatro = {}
mesasDos = {}
mesasUno = {}
texto = ""
for fila in range(4):
    for columna in range(3):
        if columna == 0:
            texto = f"Mesa para 4: disponible"
        elif columna == 1:
            texto = f"Mesa para 2: disponible"
        else:
            texto = f"Mesa para 1: disponible"
        mesa_numero = fila * 3 + columna + 1
        mesa_button = Button(
            frame_mesas,
            text=texto,
            width=20,
            height=6,
            bg="brown",
            fg="green",
            state="normal"
        )
        if columna == 0:
            mesasCuatro[len(mesasCuatro)] = [True,mesa_button] # Al inicio, todas las mesas están disponibles
        elif columna == 1:
            mesasDos[len(mesasDos)] = [True,mesa_button]
        else:
            mesasUno[len(mesasUno)] = [True,mesa_button]
            pass
        mesa_button.grid(row=fila, column=columna, padx=40, pady=30)

"""
    En lo anterior se tiene un total de 3 columnas con 4 filas. Por lo que se tienen 12 mesas en total en el establecimiento.
    Las columnas son para diferentes tamaños de grupos:
    1. La primera columna es para grupos de 4 integrantes
    2. La segunda columna para grupos de 2
    3. La tercera columna para grupos de 1

    Se almacena la información de cada una de las mesas para modificar su estado cada que un grupo utilice la mesa o desocupe la misma.

"""


# Agregamos un botón más para comenzar la simulación
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

""" 
    Para agregarle sabor, se incluirá la opción de parar el servicio en cierto momento. Esto en caso de que haya una emergencia o
    vaya a ocurrir cierto evento especial, por ejemplo, la entrega de productos. En ese caso se quiere parar el acceso de las familias para poder 
    permitir el acceso a los proveedores de productos. Las familias que se encuentran dentro podrán salir hasta que termine dicho evento.
    
    Para este caso se considerará un apagador. Este hará que ya no sea posible el acceso a los grupos, debido que se necesita de los nuevos 
    productos para poder atenderlos de forma correcta. Las personas que ya se encontraban  dentro podrán terminar de comer y salir del 
    establecimiento sin problemas
"""