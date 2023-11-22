#Proyecto 3: Sistema de archivos
#Alumnos: Hernandez Hernandez Samuel y Vazquez Reyes Sebastian
#Dentro de un dispositivo puedo tener varias particiones en cada una defino un volumen descrito por un superbloque

import struct
import os
import tkinter as tk

sector=256//8
cluster=sector*4

def leerint(pocision, numero):
    with open("fiunamfs.img", "rb") as diskito: 
        diskito.seek(pocision)
        dato = diskito.read(numero)
        num = struct.unpack("<I", dato)[0]
        return num

def leerstring(pocision, numero):
    with open("fiunamfs.img", "rb") as diskito: 
        diskito.seek(pocision)
        cadena = diskito.read(numero)
        string = cadena.decode('ascii')
        return string

def validarserver():
    neim = leerstring(0,9)
    version = leerstring(10,5)
    etiqueta = leerstring(20,20)
    tamaño = leerint(40,4)
    cantidadclusters = leerint(45,4)
    ccl = leerint(50,4)
    print ("Nombre del server: "+ neim)
    print ("Version del server: "+ version)
    print ("Etiqueta del volumen: "+ etiqueta)
    print ("El cluster del sistema mide: "+ str(tamaño) + " bytes")
    print ("Este directorio mide: "+ str(cantidadclusters) + " cluster(s)")
    print ("La unidad completa mide: "+ str(ccl) + " clusters")

def listado():
    print ("Etiqueta del volumen: "+ etiqueta)  

def mostrar_listado(datos):
    ventana = tk.Tk()
    ventana.title("Listado de Datos")

    # Crear una etiqueta para mostrar los datos
    etiqueta = tk.Label(ventana, text="\n".join(datos), font=("Arial", 12))
    etiqueta.pack()

    # Botón para cerrar la ventana
    boton_cerrar = tk.Button(ventana, text="Cerrar", command=ventana.destroy)
    boton_cerrar.pack(pady=10)

    ventana.mainloop()

# Datos de ejemplo
datos_ejemplo = ["Dato 1", "Dato 2", "Dato 3", "Dato 4"]

# Llamar a la función para mostrar el listado
mostrar_listado(datos_ejemplo)

#validarserver()