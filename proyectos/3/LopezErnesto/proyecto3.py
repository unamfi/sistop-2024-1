import os
import time
import struct
from time import sleep
from datetime import *
from math import ceil


# Ruta del archivo
ruta_imagen = "/Users/danjiro01/Downloads/fiunamfs.img"
# Se abre el archivo en modo lectura y escritura

# define our clear function
def clear():
    os.system('clear')

# Mostrar menú
def mostrar_menu():
    print("\t\t\t********************************************")
    print("\t\t\t*              MENÚ PRINCIPAL              *")
    print("\t\t\t********************************************")
    print("\t\t\t* 1. Listar archivos                       *")
    print("\t\t\t* 2. Copiar archivo de FiUnamFs a sistema  *")
    print("\t\t\t* 3. Copiar archivo de sistema a FiUnamFs  *")
    print("\t\t\t* 4. Eliminar archivo de FiUnamFs          *")
    print("\t\t\t* 5. Defragmentar                          *")
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
    
def escribirAscii(cabezal,contenido):
    global ruta_imagen
    with open(ruta_imagen,'rb+') as FiUnamFs:
        FiUnamFs.seek(cabezal)
        FiUnamFs.write(contenido.encode('Latin-1'))

def escribirEnteros(cabezal,contenido):
    global ruta_imagen
    with open(ruta_imagen,'rb+') as FiUnamFs:
        FiUnamFs.seek(cabezal)
        FiUnamFs.write(struct.pack('<I',contenido))

# Se recupera la información del superbloque. Esta deberá de ser de acceso global para todos
identificador = leerAscii(0,8)
version = leerAscii(10,4)
etiquetaVolumen = leerAscii(20,19)
tamCluster = leerEnteros(40,4)
numClusterDir = leerEnteros(45,4)
clusterTotales = leerEnteros(50,4)
numEntradas = 128
entradasDirectorio = 64
tamSectores = 256
inicioDir = tamCluster
finDir = inicioDir + 4 * tamCluster

archivos = {}
entradasLibres = []

# Revisar que está pasando 
def escribirDirectorio(nombre,tam,cabezal,fechaModificacion,fechaCreacion):
    global ruta_imagen
    global numEntradas
    numEntradas -= 1
    nombre = nombre.ljust(14)
    directorio = entradasLibres.pop(0)
    escribirAscii(directorio,'-')
    escribirAscii(directorio + 1,nombre)
    escribirEnteros(directorio + 16, tam)
    escribirEnteros(directorio + 20, ceil(cabezal/tamCluster))
    escribirAscii(directorio + 24,fechaCreacion)
    escribirAscii(directorio + 38,fechaModificacion)

def escribirInfo(cabezal,contenido):
    global ruta_imagen
    global numEntradas
    with open(ruta_imagen,'rb+') as FiUnamFs:
        FiUnamFs.seek(cabezal)
        FiUnamFs.write(contenido)
    guardarInformacionArchivos()

def eliminarDirectorio(cabezal):
    global numEntradas
    global entradasLibres
    entradasLibres.append(cabezal)
    entradasLibres.sort()
    numEntradas -= 1
    escribirAscii(cabezal,'/..............')
    escribirAscii(cabezal + 24,'0000000000000000000000000000')
    with open(ruta_imagen,'rb+') as FiUnamFs:
        FiUnamFs.seek(cabezal + 16)
        FiUnamFs.write(b'\x00' * 9)
        FiUnamFs.seek(cabezal + 52)
        FiUnamFs.write(b'\x00' * 12)

def eliminarInfo(cabezal,tam):
    with open(ruta_imagen,'rb+') as FiUnamFs:
        FiUnamFs.seek(cabezal)
        FiUnamFs.write(b'\x00' * tam)
        
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
    global numEntradas
    global archivos
    archivos.clear()
    numEntradas = 128
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
                archivo['clusterDirectorio'] = cabezal
                # Se guardar la información de los archivos que tienen información
                archivos[archivo['nombre'].rstrip()] = archivo
                cabezal += 64
                numEntradas -= 1
                pass
            else:
                # Se ignora y se avanza el cabezal
                entradasLibres.append(cabezal)
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
        if (os.path.exists(ruta) and ((os.path.exists(ruta + "/" + nombre) == False))):
            # Se copia el archivo, para lo cual se necesitan los datos
            contenido = leerInfo(archivos[nombre]['clusterInicial'] * tamCluster,archivos[nombre]['tam'])
            with open(ruta + "/" + nombre,'wb') as archivo:
                archivo.write(contenido)
            print("\n\tARCHIVO GUARDADO EXITOSAMENTE")
        else: 
            print("ERROR: La ruta especificada no existe o el archivo ya se encuentra en dicha ruta.")
    else:
        print("\tERROR: No existe un archivo con ese nombre")
    
def copiarArchivoAFiUnamFs():
    """
        Se tiene que considerar lo siguiente: 
        1. El directorio tenga entradas libres
        2. Que el nombre del archivo sea de 14 caracteres a lo mucho
        3. Que haya espacio disponible para el tamaño del archivo (el archivo no puede ser mayor a 716 * tamCluter)
    """
    # Primero se verifica que haya entradas disponibles en el directorio 
    if (len(archivos) == numEntradas): # No es posible agregar más archivos al directorio
        print("\tERROR: El directorio se encuentra saturado")
        return
    else:
        archivoSistema = input("Ingrese la ruta completa del archivo a copiar: ")
        # Se tiene que valir la ruta y la restricción de tamaño 
        if os.path.exists(archivoSistema):
            try:
                with open(archivoSistema,"rb") as file:
                    nombre = os.path.basename(archivoSistema)
                    if len(nombre) > 14:
                        print("\tERROR: El nombre del archivo es demasiado largo para el sistema.")
                        return
                    tam = os.path.getsize(archivoSistema)
                    if tam > (clusterTotales - numClusterDir) * tamCluster:
                        print("\tERROR: El tamaño del archivo es demasiado grande para el sistema.")
                        return
                    # Cumple las condiciones
                    fecha_modificacion = str(datetime.fromtimestamp(os.path.getmtime(archivoSistema)))[0:19].replace("-","").replace(" ","").replace(":","")
                    fecha_creacion = str(datetime.fromtimestamp(os.path.getctime(archivoSistema)))[0:19].replace("-","").replace(" ","").replace(":","")
                    # En este punto ya se tiene la información -> Se tiene que analizar si hay el suficiente espacio de asignación de memoria
                    clusterInicial = asignarEspacio(tam)
                    if clusterInicial == False: # No se encontró espacio de almacenamiento
                        print("\tERROR: No había el suficiente espacio de almacenamiento para el archivo seleccionado")
                        return
                    else:
                        # Se escribe el archivo 
                        contenido = file.read()
                        # Aquí se escribe en el espacio para archivos. También hay que actualizar el directorio
                        escribirDirectorio(nombre,tam,clusterInicial,fecha_modificacion,fecha_creacion)
                        escribirInfo(clusterInicial,contenido)
                        print("\tArchivo copiado de forma exitosas")
            except:
                print("\tERROR: No fue posible abrir el archivo (posiblemente no completó la ruta con el archivo)")
                return
        else:
            print("\n\tERROR: No fue posible encontrar la ruta")
            return

def asignarEspacio(tam):
    clusterNecesarios = ceil(tam/tamCluster)
    almacenamiento = []
    cluster = 5 # Se empieza por el cluster posterior al directorio
    for archivo in archivos.items():
        almacenamiento.append((archivo[1]['clusterInicial'],archivo[1]['clusterInicial'] + ceil(archivo[1]['tam'] / tamCluster)))
    almacenamiento.sort()
    while(cluster < 720):
        if len(almacenamiento) != 0 and cluster == almacenamiento[0][0]: # Si el cabezal se encuentra en un cluster ocupado, se lo salta
            cluster = almacenamiento[0][1] + 1
            almacenamiento.pop(0) # Se quita el cluster
        else:
            if len(almacenamiento) != 0 and (cluster + clusterNecesarios > almacenamiento[0][0]): # Choca con otro archivo
                cluster = almacenamiento[0][1] + 1
                almacenamiento.pop(0)
            else: # Es posible almacenar el archivo
                return cluster * tamCluster
        
        if len(almacenamiento) == 0 and (cluster + clusterNecesarios) < 720: # Es posible almacenar el archivo posterior a todos los demás
            return cluster * tamCluster
            
    return False
          
def eliminarArchivoFiUnamFs():
    print("Ingrese el nombre del archivo que desea eliminar:")
    nombre = input(" ").rstrip().lstrip()
    # Primero se debe validar que el nombre del archivo exista
    if nombre in archivos:
        # Se elimina el archivo
        informacion = archivos[nombre]
        eliminarDirectorio(informacion['clusterDirectorio'])
        eliminarInfo(informacion['clusterInicial'] * tamCluster,informacion['tam'])
    else: 
        print("\tERROR: No existe un archivo con ese nombre")
    print("\tArchivo eliminado exitosamente")
    guardarInformacionArchivos()


# INICIO
sesionActiva = True
guardarInformacionArchivos()
while(sesionActiva):
    mostrar_menu()
    opcion = input('\n\n\tSelecciona la opción deseada (cls - limpiar pantalla): ')
    if opcion == '1':
        listarContenidos()
    elif opcion == '2':
        copiarArchivoASistema()
        pass
    elif opcion == '3':
        copiarArchivoAFiUnamFs()
        pass
    elif opcion == '4':
        eliminarArchivoFiUnamFs()
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