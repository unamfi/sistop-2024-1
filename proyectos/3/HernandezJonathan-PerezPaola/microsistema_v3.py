# ¡Hola, hola! Oof.
# Bienvenido a la V3 del código. Esta versión presenta una serie de mejoras significativas, 
# como nuevas funciones para interactuar con el sistema de archivos 'fiunamfs.img', corrección 
# de varios errores (debido a su notoriedad) y optimización del código con comentarios adecuados.

# ¡Sin embargo! AÚN está en desarrollo y NO se considera completo.
# Se han añadido funciones para listar, copiar y eliminar archivos, además de mostrar información del sistema.
# Diferencias con versiones anteriores:
# - Incorporación de funciones nuevas.
# - Corrección de algunos errores y optimización del código.
# - Mayor funcionalidad y manejo de archivos en 'fiunamfs.img'.

# El código se basa en el manejo de archivos binarios para operar con el sistema de archivos 'fiunamfs.img'.

# Integrantes:
# Hernández Ortiz Jonathan.
# Pérez Avin Paola Celina de Jesús.

# Declaramos librerías a utilizar.
import os
import time
from struct import pack, unpack
import struct

# Función y librería para listar los archivos existentes en 'fiunamfs'.
def listar_archivos(sistema_archivos, cluster):
    # Se posiciona el fichero en el 'cluster'.
    sistema_archivos.seek(cluster)
    
    # Recorremos desde 1 hasta 'cluster' * 4 en pasos de 64.
    for i in range(1, cluster * 4, 64):
        # Se mueve el fichero a la posición 'cluster + i'.
        sistema_archivos.seek(cluster + i)
        # Guardamos en la variable 'archivo' los 15 bytes siguientes de 'fiunamfs' y los decodificamos en ASCII.
        archivo = sistema_archivos.read(15).decode("ascii")
        
        # Si los primeros 15 caracteres no son "...............".
        if archivo[:15] != "..............":
            # Si se cumple, obtenemos el tamaño del archivo.
            tamaño = struct.unpack('<' + 'I'*1, sistema_archivos.read(4))[0]
            
            # Si este tamaño es diferente de 0 (es decir, contiene información).
            if tamaño != 0:
                # Imprimimos el nombre, tamaño y el cluster inicial del archivo.
                print("\nArchivo:", archivo.strip(), "Tamaño:", struct.unpack('<' + 'I'*1, sistema_archivos.read(4))[0], 'Cluster inicial', struct.unpack('<' + 'I'*1, sistema_archivos.read(4))[0])

# Esta función realiza una copia a la carpeta del proyecto.
def copia_sistema(sistema_archivos, cluster):
    # Solicita el nombre del archivo que se desea copiar.
    archivo_copia = input("Nombre del Archivo a copiar: ")
    # Obtiene la información del archivo a través de la función buscar_archivo.
    datos = buscar_archivo(archivo_copia, sistema_archivos, cluster)
    tamano_archivo = datos[0]
    cluster_inicial = datos[1]
    
    # Verifica si el archivo no se encontró en 'fiunamfs'.
    if tamano_archivo == 0 and cluster_inicial == 0:
        print("\n¡El archivo no se encontró!")
    else:
        
        print("\nArchivo encontrado:", archivo_copia)
        print("Espacio que ocupa:", tamano_archivo, " Cluster inicial:", cluster_inicial)
        nuevo_archivo = open(archivo_copia, "wb")
        sistema_archivos.seek(cluster * cluster_inicial)
        nuevo_archivo.write(sistema_archivos.read(tamano_archivo))
        nuevo_archivo.close()
        print("\nArchivo copiado.")
        
# Esta función busca el archivo en 'fiunamfs' y retorna información como tamaño y cluster.
def buscar_archivo(copiar, sistema_archivos, cluster):
    # Se sitúa el puntero de 'fiunamfs' en el cluster.
    sistema_archivos.seek(cluster)
    
    for i in range(1, cluster * 4, 64):
        sistema_archivos.seek(cluster + i)
        archivo = sistema_archivos.read(15).decode("ascii")[:-1]
        if archivo.strip() == copiar.strip():
            tamano_archivo = int(struct.unpack('<' + 'I'*1, sistema_archivos.read(4))[0])
            cluster_inicial = int(struct.unpack('<' + 'I'*1, sistema_archivos.read(4))[0])
            return (tamano_archivo, cluster_inicial)
    return (0, 0)
    

# Calcula el siguiente cluster disponible para almacenar datos adicionales, considerando el tamaño actual del archivo.
def siguiente_cluster(cluster_inicial, tamano_archivo, cluster):
    # Calcula el espacio restante dentro del cluster actual.
    sobrante = tamano_archivo % cluster
    # Calcula la cantidad de bytes que se deben agregar para alcanzar el siguiente cluster.
    valor_a_aumentar = 1024 - sobrante
    # Retorna el siguiente cluster disponible para almacenar datos.
    return (cluster_inicial) * 1024 + tamano_archivo + valor_a_aumentar

# Encuentra el espacio disponible en el directorio para almacenar un nuevo archivo.
def espacio_en_directorio(sistema_archivos, cluster):
    sistema_archivos.seek(cluster)
    
    for i in range(0, cluster * 4, 64):
        sistema_archivos.seek(cluster + i)
        # Lee los siguientes 15 caracteres de 'fiunamfs' y los decodifica como ASCII.
        archivo = sistema_archivos.read(15).decode("ascii")
        
        # Comprueba si el espacio en el directorio está vacío ('..............').
        if archivo[:14] == "..............":
            return cluster + i
    return -1
    
# Encuentra un cluster disponible para almacenar un archivo de copia en 'fiunamfs'.
def Cluster_disponible(tamano_de_archivo_copia, sistema_archivos, cluster, tamano_sistema_archivos):
    # Se posiciona en el cluster.
    sistema_archivos.seek(cluster)
    datos = []
    # Recorre el espacio de clusters en 'fiunamfs'.
    for i in range(1, cluster * 4, 64):
        sistema_archivos.seek(cluster + i)
        # Lee los siguientes 15 caracteres de 'fiunamfs' y los decodifica como ASCII.
        archivo = sistema_archivos.read(15).decode("ascii").strip()[:-1]
        # Comprueba si el espacio en el cluster no está vacío ('..............').
        if archivo[:14] != "..............":
            # Obtiene el tamaño del archivo y el cluster inicial.
            tamano_archivo = int(struct.unpack('<' + 'I'*1, sistema_archivos.read(4))[0])
            cluster_inicial = int(struct.unpack('<' + 'I'*1, sistema_archivos.read(4))[0])
            datos.append((cluster_inicial, tamano_archivo))
    # Ordena los datos por el cluster inicial.
    datos = sorted(datos, key=lambda x: x[0])
    # Recorre los datos para encontrar el cluster disponible.
    for i in range(0, len(datos)):
        dir_cluster_siguiente = siguiente_cluster(datos[i][0], datos[i][1], cluster)
        if i == len(datos) - 1:
            espacio_libre = tamano_sistema_archivos - dir_cluster_siguiente
        else:
            dir_cluster_archivo_siguiente = datos[i + 1][0] * 1024
            espacio_libre = dir_cluster_archivo_siguiente - dir_cluster_siguiente
        # Verifica si el espacio libre es suficiente para el archivo de copia.
        if espacio_libre >= tamano_de_archivo_copia:
            return dir_cluster_siguiente
    return -1 # Retorna -1 si no hay cluster disponible para el archivo de copia.
    

# Realiza una copia de un archivo hacia 'fiunamfs'.
def copia_fiunamfs(sistema_archivos, tamano_sistema_archivos, cluster):
    # Solicita al usuario el nombre del archivo a copiar.
    archivo_copia = input("\nIngrese nombre del archivo: ")
    # Verifica si el nombre del archivo excede los 14 caracteres permitidos.
    if len(archivo_copia) > 14:
        print("\nEl nombre del archivo es demasiado largo.")
        return
    
    # Verifica si el archivo especificado existe en el sistema actual.
    if not os.path.isfile(archivo_copia):
        print("\nEl archivo no existe.")
        return
    # Obtiene la información del archivo a copiar en 'fiunamfs'.
    datos = buscar_archivo(archivo_copia, sistema_archivos, cluster)
    tamano_archivo = datos[0]
    cluster_inicial = datos[1]
    
    if (tamano_archivo == 0 and cluster_inicial == 0):
        # Obtiene el tamaño del archivo a copiar.
        tamano_archivo_copia = os.stat(archivo_copia).st_size
        print("\nEspacio del archivo", tamano_archivo_copia," caracteres.")
        
        # Busca espacio disponible en el directorio para el nuevo archivo.
        direccion = espacio_en_directorio(sistema_archivos, cluster)
        if direccion == -1:
            print("\nNo hay espacio en el directorio.")
            return
        
        # Encuentra un cluster disponible para almacenar el archivo de copia.
        dir_cluster_disponible = Cluster_disponible(tamano_archivo_copia, sistema_archivos, cluster, tamano_sistema_archivos)
        if dir_cluster_disponible == -1:
            print("\nNo hay espacio en el sistema de archivos.")
            return
        sistema_archivos.seek(direccion)
        sistema_archivos.write("                ".encode("ascii"))
        sistema_archivos.seek(direccion)
        sistema_archivos.write("".encode("ascii"))
        sistema_archivos.seek(direccion + 1)
        sistema_archivos.write("                ".encode("ascii"))
        sistema_archivos.seek(direccion + 1)
        sistema_archivos.write(archivo_copia.encode("ascii"))
        sistema_archivos.seek(direccion + 16)
        sistema_archivos.write("".encode("ascii"))
        str_tamano_archivo_copia = str(tamano_archivo_copia)
        numero_ceros = 9 - len(str_tamano_archivo_copia)
        sistema_archivos.seek(direccion + 16 + numero_ceros)
        sistema_archivos.write(struct.pack('<' + 'I'*1, int(str_tamano_archivo_copia)))
        sistema_archivos.seek(direccion + 20)
        sistema_archivos.write("".encode("ascii"))
        cluster_disponible = int(dir_cluster_disponible / 1024)
        str_cluster_disponible = str(cluster_disponible)
        numero_ceros = 6 - len(str_cluster_disponible)
        sistema_archivos.seek(direccion + 25 + numero_ceros)
        sistema_archivos.write(struct.pack('<' + 'I'*1, int(str_tamano_archivo_copia)))
        sistema_archivos.seek(direccion + 24)
        str_fecha = str(time.localtime().tm_year) + str(time.localtime().tm_mon).zfill(2) + str(time.localtime().tm_mday).zfill(2) + str(time.localtime().tm_hour).zfill(2) + str(time.localtime().tm_min).zfill(2) + str(time.localtime().tm_sec).zfill(2)
        str_fecha = str_fecha + ""
        sistema_archivos.write(str_fecha.encode("ascii"))
        sistema_archivos.seek(direccion + 38)
        sistema_archivos.write(str_fecha.encode("ascii"))
        contenido_archivo = open(archivo_copia, "r+b")
        sistema_archivos.seek(dir_cluster_disponible)
        
        for elemento in contenido_archivo:
            sistema_archivos.write(elemento)
        print("\nArchivo copiado")
    else:
        print("\nEl archivo ya existe.")
        

# Elimina un archivo de 'fiunamfs'.
def eliminar_archivo(sistema_archivos, cluster):
    # Solicita al usuario el nombre del archivo a eliminar.
    archivo_a_eliminar = input("Ingrese nombre del archivo a eliminar: ")
    # Posiciona el puntero en el inicio del 'cluster'.
    sistema_archivos.seek(cluster)
    
    # Recorre los clusters en 'fiunamfs'.
    for i in range(1, cluster * 4, 64):
        sistema_archivos.seek(cluster + i)
        # Lee los siguientes 15 caracteres de 'fiunamfs' y los decodifica como ASCII.
        archivo = sistema_archivos.read(15).decode("ascii")[:-1]
        print(archivo)
        
        # Comprueba si el nombre del archivo coincide con el nombre a eliminar.
        if archivo.strip() == archivo_a_eliminar.strip():
            # Se posiciona en el 'cluster' correspondiente y escribe caracteres vacíos para eliminar el archivo.
            sistema_archivos.seek(cluster + i)
            sistema_archivos.write("..............".encode("ascii"))
            print("\nArchivo eliminado.")
            return
    print("\nNo existe el archivo.")

# Definición de variables para el sistema de archivos 'fiunamfs'.
sector = 256
cluster = sector * 4
seleccion = ""

# Abre el archivo 'fiunamfs.img' en modo lectura y escritura binaria.
sistema_archivos = open("fiunamfs.img", "r+b")

# Imprime información sobre el sistema de archivos.
print("\nSISTEMA DE ARCHIVOS\n")

# Muestra información específica del sistema de archivos 'fiunamfs.img'.
sistema_archivos.seek(0)
print("Nombre:", sistema_archivos.read(9).decode("ascii"))
sistema_archivos.seek(10)
print("Versión de la implementación:", sistema_archivos.read(5).decode("ascii"))
sistema_archivos.seek(20)
print("Etiqueta del volumen:", sistema_archivos.read(19).decode("ascii"))
sistema_archivos.seek(40)
print("Tamaño del cluster en bytes:", struct.unpack('<' + 'I'*1, sistema_archivos.read(4))[0])
sistema_archivos.seek(45)
print("Número de clusters que mide el directorio:", struct.unpack('<' + 'I'*1, sistema_archivos.read(4))[0])
sistema_archivos.seek(51)
print("Número de clusters que mide la unidad completa:", struct.unpack('<' + 'I'*1, sistema_archivos.read(4))[0])

# Bucle principal para realizar operaciones en 'fiunamfs'.
while seleccion != "5":
    
    # Reabre el archivo 'fiunamfs.img' en modo lectura y escritura binaria.
    sistema_archivos = open("fiunamfs.img", "r+b")
    # Obtiene el tamaño del archivo 'fiunamfs.img'.
    tamano_sistema_archivos = os.stat("fiunamfs.img").st_size
    print("\n Opciones: \n")
    print("1. Listar contenido.")
    print("2. Copiar archivo de FiUnamFS hacia tu sistema.")
    print("3. Copiar archivo de tu sistema hacia FiUnamFS.")
    print("4. Eliminar archivo de FiUnamFS.")
    print("5. Salir.")
    
    # Solicita al usuario seleccionar una opción del menú.
    seleccion = input("\n\nIngresa una opción: ")
    if seleccion == "1":
        listar_archivos(sistema_archivos, cluster)
    elif seleccion == "2":
        copia_sistema(sistema_archivos, cluster)
    elif seleccion == "3":
        copia_fiunamfs(sistema_archivos, tamano_sistema_archivos, cluster)
    elif seleccion == "4":
        eliminar_archivo(sistema_archivos, cluster)
    
    # Cualquier comentario o sugerencia para seguir mejorando es bienvenido.
    # Cierra el archivo 'fiunamfs.img' después de completar la operación.
    sistema_archivos.close()