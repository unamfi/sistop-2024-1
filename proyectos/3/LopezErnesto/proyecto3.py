"""
Lo que ustedes deben desarrollar es un programa que pueda obtener, 
crear y modificar información en el micro-sistema-de-archivos 
de la Facultad de Ingeniería, FiUnamFS.

Siguiendo la especificación que aparece en la siguiente sección, 
tienen que desarrollar un programa que pueda:

- Listar los contenidos del directorio
- Copiar uno de los archivos de dentro del FiUnamFS hacia tu sistema
- Copiar un archivo de tu computadora hacia tu FiUnamFS
- Eliminar un archivo del FiUnamFS
- Desafortunadamente, este sistema de archivos simplote es muy dado a la fragmentación externa. Generen también un programa que desfragmente al FiUnamFS. 
Ojo, la defragmentación debe hacerse dentro del sistema de archivos (no creando un sistema de archivos nuevo y copiando hacia éste).


NOTAS:

- Simulación de una memoria de 1440 KB.
- Las cadenas de texto deberán de estar codificadas en ASCII 8-bit.
- Enteros representados en 32 bits. Es decir, en little endian. 32 bits -> 4 bytes -> 2 bytes hexa
- Sectores de 256 bytes. sect_por_clutes = 256
- No hay particiones. Hay un solo volumen
- Solo se considera un directorio plano. No hay subdirectorios

NOTA: Con lo anterior podemos decir que solamente hay un SB, un directorio raíz y los respectivos archivos almacenados

- Toda la información de los archivos está en el directorio
- Ubicación del directorio -> Clusters 1 a 4
- Las entradas del directorio miden 64 bytes

"""

import struct
import os
import time
import datetime
import math

# Ruta del archivo
ruta_imagen = "/Users/danjiro01/Downloads/fiunamfs.img"
# Se abre el archivo en modo lectura y escritura
# FiUnamFS = open(ruta_imagen,'rb+')

# Para la información de números enteros, se deberá de utilizar unpack
def leerEnteros(cabezal,tam):
    global ruta_imagen
    # Modo de apertura 'r' para lectura
    with open(ruta_imagen,'rb') as FiUnamFS:
        # Se tiene que ubicar el cabezal
        FiUnamFS.seek(cabezal)
        # Se lee la información deseada
        contenido = FiUnamFS.read(tam)
        contenido, *resto = struct.unpack('<I',contenido)
        return contenido

# Las cadenas de texto se procesaran como ASCII-8
def leerAscii(cabezal,tam):
    global ruta_imagen
    with open(ruta_imagen,'rb') as FiUnamFs:
        FiUnamFs.seek(cabezal)
        # Leemos la información y la decodificamos en Latin-1 -> ASCII 8 bits
        contenido = FiUnamFs.read(tam).decode('Latin-1')
        return contenido
    
# Para pruebas, se tiene la lectura de información de bruto
def leerInfo(cabezal,tam):
    global ruta_imagen
    with open(ruta_imagen,'rb') as FiUnamFs:
        FiUnamFs.seek(cabezal)
        # Leemos la información de bruto
        contenido = FiUnamFs.read(tam)
        return contenido

# Se recupera la información del superbloque. Esta deberá de ser de acceso global para todos
identificador = leerAscii(0,8)
version = leerAscii(10,4)
etiquetaVolumen = leerAscii(20,19)
tamCluster = leerEnteros(40,4)
numClusterDir = leerEnteros(45,4)
clusterTotales = leerEnteros(50,4)
entradasDirectorio = 64
tamSectores = 256
inicioDir = tamCluster
finDir = tamCluster * 4


print(f'Datos del sistema de archivos: {identificador} {version}')
print(f'Etiqueta del volumen: {etiquetaVolumen}')
print(f'Medidas: \n\tCluster - {tamCluster} \n\tCluster del directorio - {numClusterDir} \n\tClusters totales - {clusterTotales}')

def listarContenidos():
    # Se mostrarán únicamente los archivos que tienen un nombre específico
    # Se deberá de recorrer el directorio
    cabezal = inicioDir
    while(cabezal != finDir):
        with open(ruta_imagen,'rb') as FiUnamFs:
            FiUnamFs.seek(cabezal)
            # Se revisa si es una entrada con contenido o vacía
            entrada = leerAscii(cabezal,1)
            if entrada == '-':
                # Se lee el resto
                nombre = leerAscii(cabezal + 1, 15) # Se lee el nombre
                tam = leerEnteros(cabezal + 16, 4) # Se lee el tamaño
                clusters = leerEnteros(cabezal + 20, 4) # Se lee el tamaño del cluster
                fechaC = leerAscii(cabezal + 24, 13) # Se lee hora y fecha de creación del archivo
                fechaM = leerAscii(cabezal + 38, 13) # Se lee hora y fecha de modificación del archivo
                # Se imprime con formato
                print(f'{nombre} -- {tam} BYTES -- {fechaC} -- {fechaM}')
                cabezal += 64
                pass
            else:
                # Se ignora y se avanza el cabezal
                cabezal += 64

listarContenidos()