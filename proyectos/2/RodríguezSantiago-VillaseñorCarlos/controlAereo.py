from tkinter import *
import threading
import time
import random

class Avion:
    def __init__(self,id,departure,contador,destino):
        self.id = id
        self.departure = departure
        self.contador = contador
        self.destino = destino

#Número de hilos
numAviones = 10

#Semáforos usados
pistaA1_mutex = threading.Semaphore(1)
terminal_mutex = threading.Semaphore(1)
terminalLlegada_mutex = threading.Semaphore(1)
filaA1_mutex = threading.Semaphore(1)
filaA2_mutex = threading.Semaphore(1)
pistaA2_mutex = threading.Semaphore(1)
datos_mutex = threading.Semaphore(1)

#Diccionario destinos por duracion
lugares = {8: ' Francia  ',10: ' Portugal ',15:'  Japón   ',3:'   EEUU   '}

#Variables usadas
id = 1000
departure = "-"
prueba2 = "-"
hora = 0
texto = "-"
textoEspera = "En camino"
textoLlegada = "LLegó"
textoCDMX = "Ciudad de México"
contadorA1 = 0
contadorA2 = 0
           


def tipoAvion1():
    global hora
    global id
    global contadorA1
    #Entra a la pista un avión a la vez
    #Creamos objeto avión
    
    datos_mutex.acquire()
    id = id + 1
    contadorA1 = contadorA1 + 1
    hora= hora + 1
    
    #Se asigna una duración de vuelo y en función de esa se desplegan los resultados
    #La duracion igual determina el lugar de origen
    #duracion = random.randint(2,5)
    duracion = random.choice((8,10,15,3))
    lugar = lugares.get(duracion)
    avion = Avion(id,hora,contadorA1,lugar)
    #print("Creamos avión: "+str(avion.id)+" en fila 1")
    datos_mutex.release()   
    #Uno modifica la cola a la vez
    #Modificamos terminal con mutex
    terminal_mutex.acquire()
    #Asignamos los valores a la terminal según el contador de llegada
    # El contador relaciona cada avión con una celda de la terminal 
    #print("Contador actual A1: "+str(contadorA1))
    if(avion.contador == 1):
        myLabelFlight1.config(text = "| " + str(avion.id) + " |")
        myLabelSalida1.config(text = "| " + str(avion.departure) + " |")
        myLabelDestino1.config(text = "| " + str(avion.destino) + " |")
        myLabelEstado1.config(text ="| " + textoEspera + " |")
        #print("Avión tipo 1 modificó horario a las : "+str(avion.departure))
    if(avion.contador == 2):
        myLabelFlight2.config(text = "| " + str(avion.id) + " |")
        myLabelSalida2.config(text = "| " + str(avion.departure) + " |")
        myLabelDestino2.config(text = "| " + str(avion.destino) + " |")
        myLabelEstado2.config(text ="| " + textoEspera + " |")
        #print("Avión tipo 1 modificó horario a las : "+str(avion.departure))
    if(avion.contador == 3):
        myLabelFlight3.config(text = "| " + str(avion.id) + " |")
        myLabelSalida3.config(text = "| " + str(avion.departure) + " |")
        myLabelDestino3.config(text = "| " + str(avion.destino) + " |")
        myLabelEstado3.config(text ="| " + textoEspera + " |")
        #print("Avión tipo 1 modificó horario a las : "+str(avion.departure))
    if(avion.contador == 4):
        myLabelFlight4.config(text = "| " + str(avion.id) + " |")
        myLabelSalida4.config(text = "| " + str(avion.departure) + " |")
        myLabelDestino4.config(text = "| " + str(avion.destino) + " |")
        myLabelEstado4.config(text ="| " + textoEspera + " |")
        #print("Avión tipo 1 modificó horario a las : "+str(avion.departure))
    if(avion.contador == 5):
        myLabelFlight5.config(text = "| " + str(avion.id) + " |")
        myLabelSalida5.config(text = "| " + str(avion.departure) + " |")
        myLabelDestino5.config(text = "| " + str(avion.destino) + " |")
        myLabelEstado5.config(text ="| " + textoEspera + " |")
        #print("Avión tipo 1 modificó horario a las : "+str(avion.departure))
    terminal_mutex.release()
    #Tiempo de vuelo
    time.sleep(duracion)
    #Aterizan de uno en uno 
    terminalLlegada_mutex.acquire()
    if(avion.contador == 1):
        myLabelEstado1.config(text = "| " + textoLlegada + " |")
    if(avion.contador == 2):
        myLabelEstado2.config(text = "| " + textoLlegada + " |")
    if(avion.contador == 3):
        myLabelEstado3.config(text = "| " + textoLlegada + " |")
    if(avion.contador == 4):
        myLabelEstado4.config(text = "| " + textoLlegada + " |")
    if(avion.contador == 5):
        myLabelEstado5.config(text = "| " + textoLlegada + " |")
    terminalLlegada_mutex.release() 

def tipoAvion2():
    
    global hora
    global id
    global contadorA2
    #Entra a la pista un avión a la vez
    #Creamos objeto avión
    datos_mutex.acquire()
    id = id + 1
    hora= hora + 1
    contadorA2 = contadorA2 + 1
    #duracion = random.randint(2,5)
    duracion = random.choice((8,10,15,3))
    lugar = lugares.get(duracion)
    avion = Avion(id,hora,contadorA2,lugar)
    #print("Creamos avión: "+str(avion.id)+" en fila 2")
    datos_mutex.release()
    #Modificamos terminal
    terminal_mutex.acquire() 
    if(avion.contador == 1):
        myLabelFlight6.config(text = "| " + str(avion.id) + " |")
        myLabelSalida6.config(text = "| " + str(avion.departure) + " |")
        myLabelDestino6.config(text = "| " + str(avion.destino) + " |")
        myLabelEstado6.config(text ="| " + textoEspera + " |")
        #print("Avión tipo 2 modificó horario a las : "+str(avion.departure))
    if(avion.contador == 2):
        myLabelFlight7.config(text = "| " + str(avion.id) + " |")
        myLabelSalida7.config(text = "| " + str(avion.departure) + " |")
        myLabelDestino7.config(text = "| " + str(avion.destino) + " |")
        myLabelEstado7.config(text ="| " + textoEspera + " |")
        #print("Avión tipo 2 modificó horario a las : "+str(avion.departure))
    if(avion.contador == 3):
        myLabelFlight8.config(text = "| " + str(avion.id) + " |")
        myLabelSalida8.config(text = "| " + str(avion.departure) + " |")
        myLabelDestino8.config(text = "| " + str(avion.destino) + " |")
        myLabelEstado8.config(text ="| " + textoEspera + " |")
        #print("Avión tipo 2 modificó horario a las : "+str(avion.departure))
    if(avion.contador == 4):
        myLabelFlight9.config(text = "| " + str(avion.id) + " |")
        myLabelSalida9.config(text = "| " + str(avion.departure) + " |")
        myLabelDestino9.config(text = "| " + str(avion.destino) + " |")
        myLabelEstado9.config(text ="| " + textoEspera + " |")
        #print("Avión tipo 2 modificó horario a las : "+str(avion.departure))
    if(avion.contador == 5):
        myLabelFlight10.config(text = "| " + str(avion.id) + " |")
        myLabelSalida10.config(text = "| " + str(avion.departure) + " |")
        myLabelDestino10.config(text = "| " + str(avion.destino) + " |")
        myLabelEstado10.config(text ="| " + textoEspera + " |")
        #print("Avión tipo 2 modificó horario a las : "+str(avion.departure))
    terminal_mutex.release()
    #Tiempo de vuelo
    time.sleep(duracion)
    #Aterizan de uno en uno 
    terminalLlegada_mutex.acquire()
    if(avion.contador == 1):
        myLabelEstado6.config(text = "| " + textoLlegada + " |")
    if(avion.contador == 2):
        myLabelEstado7.config(text = "| " + textoLlegada + " |")
    if(avion.contador == 3):
        myLabelEstado8.config(text = "| " + textoLlegada + " |")
    if(avion.contador == 4):
        myLabelEstado9.config(text = "| " + textoLlegada + " |")
    if(avion.contador == 5):
        myLabelEstado10.config(text = "| " + textoLlegada + " |")
    terminalLlegada_mutex.release() 


def Volar(tipoAvion):
    #Primer tipo de avión
    #print("Entra avión tipo: "+str(tipoAvion))
    if(tipoAvion == 1):
        tipoAvion1()
    if(tipoAvion == 2):
        tipoAvion2()


def Inicio():
    global numAviones
    #Cero es el número del administrador
    #Uno y dos es el número de los aviones
    for i in range(numAviones):  
        n=i
    
        n = random.randint(1,2)
        t = threading.Thread(target=Volar,args = (n,),daemon=True)
        t.start()

#Interfaz
root= Tk()
root.title('Aeropuerto')
#root.geometry('460x250')
root.configure(bg = "black")
#root.configure(bg = 'black')
myLabelTitle = Label(root,text = "Departure and Arrivals",bg = "black",fg = "goldenrod",pady=15, font = ('Arial', 40, 'bold'))
myLabelTitle.grid(row=0,column=0, columnspan=8,sticky=W+E+N+S)
#Encabezado Aeropuertos
myLabelAirport1 = Label(root,text ="Aeropuerto Int. De la Ciudad de México",bg = "navajowhite", font = ('Arial', 20, 'bold'))
myLabelAirport1.grid(row=1,column=0, columnspan=4,sticky=W+E+N+S)

myLabelAirport2 = Label(root,text = "Aeropuertos Int. ",bg = "navajowhite", font = ('Arial', 20, 'bold'))
myLabelAirport2.grid(row=1,column=4, columnspan=4,sticky=W+E+N+S)

#Encabezado tiempo de salida
myLabelTime1 = Label(root,text = "| Salida |",bg = "darkgoldenrod3",fg = "black" , font = ('Arial', 12, 'bold'))
myLabelTime1.grid(row=2,column=1,sticky=W+E+N+S)
myLabelTime2 = Label(root, text="| Salida |",bg = "darkgoldenrod3",fg = "black" , font = ('Arial', 12, 'bold'))
myLabelTime2.grid(row=2,column=5,sticky=W+E+N+S)

#Encabezado Vuelos
myLabelVuelo1 = Label(root,text = "| Vuelo |",bg = "darkgoldenrod3",fg = "black" , font = ('Arial', 12, 'bold'))
myLabelVuelo1.grid(row=2,column=0,sticky=W+E+N+S)
myLabelVuelo2 = Label(root, text=" | Vuelo |",bg = "darkgoldenrod3",fg = "black", font = ('Arial', 12, 'bold'))
myLabelVuelo2.grid(row=2,column=4,sticky=W+E+N+S)

#Encabezado Destino
myLabelDestination1 = Label(root,text = "| Destino |",bg = "darkgoldenrod3",fg = "black", font = ('Arial', 12, 'bold'))
myLabelDestination1.grid(row=2,column=2,sticky=W+E+N+S)
myLabelDestination2 = Label(root, text="| Desde |",bg = "darkgoldenrod3",fg = "black", font = ('Arial', 12, 'bold'))
myLabelDestination2.grid(row=2,column=6,sticky=W+E+N+S)

#Encabezado Estado
myLabelCurrently1 = Label(root,text = "| Estado |",bg = "darkgoldenrod3",fg = "black", font = ('Arial', 12, 'bold'))
myLabelCurrently1.grid(row=2,column=3,sticky=W+E+N+S)
myLabelCurrently2 = Label(root, text="| Estado |",bg = "darkgoldenrod3",fg = "black", font = ('Arial', 12, 'bold'))
myLabelCurrently2.grid(row=2,column=7,sticky=W+E+N+S)

#Texto Vuelos
myLabelFlight1 = Label(root, text=texto,bg = "black",fg = "white")
myLabelFlight1.grid(row=3,column=0)
myLabelFlight2 = Label(root, text=texto,bg = "black",fg = "white")
myLabelFlight2.grid(row=4,column=0)
myLabelFlight3 = Label(root, text=texto,bg = "black",fg = "white")
myLabelFlight3.grid(row=5,column=0)
myLabelFlight4 = Label(root, text=texto,bg = "black",fg = "white")
myLabelFlight4.grid(row=6,column=0)
myLabelFlight5 = Label(root, text=texto,bg = "black",fg = "white")
myLabelFlight5.grid(row=7,column=0)

myLabelFlight6 = Label(root, text=texto,bg = "black",fg = "white")
myLabelFlight6.grid(row=3,column=4)
myLabelFlight7 = Label(root, text=texto,bg = "black",fg = "white")
myLabelFlight7.grid(row=4,column=4)
myLabelFlight8 = Label(root, text=texto,bg = "black",fg = "white")
myLabelFlight8.grid(row=5,column=4)
myLabelFlight9 = Label(root, text=texto,bg = "black",fg = "white")
myLabelFlight9.grid(row=6,column=4)
myLabelFlight10 = Label(root, text=texto,bg = "black",fg = "white")
myLabelFlight10.grid(row=7,column=4)

#Texto lugares

myLabelDestino1 = Label(root, text=texto,bg = "black",fg = "white")
myLabelDestino1.grid(row=3,column=2)
myLabelDestino2 = Label(root, text=texto,bg = "black",fg = "white")
myLabelDestino2.grid(row=4,column=2)
myLabelDestino3 = Label(root, text=texto,bg = "black",fg = "white")
myLabelDestino3.grid(row=5,column=2)
myLabelDestino4 = Label(root, text=texto,bg = "black",fg = "white")
myLabelDestino4.grid(row=6,column=2)
myLabelDestino5 = Label(root, text=texto,bg = "black",fg = "white")
myLabelDestino5.grid(row=7,column=2)

myLabelDestino6 = Label(root, text=texto,bg = "black",fg = "white")
myLabelDestino6.grid(row=3,column=6)
myLabelDestino7 = Label(root, text=texto,bg = "black",fg = "white")
myLabelDestino7.grid(row=4,column=6)
myLabelDestino8 = Label(root, text=texto,bg = "black",fg = "white")
myLabelDestino8.grid(row=5,column=6)
myLabelDestino9 = Label(root, text=texto,bg = "black",fg = "white")
myLabelDestino9.grid(row=6,column=6)
myLabelDestino10 = Label(root, text=texto,bg = "black",fg = "white")
myLabelDestino10.grid(row=7,column=6)

#Texto Estado
myLabelEstado1 = Label(root, text=texto,bg = "black",fg = "white")
myLabelEstado1.grid(row=3,column=3)
myLabelEstado2 = Label(root, text=texto,bg = "black",fg = "white")
myLabelEstado2.grid(row=4,column=3)
myLabelEstado3 = Label(root, text=texto,bg = "black",fg = "white")
myLabelEstado3.grid(row=5,column=3)
myLabelEstado4 = Label(root, text=texto,bg = "black",fg = "white")
myLabelEstado4.grid(row=6,column=3)
myLabelEstado5 = Label(root, text=texto,bg = "black",fg = "white")
myLabelEstado5.grid(row=7,column=3)

myLabelEstado6 = Label(root, text=texto,bg = "black",fg = "white")
myLabelEstado6.grid(row=3,column=7)
myLabelEstado7 = Label(root, text=texto,bg = "black",fg = "white")
myLabelEstado7.grid(row=4,column=7)
myLabelEstado8 = Label(root, text=texto,bg = "black",fg = "white")
myLabelEstado8.grid(row=5,column=7)
myLabelEstado9 = Label(root, text=texto,bg = "black",fg = "white")
myLabelEstado9.grid(row=6,column=7)
myLabelEstado10 = Label(root, text=texto,bg = "black",fg = "white")
myLabelEstado10.grid(row=7,column=7)

#Texto horario de salida
myLabelSalida1 = Label(root, text=texto,bg = "black",fg = "white")
myLabelSalida1.grid(row=3,column=1)
myLabelSalida2 = Label(root, text=texto,bg = "black",fg = "white")
myLabelSalida2.grid(row=4,column=1)
myLabelSalida3 = Label(root, text=texto,bg = "black",fg = "white")
myLabelSalida3.grid(row=5,column=1)
myLabelSalida4 = Label(root, text=texto,bg = "black",fg = "white")
myLabelSalida4.grid(row=6,column=1)
myLabelSalida5 = Label(root, text=texto,bg = "black",fg = "white")
myLabelSalida5.grid(row=7,column=1)

myLabelSalida6 = Label(root, text=texto,bg = "black",fg = "white")
myLabelSalida6.grid(row=3,column=5)
myLabelSalida7 = Label(root, text=texto,bg = "black",fg = "white")
myLabelSalida7.grid(row=4,column=5)
myLabelSalida8 = Label(root, text=texto,bg = "black",fg = "white")
myLabelSalida8.grid(row=5,column=5)
myLabelSalida9 = Label(root, text=texto,bg = "black",fg = "white")
myLabelSalida9.grid(row=6,column=5)
myLabelSalida10 = Label(root, text=texto,bg = "black",fg = "white")
myLabelSalida10.grid(row=7,column=5)

#Buton inicio
myButton = Button(root, text="Start",command=threading.Thread(target=Inicio,daemon=True).start)
myButton.grid(row=8,column=3)
#Inicia ventana
#Botón salida
salida = Button(root, text = "Exit", command = root.quit)
salida.grid(row=8,column=4)
#Ícono
#root.iconbitmap('icon.ico')
root.mainloop()