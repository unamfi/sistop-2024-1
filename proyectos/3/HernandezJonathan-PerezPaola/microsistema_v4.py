# Proyecto 3 | Sistemas Operativos | FI UNAM.

# ¡Hola, hola! ¡Ya estamos cerca del final!
# Bienvenido a la V4 del código. Esta versión presenta una serie de diferencias importantes.
# Tras detectar y abordar varios errores en las versiones anteriores (mencionados en la documentación),
# se optó por iniciar este código desde cero con una visión más apta y una estrategia mejor definida.
# Esta versión representa un enfoque más estructurado en comparación con las versiones previas (V1, V2, V3),
# buscando mejorar la funcionalidad del menú, la gestión de archivos y la interacción con el sistema 'FIUNAMFS'.

# * Diferencias con versiones anteriores:
# - Incorporación de funciones nuevas.
# - Corrección de algunos errores y optimización del código.
# - Mayor funcionalidad y manejo de archivos en 'fiunamfs.img'.
# * Se ha puesto especial énfasis en la comprensión y claridad del código, 
#   así como en la implementación de nuevas funcionalidades.

# Integrantes:
# Hernández Ortiz Jonathan.
# Pérez Avin Paola Celina de Jesús.

# Esta *NO* es la versión final del código, pero estamos cerca.

# Importación de librerías necesarias.
import os
import time
from struct import pack, unpack
import struct
import shutil

opcion = 0

# Función del menú del programa.
def menu():
    global opcion
    # Ciclo infinito hasta que el usuario ingrese 5 para salir del programa.
    while opcion != 5:
        # Apertura del archivo 'fiunamfs.img' para trabajar con él.
        sistema_archivos = open("fiunamfs.img", "r+b")
        # Obtención del tamaño del archivo 'fiunamfs.img'.
        # Básicamente, se lee el peso de 'fiunamfs'.
        tamano_sistema_archivos = os.stat("fiunamfs.img").st_size
        
        # Mostrar las opciones disponibles del menú.
        print("\n Opciones: \n")
        print("---1. Listar de contenido de FIUNAMFS---")
        print("---2. Copiar archivo de FIUNAMFS a PC---")
        print("---3. Copiar archivo de PC a FIUNAMFS---")
        print("---4. Eliminar archivo de FiUnamFS---")
        print("---5. Salir del Programa---")
        # Solicitamos al usuario que ingrese una opción del menú.
        opcion = int(input("\n\n****Ingresa una opción: "))
        
        # Si se elige la opción 1, se listan los archivos existentes en 'fiunamfs'.
        if opcion == 1:
            listar_archivos(sistema_archivos, cluster)

# Función para leer información del sistema de archivos.
def leer_info_sistema_archivos(sistema_archivos, offset, longitud):
    # Establece la posición del puntero en el archivo.
    sistema_archivos.seek(offset)
    # Lee y devuelve la información del sistema de archivos de acuerdo a la longitud.
    return sistema_archivos.read(longitud).decode("ascii")

# Función para leer un número entero del sistema de archivos.
# Devuelve el valor calculado de los cluster iniciales, correspondientes a los archivos.
def leer_entero(sistema_archivos, offset, formato='<I'):
    # Establece la posición del puntero en el archivo.
    sistema_archivos.seek(offset)
    # Lee y retorna un número entero del sistema de archivos.
    return struct.unpack(formato, sistema_archivos.read(struct.calcsize(formato)))[0]


# Función para listar archivos existentes en FIUNAMFS.
def listar_archivos(sistema_archivos, cluster):
    # Establece la posición del archivo en el cluster.
    sistema_archivos.seek(cluster)
    
    # Itera a través de los clusters para encontrar archivos.
    # Vamos a recorrer desde 1 hasta cluster *4 en pasos de 64.
    for i in range(1, cluster * 4, 64):
        # Se mueve el fichero a la posición cluster + i.
        sistema_archivos.seek(cluster + i)
        # Se añade a la variable 'archivo' el 'fiunamfs', para que lea los 15 y codifique a ASCII.
        # Lee el nombre del archivo del sistema de archivos y lo muestra si no está vacío.
        archivo = sistema_archivos.read(15).decode("ascii")
        
        # Si en 'archivos' los 15 valores siguientes son diferentes de  "...............".
        if archivo[:14] != "..............":
            # Si se cumple, ingresamos y asignamos el tamaño del archivo a 'Peso'.
            Peso = struct.unpack('<' + 'I'*1, sistema_archivos.read(4))[0]
            # Si el tamaño es distinto de cero, significa que contiene información.
            if Peso != 0 :
                # Se procede a imprimir el nombre del archivo, su tamaño (Peso), y el cluster inicial correspondiente.
                print("\nArchivo:", archivo.strip().replace("-", ""), "Peso:", struct.unpack('<' + 'I'*1, sistema_archivos.read(4))[0], 'Cluster inicial', struct.unpack('<' + 'I'*1, sistema_archivos.read(4))[0])
                
# Se asignan constantes necesarias.
sector = 256
cluster = sector * 4
# Se abre el archivo "fiunamfs.img".
# Estableciendo que 'sistema_archivos' es igual a todo lo relacionado a 'fiunamfs'.
sistema_archivos = open("fiunamfs.img", "r+b")

# Se inicia la función de menú.
menu()