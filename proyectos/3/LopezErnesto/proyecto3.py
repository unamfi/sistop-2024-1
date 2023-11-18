import os
import time
import struct
from time import sleep
import datetime
from datetime import *


# Ruta del archivo
ruta_imagen = "/Users/danjiro01/Downloads/fiunamfs.img"
# Se abre el archivo en modo lectura y escritura

# define our clear function
def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

# Mostrar menú
def mostrar_menu():
    print("\t\t\t********************************************")
    print("\t\t\t*              MENÚ PRINCIPAL              *")
    print("\t\t\t********************************************")
    print("\t\t\t* 1. Listar archivos                       *")
    print("\t\t\t* 2. Copiar archivo de FiUnamFs a sistema  *")
    print("\t\t\t* 3. Opción 3                              *")
    print("\t\t\t* 4. Opción 4                              *")
    print("\t\t\t* 5. Opción 5                              *")
    print("\t\t\t* 6. Información del sistema               *")
    print("\t\t\t* 7. Salir                                 *")
    print("\t\t\t********************************************")

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

archivos = {}

def mostrarInformacionSistema():
    print(f"\n\n\tINFORMACIÓN DEL SISTEMA: \n\n\t{'-'* (5+14+10+10+19+10)}")
    print(f'\t\tDatos del sistema de archivos: {identificador} {version}')
    print(f'\t\tEtiqueta del volumen: {etiquetaVolumen}')
    print(f'\t\tMedidas: \n\t\t\tCluster - {tamCluster} \n\t\t\tCluster del directorio - {numClusterDir} \n\t\t\tClusters totales - {clusterTotales}')
    print(f"\n\t{'-'* (5+14+10+10+19+10)}")

def guardarInformacionArchivos():
    # Se mostrarán únicamente los archivos que tienen un nombre específico
    # Se deberá de recorrer el directorio
    cabezal = inicioDir
    while(cabezal != finDir):
        archivo = {}
        with open(ruta_imagen,'rb') as FiUnamFs:
            FiUnamFs.seek(cabezal)
            # Se revisa si es una entrada con contenido o vacía
            entrada = leerAscii(cabezal,1)
            if entrada == '-':
                # Se lee el resto
                archivo['nombre'] = leerAscii(cabezal + 1, 14) # Se lee el nombre real
                archivo['tam'] = leerEnteros(cabezal + 16, 4) # Se lee el tamaño
                archivo['clusterInicial'] = leerEnteros(cabezal + 20, 4) # Se lee el tamaño del cluster
                fecha_objeto = datetime.strptime(leerAscii(cabezal + 24, 13), "%Y%m%d%H%M%S")
                cadena_formateada = fecha_objeto.strftime("%Y-%m-%d %H:%M:%S")
                archivo['fechaC'] = cadena_formateada # Se lee hora y fecha de creación del archivo
                fecha_objeto = datetime.strptime(leerAscii(cabezal + 38, 13), "%Y%m%d%H%M%S")
                cadena_formateada = fecha_objeto.strftime("%Y-%m-%d %H:%M:%S")
                archivo['fechaM'] = cadena_formateada # Se lee hora y fecha de creación del archivo
                # Se guardar la información de los archivos que tienen información
                archivos[archivo['nombre'].rstrip()] = archivo
                cabezal += 64
                pass
            else:
                # Se ignora y se avanza el cabezalg
                cabezal += 64

# Listar los elementos del directorio
def listarContenidos():
    # Se mostrarán únicamente los archivos que tienen un nombre específico
    print(f"\n\n\tARCHIVOS: \n\n\t{'-'* (5+14+10+10+19+10)}")
    for i,archivo in enumerate(archivos.items()):
        print(f"{i:>5}.- {archivo[0]:<14}: {archivo[1]['tam']:<10} -- {archivo[1]['fechaC']} -- {archivo[1]['fechaM']}")
    print(f"\n\t{'-'* (5+14+10+10+19+10)}")

def copiarArchivoASistema():
    print("\tIngrese la ruta donde desea copiar el archivo del sistema FiUnamFs:")
    ruta = input(" ").rstrip().lstrip()
    print("\tIngrese el nombre del archivo a copiar:")
    nombre = input(" ").rstrip().lstrip()
    # Primero se debe validar que el nombre del archivo exista
    if nombre in archivos:
        # Se encntró el archivo, por lo tanto se procede a copiar (en caso de que la ruta sea la correcta y no exista el archivo)
        if (os.path.exists(ruta) and ((os.path.exists(ruta + "/" + nombre) == False and os.name == 'posix') or (os.path.exists(ruta + "\\" + nombre) == False and os.name == 'nt'))):
            # Se copia el archivo, para lo cual se necesitan los datos
            contenido = leerInfo(archivos[nombre]['clusterInicial'] * tamCluster,archivos[nombre]['tam'])
            if os.name == 'posix':
                with open(ruta + "/" + nombre,'wb') as archivo:
                    archivo.write(contenido)
                print("\n\tARCHIVO GUARDADO EXITOSAMENTE")
            else:
                with open(ruta + "\\" + nombre,'wb') as archivo:
                    archivo.write(contenido)
                print("\n\tARCHIVO GUARDADO EXITOSAMENTE")
        else: 
            print("ERROR: La ruta especificada no existe o el archivo ya se encuentra en dicha ruta.")
    else:
        print("\tERROR: No existe un archivo con ese nombre")
    
# INICIO
sesionActiva = True
guardarInformacionArchivos()
print(archivos)
while(sesionActiva):
    mostrar_menu()
    opcion = input('\n\n\tSelecciona la opción deseada (cls - limpiar pantalla): ')
    if opcion == '1':
        listarContenidos()
    elif opcion == '2':
        copiarArchivoASistema()
        pass
    elif opcion == '3':
        pass
    elif opcion == '4':
        pass
    elif opcion == '5':
        pass
    elif opcion == '6':
        mostrarInformacionSistema()
    elif opcion == '7':
        print("\tCerrando sistema de archivos...")
        sleep(1)
        break
    elif opcion == 'cls':
        clear()
        pass
    else:
        print("\tERROR. Favor de seleccionar una opción válida")
        sleep(1)

# listarContenidos()
