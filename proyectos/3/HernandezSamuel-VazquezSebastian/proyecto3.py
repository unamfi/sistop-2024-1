#Proyecto 3: Sistema de archivos
#Alumnos: Hernandez Hernandez Samuel y Vazquez Reyes Sebastian

import struct
from tkinter import *
from tkinter import ttk, filedialog
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
        string = cadena.decode("ascii")
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

#Funcion que lee y retorna el contenido leido desde una ubicacion en particular del archivo
def leercont (ini, tamaño):
    with open("fiunamfs.img", "rb") as diskito: 
        diskito.seek(ini)
        contenido = diskito.read(tamaño)
        return contenido

def limpiar_cadena(cadena):#Con esta funcion limpiamos una cadena dentro del directorio para compararla facilmente
    return cadena.strip('\0').rstrip()

def buscar(var):#Esta funcion se encarga de buscar un archivo en especifico del directorio y devolver sus datos mas importantes para trabajarlos
    nombre = var.get()
    for item in tabla.get_children():
        l = tabla.item(item, "text")
        if l == nombre:
            cadena2 = tabla.set(item, "Tamaño")
            cadena3 = tabla.set(item, "Cluster")
            break
    tamaño = int(cadena2)
    cluster = int(cadena3)
    cadenafull = limpiar_cadena(nombre)
    return tamaño, cluster, cadenafull

#La siguiente funcion mueve un objeto desde el disco hasta nuestro computador. La copia se hace directamente en el directorio del programa
def moverdesde(var):
    global cluster, directorioact
    tamaño, cl_ini, cadenafull = buscar(var)
    datos = leercont(cluster*cl_ini, tamaño) 

    for r,_, archivos in os.walk(directorioact):
        if cadenafull in archivos:
            nom=Label(frame2, text = "El archivo: "+cadenafull +" ya se encuentra en el direcotorio del programa", bg="gray71",fg="gray1",font=fonttext, wraplength=700)
            nom.pack()
            registrar_bitacora("Intento de mover el archivo " + cadenafull + ", pero ya existe en el directorio")
            break
        else:
            archcopy = open(cadenafull,"wb")
            archcopy.write(datos)
            archcopy.close()
            nom=Label(frame2, text = "El archivo: "+cadenafull +" se ha copiado exitosamente en el direcotorio del programa", bg="gray71",fg="gray1",font=fonttext, wraplength=700)
            nom.pack()
            registrar_bitacora("Archivo " + cadenafull + " copiado exitosamente al directorio del programa")
            break

def eliminar(var): #Esta funcion se encarga de eliminar el archivo del directorio que escoja el usuario
    global cluster, directorioact
    tamaño, cl_ini, cadenafull = buscar(var) 
    encontrar = False
    for i in range(0, (cluster*4), 64):
        r = limpiar_cadena(leerstring(cluster+i, 16))
        if r == cadenafull:
            with open("fiunamfs.img", "rb+") as diskito: 
                diskito.seek(cluster+i)
                diskito.write(b'/..............\x00')
                diskito.seek(cluster+i+16)
                diskito.write(b'\x00'*8)
                diskito.seek(cluster+i+24)
                diskito.write(b'00000000000000'*2)
                encontrar=True
    if encontrar==True:
        with open("fiunamfs.img", "rb+") as diskito: 
            diskito.seek(cluster*cl_ini)
            diskito.write(b'\x00'*tamaño)
        nom = Label(frame2, text="El archivo: " + cadenafull + " se ha eliminado exitosamente", bg="gray71", fg="gray1", font=fonttext, wraplength=700)
        nom.pack()
        registrar_bitacora(f"Eliminación del archivo: {cadenafull}")  # Registro en la bitácora
    else:
        nom = Label(frame2, text="El archivo: " + cadenafull + " ya ha sido eliminado", bg="gray71", fg="gray1", font=fonttext, wraplength=700)
        nom.pack()

def moverhacia(): #Funcion para mover un archivo a fiUNAMFS
    global cluster, directorioact
    #Ventana de seleccion de archivos para la funcion de mover archivos hacia FiUNAMFS
    archmover = filedialog.askopenfilename(initialdir=directorioact, title="Selecciona un archivo", filetypes=(("png files", "*.png"), ("all files", "*.*")))
    tamaño = os.path.getsize(archmover)
    nombre2, extension_archivo = os.path.splitext(archmover)
    print (str(tamaño))
    print (nombre2)
    print (extension_archivo)
    if (len(nombre2)+len(extension_archivo))>15:
        nom = Label(frame2, text="El nombre del archivo es demasiado grande", bg="gray71", fg="gray1", font=fonttext, wraplength=700)
        nom.pack()
        return
    for item in tabla.get_children():
        l = tabla.item(item, "text")
        if l == nombre2:
            nom = Label(frame2, text="Este archivo ya esta en el sistema", bg="gray71", fg="gray1", font=fonttext, wraplength=700)
            nom.pack()
            break
    nombre = "-"+ nombre2 + extension_archivo + " " * (14 - len(nombre))

# Función para identificar archivos fragmentados en el sistema de archivos, recorre todo el directorio para averiguarlo
def identificar_fragmentados():
    fragmentados = []
    with open("fiunamfs.img", "rb") as diskito:
        diskito.seek(1 * cluster) 
        entrada_tamano = 64  
        while True:
            entrada = diskito.read(entrada_tamano)
            if not entrada or len(entrada) < 24:  # Asegurarse de que la entrada sea lo suficientemente larga
                break
            tipo_archivo = entrada[0]  # Tipo de archivo
            cluster_inicial = struct.unpack("<I", entrada[20:24])[0]  # Cluster inicial
            tamano_archivo = struct.unpack("<I", entrada[16:20])[0]  # Tamaño del archivo

            # Verificar si el archivo ocupa más de un cluster (fragmentado)
            if tipo_archivo != 47 and tamano_archivo > cluster * 4:
                fragmentados.append((cluster_inicial, tamano_archivo))
    return fragmentados

# Función para desfragmentar el sistema de archivos
def desfragmentar():
    fragmentados = identificar_fragmentados()
    cambios = {}
    with open("fiunamfs.img", "r+b") as disco:
        for cluster_inicial, tamano_archivo in fragmentados:
            espacio_libre = encontrar_espacio_libre(disco, tamano_archivo)
            nuevo_cluster_inicial = espacio_libre // cluster
            
            registrar_bitacora(f"Moviendo archivo fragmentado desde el cluster {cluster_inicial} al cluster {nuevo_cluster_inicial}")
            
            cambios[cluster_inicial] = nuevo_cluster_inicial
            
            contenido_archivo = leercont(cluster * cluster_inicial, tamano_archivo)
            disco.seek(espacio_libre)
            disco.write(contenido_archivo)
    
    # Aplicar todos los cambios en el disco en una sola pasada
    for cluster_inicial, nuevo_cluster in cambios.items():
        disco.seek(1 * cluster + cluster_inicial * cluster)
        disco.write(struct.pack("<I", nuevo_cluster))
        disco.seek(cluster * cluster_inicial)
        disco.write(b'\x00' * tamano_archivo)
    nom = Label(frame2, text="Desfragmentacion completa", bg="gray71", fg="gray1", font=fonttext, wraplength=700)
    nom.pack()
    registrar_bitacora("Sistema de archivos desfragmentado exitosamente")

# Función para encontrar espacio libre en el disco
def encontrar_espacio_libre(disco, tamano_archivo):
    disco.seek(1 * cluster)  # Inicio del espacio de datos
    espacio_libre = b'\x00' * tamano_archivo  # Espacio libre requerido
    datos = disco.read()  # Leer todos los datos

    indice = datos.find(espacio_libre)  # Buscar la primera aparición del espacio libre
    while indice != -1:
        pos = disco.tell()
        disco.seek(pos + indice)
        if datos[indice:indice + tamano_archivo] == espacio_libre:
            return pos + indice
        indice = datos.find(espacio_libre, indice + 1)  # Buscar el siguiente espacio libre
    raise ValueError("No se encontró espacio suficiente para el archivo.")

#Esta funcion se encarga de registrar las acciones realizadas en la bitacora con su hora de entrada
def registrar_bitacora(accion):
    with open("bitacora.txt", "a") as bitacora:
        from datetime import datetime
        fecha_hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        bitacora.write(f"{accion}, {fecha_hora_actual}\n")

#Esta funcion le permite al usuario ver la bitacora   
def ver_bitacora():
    global directorioact
    bitacoraencont=False
    for r,_, archivos in os.walk(directorioact):
        if "bitacora.txt" in archivos:
            with open("bitacora.txt", "r") as bitacora:
                bitacora_content = bitacora.readlines()
                # Crear ventana para mostrar la bitácora
                ventana_bitacora = Toplevel(root)
                ventana_bitacora.title("Bitácora de operaciones")
                ventana_bitacora.geometry("500x500")
                bitacora_texto = Text(ventana_bitacora)
                bitacora_texto.pack(fill="both", expand=True)
                for linea in bitacora_content:
                    bitacora_texto.insert(END, linea)
            bitacoraencont = True
    if bitacoraencont==False:
        nom = Label(frame2, text="La bitacora no existe porque no se ha realizado alguna operacion", bg="gray71", fg="gray1", font=fonttext, wraplength=700)
        nom.pack()

"""---------------------------------------------------------------
A partir de aqui empieza el desarrollo de nuestra interfaz grafica
------------------------------------------------------------------"""

#Menu de seleccion para las funciones que le ofrecen al usuario escoger archivos dentro del directorio
def actualizarmove(bot):
    var=StringVar()
    neims = tabla.get_children()
    archivos = [tabla.item(item, "text") for item in neims]
    var.set(archivos[0])
    listado()
    move=OptionMenu(frame2, var, *archivos)
    bot11=Button (frame2, text="Escoger", bg="gray71",fg="gray1",font=fonttext, command=lambda: moverdesde(var))
    bot12=Button (frame2, text="Escoger", bg="gray71",fg="gray1",font=fonttext, command=lambda: eliminar(var))   
    bot13=Button (frame2, text="Aceptar", bg="gray71",fg="gray1",font=fonttext, command=lambda: desfragmentar()) 
    bot14=Button (frame2, text="Escoger", bg="gray71",fg="gray1",font=fonttext, command=lambda: moverhacia())   
    if (bot==bot6):
        return move, bot12
    elif (bot==bot4):
        return move, bot11
    elif (bot==bot7):
        return move, bot13
    elif (bot==bot5):
        return bot14 
    else: 
        bot11.place_forget()
        bot12.place_forget()
        bot13.place_forget()
        bot14.place_forget()
    
#Esta funcion da la apariencia a un boton de ser seleccionado cuando fue presionado. De esta forma no puede presionarse varias veces seguidas
#Tambien se encarga de mostrar el menu de la opcion que presiona el usuario
def presionado(boton):
    listado()
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
    ejecucion=1
    if (boton==bot1): #Segun el boton que presionemos, se ejecuta la tarea que el usuario pidio
        tabla.pack(fill="both", side=LEFT, expand=True)  
        actualizarmove(bot1)  
    if (boton==bot2): #Conocer el server
        validarserver()
        actualizarmove(bot2)
    if (boton==bot4): #Copiar desde
        nom=Label(frame2, text = "¿Que archivo deseas copiar?", bg="gray71",fg="gray1",font=fonttext)
        nom.pack()
        move, bot11 =actualizarmove(bot4)
        move.pack()
        bot11.place(x=75, y= 500)
    if (boton==bot5):
        nom=Label(frame2, text = "¿Que archivo deseas mover a FiUNAMFS?", bg="gray71",fg="gray1",font=fonttext)
        nom.pack()
        nom1=Label(frame2, text = "Ten presente: su nombre no debe exceder los 15 caracteres", bg="gray71",fg="gray1",font=fonttext)
        nom1.pack()
        bot14 =actualizarmove(bot5)
        bot14.place(x=75, y= 500)
    if (boton==bot6):
        nom=Label(frame2, text = "¿Que archivo deseas eliminar?", bg="gray71",fg="gray1",font=fonttext)
        nom.pack()
        move, bot12 =actualizarmove(bot6)
        move.pack()
        bot12.place(x=75, y= 500)
    if boton == bot7:  #Para desfragmentar
        nom=Label(frame2, text = "¿Que archivo deseas desfragmentar?", bg="gray71",fg="gray1",font=fonttext)
        nom.pack()
        move, bot13 =actualizarmove(bot7)
        move.pack()
        bot13.place(x=75, y= 500)
    if boton == bot8: #Para mostrar la bitacora
        ver_bitacora()
        actualizarmove(bot8)  

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

bot8=Button (frame1, text="Bitacora", font=fonttext, fg="white", bg="MediumPurple1", command=lambda: presionado(bot8))
bot8.place(x=60, y= 510)

bot3=Button (frame1, text="Salir del sistema", font=fonttext, fg="white", bg="MediumPurple1", command=root.quit)
bot3.place(x=33, y= 570)

#Frame pa decoracion
frame2=Frame(root, bg="gray71")
frame2.pack(fill="both",side=LEFT)
frame2.configure(width=700, height=700)

#Tabla para mostrar y almacenar los datos de los archivos del directorio
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

root.mainloop() 