import os
import struct

# Abrir el archivo
nombre_sistemaArchivos="fiunamfs.img"
sistemaArchivos = open(nombre_sistemaArchivos, "r+b")

# Inicializamos las variables que representarán el tamaño de clusters,
# el número de ellos que mide el directorio
# y el número de clusters que mide la unidad completa
tamanoClusters = 0 
numeroClusters = 0
numeroClustersUnidad = 0

#Tamaño del directorio
tamanoDirectorio = 0

# Inicializamos estas variables también, después serán actualizadas dependiendo del sistema de archivos
id_sistemaArchivos = ""
version = ""
etiqueta = ""

# Lista de archivos del directorio
archivosDir = []

# Clase para representar un archivo del directorio
class archivo:
    def __init__(self, nombre, tamano, clusterInicial,): 
        self.nombre = nombre
        self.tamano = tamano
        self.clusterInicial = clusterInicial

# Estructura para la tabla de asignación de archivos
class TablaAsignacionArchivos:
    def __init__(self):
        self.tabla = {}

    def agregar_archivo(self, nombre_archivo, cluster_inicial, tamano):
        self.tabla[nombre_archivo] = {'cluster_inicial': cluster_inicial, 'tamano': tamano}

    def eliminar_archivo(self, nombre_archivo):
        if nombre_archivo in self.tabla:
            del self.tabla[nombre_archivo]

    def obtener_archivo(self, nombre_archivo):
        return self.tabla.get(nombre_archivo)

    def mostrar_tabla(self):
        for nombre, detalles in self.tabla.items():
            print(f"Archivo: {nombre}, Cluster Inicial: {detalles['cluster_inicial']}, Tamaño: {detalles['tamano']} bytes")

# Instancia de la tabla de asignación de archivos
tabla_asignacion = TablaAsignacionArchivos()

# Función para leer los datos del archivo enteros
def leerDatos(inicio,tamano):
    global sistemaArchivos
    sistemaArchivos.seek(inicio)
    return sistemaArchivos.read(tamano)

# Función para leer los datos ASCII del sistemaArchivos
def leerDatosASCII(inicio,tamano):
    global sistemaArchivos 
    sistemaArchivos.seek(inicio)
    datos = sistemaArchivos.read(tamano)
    return datos.decode("ascii")

# Para convertir los datos de ASCII
def datoUnpack(inicio, tamano):
    global sistemaArchivos
    sistemaArchivos.seek(inicio)
    dato = sistemaArchivos.read(tamano)
    return struct.unpack('<i', dato)[0]

# Para escribir datos al sistema de archivos
def datosPack(inicio, dato):
    global sistemaArchivos
    sistemaArchivos.seek(inicio)
    dato = struct.pack('<i', dato)
    return sistemaArchivos.write(dato)

# Función para leer los datos del archivo en ASCII
def leerDatosArchivo(posicion):
    inicio = 1024 + (posicion * 64)
    nombre = leerDatosASCII(inicio + 1, 14)
    if nombre.strip('.') != "":
        tamano = datoUnpack(inicio + 16, 4)
        clusterInicial = datoUnpack(inicio+20,4)
        return archivo(nombre, tamano, clusterInicial)
    return None

# Para escribir datos ASCII al sistema de archivos
def escribirDatosASCII(inicio, dato):
    global sistemaArchivos
    sistemaArchivos.seek(inicio)
    dato = dato.encode("ascii")  # Mantener "ascii"
    return sistemaArchivos.write(dato)

# Función para agregar un archivo al directorio
def agregarAlDirectorio(nuevoArchivo):
    global sistemaArchivos
    global tamanoClusters
    global tamanoDirectorio
    
    # Buscar una entrada libre en el directorio
    entradaLibre = -1
    for i in range(tamanoDirectorio // 64):
        sistemaArchivos.seek(1024 + i * 64)
        if sistemaArchivos.read(1) == b'\x00':
            entradaLibre = i
            break
    if entradaLibre == -1:
        print("No hay espacio en el directorio para agregar el archivo.")
        return False
    else:
        # Escribir los datos del nuevo archivo en la entrada libre
        inicio = 1024 + entradaLibre * 64
        escribirDatosASCII(inicio + 1, nuevoArchivo.nombre)
        datosPack(inicio + 16, nuevoArchivo.tamano)
        datosPack(inicio + 20, nuevoArchivo.clusterInicial)
        return True

# Función para enlistar los archivos del directorio
def listarDirectorio():
    global tamanoClusters
    global numeroClusters
    global tamanoDirectorio
    global archivosDir
    
    archivosDir = []
    
    print("\033[1m   Nombre\t\tTamaño   \033[0m")
    # Cuánto mide un cluster, cuántos clusters hay, y cuánto mide el directorio
    for i in range(int((tamanoClusters * numeroClusters) / tamanoDirectorio)):
        aux = leerDatosArchivo(i)
        if aux and aux.tamano != 0:
            print(f"   {aux.nombre}\t{aux.tamano} bytes")
            archivosDir.append(aux)

# Verificamos si el archivo existe en nuestro directorio
def verificarArchivo(nombreCopia):
    global archivosDir
    for i in archivosDir:
        if i.nombre.strip() == nombreCopia.strip():
            return archivosDir.index(i), True
    return -1,False

# Función para copiar un archivo del sistema de archivos a la computadora
def copiarArchivoSistema(nombreCopia, rutaNueva):
    # Verificamos si el archivo que se quiere copiar existe en nuestro directorio
    indexArchivo, validacion = verificarArchivo(nombreCopia)
    if not validacion:
        print("El archivo no existe")
        return

    # Archivo que se quiere copiar
    archivoC = archivosDir[indexArchivo]

    print(f"Tamaño del archivo a copiar: {archivoC.tamano}")

    # Crear el archivo en la ruta especificada
    if os.path.exists(rutaNueva):
        if os.path.isfile(os.path.join(rutaNueva, nombreCopia)):
            rutaArchivoDestino = os.path.join(rutaNueva, "copia de " + nombreCopia)
        else:
            rutaArchivoDestino = os.path.join(rutaNueva, nombreCopia)

        with open(rutaArchivoDestino, "wb") as destino:
            inicio_lectura = archivoC.clusterInicial * tamanoClusters
            sistemaArchivos.seek(inicio_lectura)
            datos_archivo = sistemaArchivos.read(archivoC.tamano)
            destino.write(datos_archivo)

        print("Archivo copiado con éxito")
    else:
        print("La ruta especificada no existe")

# Función para copiar un archivo de la computadora al sistema de archivos
def copiarArchivoComputadora(rutaArchivo):
    global tabla_asignacion
    global archivosDir
    global tamanoClusters
    global sistemaArchivos

    if not os.path.exists(rutaArchivo):
        print("El archivo no existe.")
        return

    # Obtener el nombre del archivo
    nombreArchivo = os.path.basename(rutaArchivo)
    
    #validar si el archivo ya existe en el sistema de archivos
    if verificarArchivo(nombreArchivo)[1]:
        print("El archivo ya existe en el sistema de archivos.")
        return

    # Obtener el tamaño del archivo
    tamanoArchivo = os.path.getsize(rutaArchivo)
    espacioDisponible = encontrarEspacioDisponible(tamanoArchivo)
    print(f"Espacio disponible: {espacioDisponible}")

    if espacioDisponible == -1:
        print("No hay suficiente espacio en el sistema de archivos para copiar el archivo.")
        return

    with open(rutaArchivo, "rb") as archivoComputadora:
        contenido = archivoComputadora.read()

        # Escribir en el espacio disponible encontrado
        inicio_escritura = espacioDisponible  # No multiplicar por tamanoClusters
        print("Inicio escritura: ", inicio_escritura)
        sistemaArchivos.seek(inicio_escritura)
        sistemaArchivos.write(contenido)

    nuevoArchivo = archivo(nombreArchivo, tamanoArchivo, espacioDisponible)
    print("Nombre del archivo: ", nuevoArchivo.nombre)
    archivosDir.append(nuevoArchivo)
    agregarAlDirectorio(nuevoArchivo)
    print("Archivo copiado con éxito al sistema de archivos")

def encontrarEspacioDisponible(tamanoArchivo):
    global archivosDir
    global tamanoClusters
    global numeroClusters
    global sistemaArchivos

    # Conjunto de todos los clusters ocupados por archivos existentes
    clustersOcupados = set()

    for archivo in archivosDir:
        # Calcula todos los clusters ocupados por el archivo actual
        clusters = [archivo.clusterInicial + i for i in range((archivo.tamano + tamanoClusters - 1) // tamanoClusters)]
        clustersOcupados.update(clusters)

    # Busca un espacio libre
    espacioLibre = -1
    i = 0
    while i < numeroClusters:
        if i not in clustersOcupados and i * tamanoClusters > 54:  # Excluye los primeros 54 bytes
            inicio = i * tamanoClusters
            sistemaArchivos.seek(inicio)
            # Verifica si el espacio libre encontrado es suficiente para el archivo que se va a escribir
            if (i + (tamanoArchivo + tamanoClusters - 1) // tamanoClusters) < numeroClusters:
                return i  # Devuelve el índice del espacio libre encontrado
        i += 1
    return -1  # Si no se encuentra ningún espacio libre, devuelve -1

def mostrarInfoCompleta():
    print("\nNombre del sistema de archivos: ", nombre_sistemaArchivos)
    print("Identificación del sistema de archivos: ", id_sistemaArchivos)
    print("Versión de la implementación: ", version)
    print("Etiqueta del volumen: ", etiqueta)
    print("Tamaño de un cluster: ", tamanoClusters)
    print("Número de clusters que mide el directorio: ", numeroClusters)
    print("Número de clusters que mide la unidad completa: ", numeroClustersUnidad)
    print("\n\n\n")

def datosEstaticos():
    global id_sistemaArchivos
    global version
    global etiqueta
    global tamanoClusters
    global numeroClusters
    global numeroClustersUnidad
    global tamanoDirectorio

    #Identificación del sistema de archivos por defecto
    id_sistemaArchivos = leerDatosASCII(0,8)

    #Versión de la implementación
    version = leerDatosASCII(10,4)

    #Etiqueta del volumen
    etiqueta = leerDatosASCII(20,19)

    #Tamaño de un cluster
    tamanoClusters = datoUnpack(40,4)

    #Número de clusters que mide el directorio
    numeroClusters = datoUnpack(45,4)

    #Número de clusters que mide la unidad completa
    numeroClustersUnidad = datoUnpack(50,4)

    #Tamaño del directorio por defecto
    tamanoDirectorio = 64

def borrarArchivo(nombreArchivo):
    global archivosDir
    global tamanoClusters
    global sistemaArchivos

    # Verificamos si el archivo que se quiere borrar existe en nuestro directorio
    indexArchivo, validacion = verificarArchivo(nombreArchivo)
    if validacion != True:
        print("El archivo no existe")
        return

    # Archivo que se quiere borrar
    archivoBorrar = archivosDir[indexArchivo]

    # Eliminamos el archivo del directorio
    archivosDir.pop(indexArchivo)

    # Marcar la entrada en el directorio como eliminada
    sistemaArchivos.seek(1024 + indexArchivo * 64)
    sistemaArchivos.write(b'\x00')

    # Marcamos los clusters correspondientes como libres
    sistemaArchivos.seek(archivoBorrar.clusterInicial * tamanoClusters)
    sistemaArchivos.write(b'\x00' * archivoBorrar.tamano)

    # Recargar la lista de archivos del directorio
    archivosDir = []
    listarDirectorio()

    print("Archivo eliminado con éxito")

def desfragmentarSistema():
    global archivosDir
    global tamanoClusters
    global sistemaArchivos

    # Ordenamos los archivos por su cluster inicial
    archivosDir.sort(key=lambda x: x.clusterInicial)

    # Recorremos todos los archivos
    for i in range(len(archivosDir) - 1):
        # Si el archivo actual y el siguiente no están contiguos
        if archivosDir[i].clusterInicial + (archivosDir[i].tamano + tamanoClusters - 1) // tamanoClusters < archivosDir[i + 1].clusterInicial:
            # Movemos el archivo siguiente para que esté contiguo al archivo actual
            inicio_lectura = archivosDir[i + 1].clusterInicial * tamanoClusters
            sistemaArchivos.seek(inicio_lectura)
            datos_archivo = sistemaArchivos.read(archivosDir[i + 1].tamano)
            inicio_escritura = (archivosDir[i].clusterInicial + (archivosDir[i].tamano + tamanoClusters - 1) // tamanoClusters) * tamanoClusters
            sistemaArchivos.seek(inicio_escritura)
            sistemaArchivos.write(datos_archivo)
            # Actualizamos el cluster inicial del archivo que movimos
            archivosDir[i + 1].clusterInicial = inicio_escritura // tamanoClusters

    # Recargar la lista de archivos del directorio
    archivosDir = []
    listarDirectorio()

    print("Sistema de archivos desfragmentado con éxito")

def menu():
    while True:
        print("1. Listar el contenido del directorio")
        print("2. Copiar archivo del sistema a la computadora")
        print("3. Copiar archivo de la computadora al sistema")
        print("4. Borrar archivo del sistema")
        print("5. Desfragmentar el sistema")
        print("6. Salir")
        opcion = int(input("Ingresa una opción: "))
        if opcion == 1:
            listarDirectorio()
        elif opcion == 2:
            nombreCopia = input("Ingresa el nombre del archivo que deseas copiar (incluye la extensión): ")
            #Si se desea copiar a la ruta en donde se encuentra este archivo:
            rutaCopiar = os.path.dirname(os.path.abspath(__file__))

            #Si se desea copiar a una ruta específica:
            #rutaCopiar = input("Ingresa la ruta donde deseas copiar el archivo: ").replace("\\","/")
            copiarArchivoSistema(nombreCopia, rutaCopiar)
        elif opcion == 3:
            copiarArchivoComputadora(input("Ingresa la ruta de donde deseas copiar el archivo (incluye el archivo con su extensión): ").replace("\\","/"))
        elif opcion == 4:
            nombreArchivo = input("Ingresa el nombre del archivo que deseas borrar (incluye la extensión): ")
            borrarArchivo(nombreArchivo)
        elif opcion == 5:
            desfragmentarSistema()
        elif opcion == 6:
            break
        else:
            print("Opción inválida")

def main():
    datosEstaticos()
    mostrarInfoCompleta()
    menu()
    
main()
