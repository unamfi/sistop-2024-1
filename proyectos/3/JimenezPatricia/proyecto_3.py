
import struct
import os
import time
import datetime
import math

iden =  input("Ingresa el nombre del archivo de imagen: ")
archivos, mapa = [], []
imagen = open(iden, "br+")
#Esta función es como un lector de datos. Le dices desde dónde quieres leer (inicio) y 
#cuántos bytes necesitas (tamanio), y ella te pasa esos bytes. Simple, ¿no?
def Datos(inicio, tamanio):
    global imagen
    imagen.seek(inicio)
    return imagen.read(tamanio)
# Le das un punto de inicio y cuántas letras quieres, y ella te devuelve el texto en 
#formato legible.
def DAscii(inicio, tamanio):
    global imagen
    imagen.seek(inicio)
    return imagen.read(tamanio).decode("ascii")
#Aquí, se está desempaquetando datos. Le indicas desde dónde quieres desempaquetar y cuántos bytes tomar,
# y ella te da un número listo para usar.
def datoUnpack(inicio, tamanio):
    global imagen
    imagen.seek(inicio)
    return struct.unpack('<i', imagen.read(tamanio))[0]
#Le das una posición y una cadena de texto, y ella escribe esa cadena en el archivo 
#desde esa posición.
def inputAscii(inicio, dato):
    global imagen
    imagen.seek(inicio)
    return imagen.write(dato.encode("ascii"))
#Inversamente, esta función empaqueta un dato (número) y lo coloca en una
# posición específica del archivo.
def meteDatoPack(inicio, dato):
    global imagen
    imagen.seek(inicio)
    return imagen.write(struct.pack('<i', dato))

tamanioCluster, clustersDirectorio, clustersUnidad, tamanioDirectorio = datoUnpack(40, 4), datoUnpack(45, 4), datoUnpack(50, 4), 64

class archivo:
    global tamanioCluster

    def __init__(self, nombre, tamanio, clusterInicial, fechaCreacion, fechaModificacion):
        self.nombre, self.tamanio, self.clusterInicial, self.fechaCreacion, self.fechaModificacion = nombre.replace(" ", ""), tamanio, clusterInicial, fechaCreacion, fechaModificacion
        self.numClusters = math.ceil(tamanio / tamanioCluster)
#Le dices cuál archivo quieres, y te da los detalles: nombre, tamaño, etc.
def DatosArchivo(posicion):
    inicial = 1024 + (posicion * 64)
    if DAscii(inicial + 1, 14) != "--------------":
        nombre = DAscii(inicial + 1, 14)
        tamanio = datoUnpack(inicial + 16, 4)
        clusterInicial = datoUnpack(inicial + 20, 4)
        fechaCreacion, fechaModificacion = DAscii(inicial + 24, 14), DAscii(inicial + 38, 14)
        return archivo(nombre, tamanio, clusterInicial, fechaCreacion, fechaModificacion)
#Inicia el "mapa" que mantiene registro de qué clusters están ocupados y cuáles no
def iniciaMapa():
    global mapa
    mapa = [1] * 5 + [0] * (720 - 5)
#Actualiza el mapa basándose en la información actual de los archivos. Es como revisar
# y marcar asientos ocupados.
def actualizaMapa():
    global mapa, archivos
    mapa = [0] * 720
    mapa[:5] = [1] * 5
    for archivoActual in archivos:
        for j in range(archivoActual.numClusters):
            mapa[archivoActual.clusterInicial + j] = 1
#Lee la información del sistema de archivos y configura la lista de archivos. 
def inicializaArchivos():
    global archivos
    numArchivos = int((tamanioCluster * clustersDirectorio) / tamanioDirectorio)
    archivos = [DatosArchivo(x) for x in range(numArchivos) if DatosArchivo(x) is not None]
    actualizaMapa()
#Le dices un nombre de archivo y te dice dónde encontrarlo en la lista.
def buscaArchivoNombre(nombre):
    global archivos
    return next((archivos.index(x) for x in archivos if x.nombre == nombre), -1)

def buscaArchivoClusterInicial(clusterInicial):
    global archivos
    return next((archivos.index(x) for x in archivos if x.clusterInicial == clusterInicial), -1)

def muestraDirectorio():
    global archivos
    for x in archivos:
        print(f"{x.nombre}        {x.tamanio} bytes")
#Trae un archivo de tu computadora y lo coloca en el sistema de archivos.
# Como poner un nuevo libro en tu estantería.
def copiaArchivoAComputadora(nombreArchivo, ruta):
    global archivos
    desfragmentar()
    posicion = buscaArchivoNombre(nombreArchivo)
    if posicion != -1:
        auxiliar = Datos(archivos[posicion].clusterInicial * 1024, archivos[posicion].tamanio)
        if os.path.exists(ruta) and not os.path.exists(os.path.join(ruta, nombreArchivo)):
            print("Archivo copiado exitosamente.")
            with open(os.path.join(ruta, nombreArchivo), "bw") as ArchivoNuevo:
                ArchivoNuevo.write(auxiliar)
        else:
            print("No se pudo copiar el archivo")
    else:
        print("No se pudo copiar el archivo")

def borraEnDirectorio(posicion):
    global imagen
    inicial = 1024 + (posicion * 64)
    imagen.seek(inicial)
    imagen.write(b'---------------' + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00' + b'0000000000000000000000000000' + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')


def borraEnDirectorio2(posicion):
    global imagen
    inicial = 1024 + (posicion * 64)
    imagen.seek(inicial)
    imagen.write(b'-              ' + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00' + b'0000000000000000000000000000' + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

def borraArchivo(nombreArchivo, aux):
    global archivos
    for x in archivos:
        if x.nombre == nombreArchivo:
            archivos.pop(archivos.index(x))
            actualizaMapa()
            for y in range(64):
                inicial = 1024 + (y * 64)
                nombre = DAscii(inicial + 1, 14).replace(" ", "")
                print(nombre)
                if nombre == nombreArchivo:
                    borraEnDirectorio(y)
                    return
                elif aux == 2:
                    return
    print("El archivo para borrar no existe")
    return

#
def copiaArchivoAImagen(rutaOrigen):
    global archivos
    desfragmentar()
    if os.path.exists(rutaOrigen) and len(os.path.split(rutaOrigen)[-1].replace(" ", "")) < 15 and os.stat(rutaOrigen).st_size < 732160:
        if buscaArchivoNombre(os.path.split(rutaOrigen)[-1].replace(" ", "")) == -1:
            nombre = agregaEspacios(os.path.split(rutaOrigen)[-1])
            tamanio = os.stat(rutaOrigen).st_size
            clusterInicial = asignaCluster(tamanio)
            if clusterInicial == -1:
                print("Sin espacio")
                return
            fechaCreacion = datetime.datetime.strptime(time.ctime(os.stat(rutaOrigen).st_ctime), "%a %b %d %H:%M:%S %Y").strftime("%Y%m%d%H%M%S")
            fechaModificacion = datetime.datetime.strptime(time.ctime(os.stat(rutaOrigen).st_mtime), "%a %b %d %H:%M:%S %Y").strftime("%Y%m%d%H%M%S")
            archivoAux = archivo(nombre, tamanio, clusterInicial, fechaCreacion, fechaModificacion)
            archivos.append(archivoAux)
            if agregaADirectorio(archivoAux) == -1:
                return
            agregaArchivoAImagen(rutaOrigen, archivoAux)
            actualizaMapa()
        else:
            print("Ya existe un archivo con el mismo nombre. Por favor inténtelo nuevamente.")

def agregaArchivoAImagen(rutaOrigen, archivoAux):
    global imagen
    Auxfile = open(rutaOrigen, "br")
    contenido = Auxfile.read()
    Auxfile.close()

    inicio = archivoAux.clusterInicial * tamanioCluster
    imagen.seek(inicio)
    imagen.write(contenido)

def agregaADirectorio(archivoAux):
    for y in range(64):
        inicial = 1024 + (y * 64)
        if DAscii(inicial + 1, 14) == "--------------":
            borraEnDirectorio2(y)
            inputAscii(inicial, "-")
            inputAscii(inicial + 1, archivoAux.nombre)
            inputDato(inicial + 16, archivoAux.tamanio)
            inputDato(inicial + 20, archivoAux.clusterInicial)
            inputAscii(inicial + 24, archivoAux.fechaCreacion)
            inputAscii(inicial + 38, archivoAux.fechaModificacion)
            return 1
    print("Ya no hay espacio en el directorio")
    borraArchivo(archivoAux.nombre, 2)
    return -1

def asignaCluster(tam):
    global mapa
    try:
        clusterInicialPosible = mapa.index(0)
    except ValueError:
        print("Ya no hay espacio en el dispositivo para almacenar")
        return -1
    clustersDeArchivo = math.ceil(tam / tamanioCluster)
    if clusterInicialPosible + clustersDeArchivo < 720:
        return clusterInicialPosible
    else:
        return -1

def agregaEspacios(nombre):
    while len(nombre) != 14:
        nombre = nombre + " "
    return nombre

def desfragmentar():
    global archivos, imagen, mapa
    espacioLibre = 0
    posicionMapa = -1
    for x in mapa:
        posicionMapa += 1
        if x == 0:
            espacioLibre += 1
        elif x == 1 and espacioLibre != 0:
            moverArchivoEnImagen(posicionMapa, espacioLibre)
            actualizarArchivos(posicionMapa, espacioLibre)
            actualizarDirectorio()
            espacioLibre = 0

# Resto del código sigue igual...

def inicio():
    iniciaMapa()
    inicializaArchivos()
    print("Datos del sistema de archivos:")
    nombreSistema, version, etiqueta =DAscii(0, 8), DAscii(10, 4), DAscii(20, 5)
    print(f"{nombreSistema} {version} {etiqueta}\n")

    menu1 = True
    while menu1:
        print("\n---------Opciones:\n1.-Listar \n2.-Copiar un archivo a la computadora\n3.-Copiar un archivo de tu computadora hacia FiUnamFS\n4.-Eliminar un archivo del FiUnamFS\n5. Cerrar\n")
        opcion = input("")
        if opcion == "1":
            muestraDirectorio()
        elif opcion == "2":
            nombre = input("Nombre del archivo a copiar: ")
            ruta = input("Dame la ruta donde sera copiada: ").replace("\\", "/")
            copiaArchivoAComputadora(nombre, ruta)
        elif opcion == "3":
            ruta = input("Dame  la ruta del archivo:").replace("\\", "/")
            copiaArchivoAImagen(ruta)
        elif opcion == "4":
            nombre = input("que archivo quieres eliminar: ")
            borraArchivo(nombre, 1)
        elif opcion == "5" or opcion == "cls":
            menu1 = False
        else:
            print("No ingresaste una opción válida. Por favor inténtalo nuevamente.\n\n")

inicio()
imagen.close()