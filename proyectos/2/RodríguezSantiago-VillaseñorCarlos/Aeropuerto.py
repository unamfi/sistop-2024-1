from tkinter import *
import threading
import time
import random


numAviones = 6

pistaA1_mutex = threading.Semaphore(1)
terminal_mutex = threading.Semaphore(1)
pistaA2_mutex = threading.Semaphore(1)

prueba = "-"
prueba2 = "-"
cont = 0
pistaA1 = []
pistaD1 = []

pistaA2 = []
pistaD2 = []


def tipoAvion0():
    global prueba
    global cont
    #Entra a la pista un avión a la vez
    pistaA1_mutex.acquire()
    #Modificamos terminal con mutex
    terminal_mutex.acquire()
    cont= cont + 1
    prueba = "300"+str(cont)
    myLabel.configure(text=prueba)
    print("Avión tipo 0 modificó inf a: "+prueba)
    terminal_mutex.release()
    pistaA1_mutex.release()

def tipoAvion1():
    global prueba2
    global cont
    #Entra a la pista un avión a la vez
    pistaA2_mutex.acquire()
    #Modificamos terminal con mutex
    terminal_mutex.acquire()
    cont = cont + 1
    prueba2 = "200"+str(cont)
    myLabel2.configure(text=prueba2)
    print("\nAvión tipo 1 modificó inf a: "+prueba2)
    terminal_mutex.release()
    pistaA2_mutex.release()


def Volar(tipoAvion):
    #Primer tipo de avión
    print("Entra avión tipo: "+str(tipoAvion))
    if(tipoAvion == 0):
        tipoAvion0()
    if(tipoAvion == 1):
        tipoAvion1()


def Inicio():
    global numAviones
    for i in range(numAviones):  
        n=i
        if(i > 1):
            n = random.randint(0,1)
        t = threading.Thread(target=Volar,args = (n,),daemon=True)
        t.start()

#Interfaz
root= Tk()
root.title('Aeropuerto')
myLabel = Label(root, text=prueba)
myLabel.grid(row=0,column=0)
myLabel2 = Label(root, text=prueba2)
myLabel2.grid(row=0,column=1)
myButton = Button(root, text="iniciar",command=threading.Thread(target=Inicio,daemon=True).start)
myButton.grid(row=2,column=0)
#Inicia ventana
root.mainloop()




