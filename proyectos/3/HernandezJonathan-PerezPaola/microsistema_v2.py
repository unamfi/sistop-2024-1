# ¡Hola, hola! ¿Qué tal todo, amiguito?
# Bienvenido a la V2 del código. Esta versión puede contener errores y está sujeta a mejoras.
# Diferencias respecto a la V1: Se han añadido comentarios explicativos para comprender mejor las funciones.
# ¡Además! Se ha agregado un menú con diferentes opciones para interactuar con el archivo 'fiunamfs.img'.

# ¡Como sea! Sin más preámbulos.

# Integrantes:
# Hernández Ortiz Jonathan.
# Pérez Avin Paola Celina de Jesús.

import os
import struct

fiunamfs = "fiunamfs.img"

# Función para transformar una sección binaria en ASCII.
def tranformar_ascii(inicio, fin):
    global fiunamfs
    espacio = fin - inicio
    with open(fiunamfs,'rb') as fiunamfs:
        fiunamfs.seek(inicio)
        # Leemos la información y la decodificamos en Latin-1 -> ASCII 8 bits.
        info = fiunamfs.read(espacio).decode('ascii')
        return info

# Función para leer enteros en formato little-endian desde un archivo.
def leerEnteros(inicio, fin):
    espacio = fin - inicio
    # Modo de apertura 'r' para lectura.
    with open(fiunamfs,'rb') as fiunamfs:
        # Se tiene que ubicar el cabezal.
        fiunamfs.seek(inicio)
        # Se lee la información deseada.
        info = fiunamfs.read(espacio)
        info , *resto = struct.unpack('<I',info)
        return info
    
# Función para listar el contenido del directorio.
def lista_contenido():
    if os.path.isfile(fiunamfs):
        with open(fiunamfs,'r') as archivo:
            for caracter in enumerate(archivo):
                if caracter == "-":
                    print(caracter, end="")
    else:
        print(f"¡No existe el Archivo {fiunamfs}!")

# Menú de opciones.
print("ARCHIVOS SO: MENÚ")
print("1. Listar contenido del directorio.")
print("2. Copiar un archivo de FIUnamFS a archivo local.")
print("3. Copiar un archivo de la PC al archivo FIUnamFS.")
print("4. Eliminar un archivo de FIUnamFS.")
print("5. Desfragmentar FIUnamFS.")

# Solicitar al usuario una opción del menú.
opcion = int(input("Ingresa un valor del menu a realizar:\n"))
while opcion < 1 or opcion > 5:
    opcion = int(input("Ingrese una opción correcta:"))

# ¡Y a realizar acciones según la opción elegida!
match opcion:
    case 1:
        lista_contenido()
    case 2:
        print("¡Hola!")
    case 3:
        print("¡Hola!")
    case 4:
        print("¡Hola!")
    case 5:
        print("¡Hola!")
        
# Llamadas a las funciones para obtener información de la estructura del archivo.
identificador = tranformar_ascii(0, 8)
version = tranformar_ascii(10, 14)
etiquetaVolumen = tranformar_ascii(20, 39)
tamCluster = leerEnteros(40, 44)
numClusterDir = leerEnteros(45, 49)
clusterTotales = leerEnteros(50, 54)
entrada = 64
tam_total = 256
inicioDirectorio = tamCluster
finDirectorio = tamCluster * 4