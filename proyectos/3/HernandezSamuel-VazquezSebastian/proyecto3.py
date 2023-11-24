#Proyecto 3: Sistema de archivos
#Alumnos: Hernandez Hernandez Samuel y Vazquez Reyes Sebastian

import struct
from tkinter import *
from tkinter import ttk
from pathlib import Path
import os

#Variables globales que nos ayudan a lo largo del programa
sector=256
cluster=sector*8
estadoboton=0
ejecucion=0
botonrep=Button
directorioact = os.getcwd()

#Funcion que lee enteros en el archivo fuente
def leerint(pocision, numero):
    with open("fiunamfs.img", "rb") as diskito: 
        diskito.seek(pocision)
        dato = diskito.read(numero)
        num= struct.unpack("<I", dato)[0]
        return num

#Funcion que lee cadenas en el archivo fuente
def leerstring(pocision, numero):
    with open("fiunamfs.img", "rb") as diskito: 
        diskito.seek(pocision)
        cadena = diskito.read(numero)
        string = cadena.decode('ascii')
        return string

#Funcion que recopila la informacion del server ubicada en el primer cluster
def validarserver():
    neim = leerstring(0,9)
    version = leerstring(10,5)
    etiqueta = leerstring(20,20)
    tamaño = leerint(40,4)
    cantidadclusters = leerint(45,4)
    ccl = leerint(50,4)
    #se imprimen en la interfaz las caracteristicas del sistema
    nom=Label(frame2, text = "El sistema se llama: "+neim, bg="gray71",fg="gray1",font=fonttext)
    nom.pack()
    nom=Label(frame2, text = "La version es: "+version, bg="gray71",fg="gray1",font=fonttext)
    nom.pack()
    nom=Label(frame2, text = "Etiqueta del volumen: "+etiqueta, bg="gray71",fg="gray1",font=fonttext)
    nom.pack()
    nom=Label(frame2, text = "Tamaño del Cluster: "+str(tamaño)+" bytes", bg="gray71",fg="gray1",font=fonttext)
    nom.pack()
    nom=Label(frame2, text = "Numero de clusters que mide el directorio: "+str(cantidadclusters), bg="gray71",fg="gray1",font=fonttext)
    nom.pack()
    nom=Label(frame2, text = "Numero de clusters que mide toda la unidad: "+str(ccl), bg="gray71",fg="gray1",font=fonttext)
    nom.pack()
    

#Funcion que lista el contenido del directorio, ignorando las entradas vacias
def listado():
    tabla.delete(*tabla.get_children())
    for i in range (0, (cluster*4), 64):
        r=leerstring(cluster+i,16)
        if (r[0]!="/"):
            a=leerint(cluster+i+16,4)
            b=leerint(cluster+i+20,4)
            c=leerstring(cluster+i+24,14) 
            d=leerstring(cluster+i+38,14)        
            tabla.insert("", END, text=r, values=(a,b,c,d))#se almacenan en la tabla de archivos los datos del disco

def leercont (ini, tamaño):
    with open("fiunamfs.img", "rb") as diskito: 
        diskito.seek(ini)
        contenido = diskito.read(tamaño)
        return contenido

#La siguiente funcion mueve un objeto desde el disco hasta nuestro computador. La copia se hace directamente en el directorio del programa
def moverdesde(var):
    global cluster, directorioact
    nombre=var.get()
    for item in tabla.get_children():
        l = tabla.item(item, "text")
        if l == nombre:
            cadena2 = tabla.set(item, "Tamaño")
            cadena3 = tabla.set(item, "Cluster")
            break

    tamaño = int(cadena2)
    cl_ini = int (cadena3)  
    datos = leercont(cluster*cl_ini, tamaño) 
    cadenasn = nombre.replace("\0", "")
    cadenasg = " ".join(cadenasn.split())
    cadenafull = cadenasg[1:]
    for r,_, archivos in os.walk(directorioact):
        if cadenafull in archivos:
            nom=Label(frame2, text = "El archivo: "+cadenafull +" ya se encuentra en el direcotorio del programa", bg="gray71",fg="gray1",font=fonttext, wraplength=700)
            nom.pack()
            break
        else:
            archcopy = open(cadenafull,"wb")
            archcopy.write(datos)
            archcopy.close()
            nom=Label(frame2, text = "El archivo: "+cadenafull +" se ha copiado exitosamente en el direcotorio del programa", bg="gray71",fg="gray1",font=fonttext, wraplength=700)
            nom.pack()
            break

"""-------------------------------------------------------------
A partir de aqui empieza el desarrollo de mi interfaz grafica
-------------------------------------------------------------"""

#Esta funcion da la apariencia a un boton de ser seleccionado cuando fue presionado. De esta forma no puede presionarse varias veces seguidas
def presionado(boton):
    bot11.place_forget()
    frame2.pack(fill="both",side=LEFT)
    global estadoboton, botonrep, ejecucion
    if estadoboton==1:
            botonrep.config(state=NORMAL)
            botonrep.config(relief=RAISED)
    elif estadoboton==0:
        estadoboton=1
    if ejecucion==1:
        for widget in frame2.winfo_children():
            widget.pack_forget()
        ejecucion = 0
    botonrep=boton
    boton.config(state=DISABLED)
    boton.config(relief=SUNKEN)
    if (boton==bot1): #Segun el boton que presionemos, se ejecuta la tarea que el usuario pidio
        listado()
        tabla.pack(fill="both", side=LEFT, expand=True)    
        ejecucion=1
    if (boton==bot2):
        validarserver()
        ejecucion=1
    if (boton==bot4):
        listado()
        nom=Label(frame2, text = "¿Que archivo deseas copiar?", bg="gray71",fg="gray1",font=fonttext)
        nom.pack()
        move.pack()
        bot11.place(x=75, y= 500)
        ejecucion=1

#Parametros basicos de la ventana y las cadenas
root = Tk()
root.title("Proyecto 3: Sistema de archivos")
root.geometry("700x700")
fonttext= ("Times New Roman", 14)

#Frame para el titulo de la interfaz
tit=Frame(root, bg="navy")
tit.pack(fill="x", side=TOP)
tit.configure(width=500, height=75)
tit1=Label(tit, text = "BIENVENIDO A TU SISTEMA DE ARCHIVOS", bg="navy",fg="white",font=("Times New Roman",17))
tit1.pack()
tit1=Label(tit, text = "¿Que deseas hacer?", bg="navy",fg="white",font=fonttext)
tit1.pack()

#Frame para el menu de seleccion de operaciones de la interfaz
frame1=Frame(root, bg="MediumPurple1")
frame1.pack(fill="y",side=LEFT)
frame1.configure(width=200, height=700)
#Botones del frame de seleccion
bot1=Button (frame1, text="Listar los elementos\ndel directorio", font=fonttext, fg="white", bg="MediumPurple1", command=lambda: presionado(bot1))
bot1.place(x=20, y= 80)
bot2=Button (frame1, text="Conocer al server", font=fonttext, fg="white", bg="MediumPurple1", command=lambda: presionado(bot2))
bot2.place(x=27, y= 10)
bot4=Button (frame1, text="Copiar DESDE\nEL directorio", font=fonttext, fg="white", bg="MediumPurple1",  command=lambda: presionado(bot4))
bot4.place(x=40, y= 180)
bot5=Button (frame1, text="Copiar HACIA\nEL directorio", font=fonttext, fg="white", bg="MediumPurple1",  command=lambda: presionado(bot5))
bot5.place(x=40, y= 270)
bot6=Button (frame1, text="Eliminar un archivo", font=fonttext, fg="white", bg="MediumPurple1",  command=lambda: presionado(bot6))
bot6.place(x=22, y= 360)
bot7=Button (frame1, text="Desfragmentar\nel sistema", font=fonttext, fg="white", bg="MediumPurple1",  command=lambda: presionado(bot7))
bot7.place(x=35, y= 430)
bot3=Button (frame1, text="Salir del sistema", font=fonttext, fg="white", bg="MediumPurple1", command=root.quit)
bot3.place(x=33, y= 530)

#Frame pa decoracion
frame2=Frame(root, bg="gray71")
frame2.pack(fill="both",side=LEFT)
frame2.configure(width=700, height=700)

#Tabla para mostrar los archivos del directorio
tabla=ttk.Treeview(frame2, height=50, columns=("Tamaño", "Cluster", "Fecha de creación", "Ultima modificación"))
tabla.column("#0", width=120)
tabla.column("Tamaño", width=80, anchor=CENTER)
tabla.column("Fecha de creación", width=120, anchor=CENTER)
tabla.column("Ultima modificación", width=120, anchor=CENTER)
tabla.heading("#0", text="Nombre", anchor=CENTER)
tabla.heading("Tamaño", text="Tamaño", anchor=CENTER)
tabla.heading("Cluster", text="Cluster inicial", anchor=CENTER)
tabla.heading("Fecha de creación",text="Fecha de creación", anchor=CENTER)
tabla.heading("Ultima modificación", text="Ultima modificación", anchor=CENTER)

listado()
#Menu de seleccion para las funciones de mover y eliminar archivos
var=StringVar()
neims = tabla.get_children()
archivos = [tabla.item(item, "text") for item in neims]
var.set(archivos[0])
move=OptionMenu(frame2, var, *archivos)
bot11=Button (frame2, text="Escoger", bg="gray71",fg="gray1",font=fonttext, command=lambda: moverdesde(var))

root.mainloop() 