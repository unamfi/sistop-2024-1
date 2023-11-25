# Proyecto 3 | Sistemas Operativos | FI UNAM.

# ¡Bienvenido a la V5, la versión final de este código!
# Este código representa la culminación de mejoras significativas y funcionalidades implementadas.

# * Descripción general del código:
# * Este programa es un gestor de archivos que interactúa con el sistema 'FIUNAMFS'.
# * Su funcionalidad incluye:
# - Listar contenido del sistema de archivos.
# - Copiar archivos desde 'FIUNAMFS' a la computadora y viceversa.
# - Eliminar archivos del sistema 'FIUNAMFS'.
# - Verificar información general del sistema de archivos.

# * A lo largo de esta versión:
# - Se han corregido errores.
# - Optimizado el código.
# - Se han agregado nuevas funciones.

# Integrantes:
# Hernández Ortiz Jonathan.
# Pérez Avin Paola Celina de Jesús.

# Se importan las bibliotecas a utilizar.
import os
import time
from struct import pack, unpack
import struct
import shutil
opcion = 0

# Función que maneja el menú del programa.
def menu():
    global opcion
    # Se ejecuta un ciclo continuo hasta que el usuario ingrese '5' para salir del programa.
    while opcion != 5:
        # Se abre el archivo 'fiunamfs' para su manipulación.
        sistema_archivos = open("fiunamfs.img", "r+b")
        # Leemos el peso del archivo 'fiunamfs'.
        tamano_sistema_archivos = os.stat("fiunamfs.img").st_size
        # Menú que presenta diversas opciones al usuario.
        print("\n Opciones: \n")
        print("---1. Listar de contenido de FIUNAMFS---")
        print("---2. Copiar archivo de FIUNAMFS a PC---")
        print("---3. Copiar archivo de PC a FIUNAMFS---")
        print("---4. Eliminar archivo de FiUnamFS------")
        print("---5. Salir del Programa----------------")
        # Solicitamos al usuario que ingrese una opción para continuar.
        opcion = int(input("\n\n---|Ingresa una opción: "))
        # Si el usuario ingresa '1', se procede a listar los archivos disponibles.
        if opcion == 1:
            listar_archivos(sistema_archivos, cluster)
        # Realizamos la copia de un archivo desde 'fiunamfs' a la computadora.
        elif opcion == 2:
            copia_sistema(sistema_archivos, cluster)
        # Copiamos un archivo desde la computadora a 'fiunamfs'.
        elif opcion == 3:
            copia_fiunamfs(sistema_archivos, tamano_sistema_archivos, cluster)
        # Eliminamos un archivo de 'fiunamfs'.
        elif opcion == 4:
            eliminar_archivo(sistema_archivos, cluster)
        # Cerramos 'fiunamfs' para guardar los cambios realizados.
        sistema_archivos.close()

# Función que lee información del archivo 'fiunamfs'.
def leer_info_sistema_archivos(sistema_archivos, offset, longitud):
    # Indica la posición actual del puntero en el archivo.
    sistema_archivos.seek(offset)
    # Lectura de información desde el archivo 'fiunamfs'.
    # Básicamente, lo que se lee del 'fiunamfs'.
    return sistema_archivos.read(longitud).decode("ascii")

# Devuelve el valor calculado de los clusters iniciales de los archivos.
def leer_entero(sistema_archivos, offset, formato='<I'):
    # Indicamos la ubicación actual del puntero en el código.
    sistema_archivos.seek(offset)
    # Retorna el peso calculado a partir de la lectura de 4 bytes.
    return struct.unpack(formato, sistema_archivos.read(struct.calcsize(formato)))[0]


# Con esta librería mandaremos a enlistar los archivos existentes en FIUNAMFS.
def listar_archivos(sistema_archivos, cluster):
    # Mueve el puntero del archivo a la posición del cluster especificado.
    sistema_archivos.seek(cluster)
    # Iteramos desde 1 hasta el valor de 'cluster' multiplicado por 4 en incrementos de 64.
    for i in range(1, cluster * 4, 64):
        # Se mueve el fichero a la posición 'cluster + i'.
        sistema_archivos.seek(cluster + i)
        # Añadimos al archivo la lectura de los próximos 15 caracteres del archivo 'fiunamfs' y los decodificamos a ASCII.
        archivo = sistema_archivos.read(15).decode("ascii")
        # Si los siguientes 15 valores en 'archivos' son distintos de "...............".
        if archivo[:14] != "..............":
            # Si se cumple la condición, asignamos el peso del archivo a la variable 'Peso'.
            Peso = struct.unpack('<' + 'I'*1, sistema_archivos.read(4))[0]
            # Si el valor es diferente de 0, indica que el archivo contiene información.
            if Peso != 0 :
                # En caso de contener información, se imprime el nombre del archivo, su peso y el cluster inicial.
                print("\nArchivo:", archivo.strip().replace("-", ""), "Peso:", struct.unpack('<' + 'I'*1, sistema_archivos.read(4))[0], 'Cluster inicial:', struct.unpack('<' + 'I'*1, sistema_archivos.read(4))[0])
                
                
# Esta función realiza una copia del archivo a nuestra carpeta de proyecto actual.
def copia_sistema(sistema_archivos, cluster):
    # Solicitamos al usuario el nombre del archivo que desea copiar.
    archivo_copia = input("---|Nombre del Archivo a copiar: ")
    # Asignamos a 'datos' el resultado obtenido de la función 'buscar_archivo'.
    datos = buscar_archivo(archivo_copia, sistema_archivos, cluster)
    # Obtenemos el peso del archivo desde la función 'buscar'.
    tamano_archivo = datos[0]
    # Obtenemos el cluster del archivo desde la función 'buscar_archivo'.
    cluster_inicial = datos[1]
    
    # Si ambos valores son 0, significa que el archivo no existe.
    if tamano_archivo == 0 and cluster_inicial == 0:
        print("\nNo se encontro ningun archivo o esta vacio.")
    else:
        # Si se encuentra el archivo, se envía información.
        print("\nArchivo encontrado:", archivo_copia)
        # ¡Importante! Agregamos la funcionalidad de desfragmentación.
        # Imprimimos el peso y el cluster obtenidos en la función 'buscar_archivo'.
        print("Espacio que ocupa:", tamano_archivo, " Cluster inicial:", cluster_inicial)
        # Abrimos un nuevo archivo llamado 'archivo_copia' en modo lectura.
        nuevo_archivo = open(archivo_copia, "wb")
        # Movemos el puntero a la posición correspondiente al archivo a copiar en el cluster inicial.
        sistema_archivos.seek(cluster * cluster_inicial)
        # Mandamos esos datos a 'nuevo_archivo' con la información de 'fiunamfs'.
        # Transferimos la información del archivo al nuevo archivo que estamos generando.
        nuevo_archivo.write(archivo_copia.read(tamano_archivo).decode("ascii"))
        # Y cerramos el archivo.
        nuevo_archivo.close()
        print("\nArchivo copiado.")
        
        
# Esta función busca el archivo en 'fiunamfs' y devuelve información como peso y cluster.
def buscar_archivo(copiar, sistema_archivos, cluster):
    # Movemos el puntero en 'fiunamfs' a la posición del cluster especificado.
    sistema_archivos.seek(cluster)
    # Iremos desde 1 hasta el valor de 'cluster' multiplicado por 4 en incrementos de 64.
    for i in range(1, cluster * 4, 64):
        # Posicionamos el puntero en 'cluster + i'.
        sistema_archivos.seek(cluster + i)
        # La variable 'archivo' obtiene la lectura de los siguientes 15 caracteres y los decodifica a ASCII.
        archivo = sistema_archivos.read(15).decode("ascii")[:-1]
        # ¡Si las copias son idénticas, significa que el archivo existe!
        if archivo.strip().replace("-", "") == copiar.strip():
            # Calculamos el peso a partir de los primeros 4 bytes en 'fiunamfs' y lo convertimos a entero.
            tamano_archivo = int(struct.unpack('<' + 'I'*1, sistema_archivos.read(4))[0])
            # Calculamos el cluster a partir de los primeros 4 bytes en 'fiunamfs' y lo convertimos a entero.
            cluster_inicial = int(struct.unpack('<' + 'I'*1, sistema_archivos.read(4))[0])
            # Retornamos el peso y el cluster inicial del archivo que existe en 'fiunamfs'.
            return (tamano_archivo, cluster_inicial)
    # Si el archivo a copiar o el archivo en 'fiunamfs' no existe, devuelve valores de 0.
    return (0, 0)

# Función para copiar un archivo desde nuestra computadora a 'fiunamfs'.
def copia_fiunamfs(sistema_archivos, tamano_sistema_archivos, cluster):
    # Solicitamos al usuario el archivo que desea copiar.
    archivo_copia = input("\n---|Ingrese nombre del archivo: ")
    # Si el peso del archivo es mayor a 14 (que es el peso máximo de los nombres de archivos).
    if len(archivo_copia) > 14:
        # Se informa al usuario que el nombre del archivo es demasiado grande.
        print("\n¡Oops, nombre muy largo! :(")
        # ¡Retornamos!
        return
    # Si el archivo a copiar no existe en la PC.
    if not os.path.isfile(archivo_copia):
        # Se indica que el archivo no existe.
        print("\nArchivo no encontrado. :(")
        return
    # Se asigna a 'datos' el resultado de la búsqueda del archivo.
    datos = buscar_archivo(archivo_copia, sistema_archivos, cluster)
    # Cálculo del peso obtenido en la función 'buscar_archivo'.
    tamano_archivo = datos[0]
    # Cálculo del peso obtenido en la función 'buscar_archivo'.
    cluster_inicial = datos[1]
    # Si 'datos' contiene valores de 0, significa que el archivo no existe o está vacío.
    if (tamano_archivo == 0 and cluster_inicial == 0):
        # Calculamos el peso total de 'archivo_copia'.
        tamano_archivo_copia = os.stat(archivo_copia).st_size
        # Imprimimos información del archivo a copiar.
        print("\nTamaño: ", tamano_archivo_copia," caracteres.")
        # Asignamos a 'direccion' el resultado obtenido de la función 'espacio_dir'.
        direccion = espacio_dir(sistema_archivos, cluster)
        # Si la función 'espacio_dir'...
        if direccion == -1:
            # No hay suficiente espacio disponible para copiar a 'fiunamfs'.
            print("\n¡Espacio insuficiente para FIUNAMFS! :(")
            # ¡Retornamos!
            return
        # Asignamos a 'cluster_disponible' el resultado obtenido de la función 'Cluster_disponible'.
        cluster_disponible = Cluster_disponible(tamano_archivo_copia, sistema_archivos, cluster, tamano_sistema_archivos)
        # Si no se encontró espacio, es decir, se retornó 0.
        if cluster_disponible == -1:
            # Mandamos a decir que no hay espacio en el sistema de archivos.
            print("\nNo hay espacio en el sistema de archivos.")
            # Retornamos.
            return
        # Posiciona el puntero en el archivo en la posición especificada por 'direccion'.
        sistema_archivos.seek(direccion)
        # Lee los primeros 5 caracteres del archivo a partir de la posición actual y los almacena en 'texto'.
        texto = str(sistema_archivos.read(5))
        # Reemplaza todas las barras inclinadas ("/") en la cadena 'texto', pero no guarda el resultado.
        texto.replace("/", "")
        # Reposiciona el puntero al inicio de la dirección especificada en el archivo.
        sistema_archivos.seek(direccion)
        # Escribe una cadena de 16 espacios en blanco en el archivo.
        # Sin embargo, esto podría no hacer lo que se espera, ya que se está escribiendo en la posición actual del puntero.
        sistema_archivos.write("                ".encode("ascii"))
        # Reposiciona el puntero al inicio de la dirección especificada en el archivo.
        sistema_archivos.seek(direccion)
        # Escribe un guion ("-") en el archivo en la posición especificada por 'direccion'.
        # Nuevamente, esto podría no funcionar como se espera si la posición no es un múltiplo de 16.
        sistema_archivos.write("-".encode("ascii"))
        # Mueve el puntero a la posición 'direccion + 1' y escribe una cadena de 15 espacios en blanco.
        sistema_archivos.seek(direccion + 1)
        sistema_archivos.write("               ".encode("ascii"))
        # Mueve el puntero a la posición 'direccion + 1'.
        sistema_archivos.seek(direccion+1)
        # Escribe el nombre del archivo de copia en el sistema de archivos.
        sistema_archivos.write(archivo_copia.encode("ascii"))
        # Mueve el puntero a la posición 'direccion + 16'.
        sistema_archivos.seek(direccion + 16)
        # Escribe una cadena vacía.
        sistema_archivos.write("".encode("ascii"))
        # Convierte el tamaño del archivo de copia a una cadena.
        str_tamano_archivo_copia = str(tamano_archivo_copia)
        # Calcula el número de ceros necesarios.
        numero_ceros = 9 - len(str_tamano_archivo_copia)
        # Mueve el puntero a la posición 'direccion + 16 + numero_ceros'.
        sistema_archivos.seek(direccion + 16 + numero_ceros)
        # Escribe el tamaño del archivo de copia.
        sistema_archivos.write(struct.pack('<' + 'I'*1, int(str_tamano_archivo_copia)))
        # Mueve el puntero a la posición 'direccion + 20' y escribe una cadena vacía.
        sistema_archivos.seek(direccion + 20)
        # Escribe una cadena vacía.
        sistema_archivos.write("".encode("ascii"))
        # Convierte el tamaño del clúster disponible y escribe en el sistema de archivos.
        cluster_disponible = int(cluster_disponible / 1024)
        # Convierte el tamaño del cluster disponible a una cadena de caracteres.
        str_cluster_disponible = str(cluster_disponible)
        # Calcula el número de ceros necesarios para que la cadena tenga una longitud de 6 caracteres.
        numero_ceros = 6 - len(str_cluster_disponible)
        # Mueve el puntero a la posición 'direccion + 25 + numero_ceros' en el archivo.
        sistema_archivos.seek(direccion + 25 + numero_ceros)
        # Este desplazamiento sugiere que se está escribiendo información relacionada con el clúster disponible en el sistema de archivos.
        sistema_archivos.write(struct.pack('<' + 'I'*1, int(str_cluster_disponible)))
        # Mueve el puntero a la posición 'direccion + 23'.
        sistema_archivos.seek(direccion + 23)
        # Escribe la fecha actual en el sistema de archivos.
        str_fecha = str(time.localtime().tm_year) + str(time.localtime().tm_mon).zfill(2) + str(time.localtime().tm_mday).zfill(2) + str(time.localtime().tm_hour).zfill(2) + str(time.localtime().tm_min).zfill(2) + str(time.localtime().tm_sec).zfill(2)
        str_fecha = str_fecha + ""
        sistema_archivos.write(str_fecha.encode("ascii"))
        # Mueve el puntero a la posición 'direccion + 38'.
        sistema_archivos.seek(direccion + 38)
        # Escribe la fecha actual en el sistema de archivos.
        sistema_archivos.write(str_fecha.encode("ascii"))
        # Abre el archivo de copia en modo lectura y escritura binaria.
        contenido_archivo = open(archivo_copia, "r+b")
        # Mueve el puntero a la posición del clúster disponible.
        sistema_archivos.seek(cluster_disponible)
        # Escribe el contenido del archivo de copia en el sistema de archivos.
        for elemento in contenido_archivo:
            sistema_archivos.write(elemento)
        # Imprime un mensaje indicando que el archivo ha sido copiado.
        print("\nArchivo copiado.")
    else:
        # Mandamos a imprimir que ya existe un archivo en 'fiunamfs' con ese nombre.
        print("\nEl archivo ya existe.")
        
        
# Función que verifica la existencia de espacio para agregar información a 'fiunamfs'.
def Cluster_disponible(tamano_de_archivo_copia, sistema_archivos, cluster, tamano_sistema_archivos):
    # Establece el puntero al inicio del cluster en el sistema de archivos.
    sistema_archivos.seek(cluster)
    # Inicializa una lista para almacenar datos sobre archivos existentes.
    datos = []
    # Itera sobre los clusters en incrementos de 64 bytes.
    for i in range(1, cluster * 4, 64):
        # Mueve el puntero al inicio del cluster actual.
        sistema_archivos.seek(cluster + i)
        # Lee el nombre del archivo del cluster y lo decodifica como ASCII.
        archivo = sistema_archivos.read(15).decode("ascii").strip()[:-1]
        archivo = archivo.strip().replace("-", "")
        # Verifica si el nombre del archivo no es igual a una cadena de puntos, que indica un cluster no utilizado.
        if archivo[:14] != "..............":
            # Lee el Peso y el cluster inicial del archivo actual.
            tamano_archivo = int(struct.unpack('<' + 'I'*1, sistema_archivos.read(4))[0])
            cluster_inicial = int(struct.unpack('<' + 'I'*1, sistema_archivos.read(4))[0])
            # Almacena los datos en la lista como una tupla.
            datos.append((cluster_inicial, tamano_archivo))
    # Ordena la lista de datos por el cluster inicial.
    datos = sorted(datos, key=lambda x: x[0])
    # Itera sobre los datos para encontrar un espacio libre.
    for i in range(0, len(datos)):
        dir_cluster_siguiente = siguiente_cluster(datos[i][0], datos[i][1], cluster)
        # Calcula el espacio libre entre el cluster actual y el siguiente.
        if i == len(datos) - 1:
            # Si se cumple, calcula el espacio libre.
            espacio_libre = tamano_sistema_archivos - dir_cluster_siguiente
        else:
            # Calcula el espacio siguiente.
            dir_cluster_archivo_siguiente = datos[i + 1][0] * 1024
            # Encuentra el espacio libre.
            espacio_libre = dir_cluster_archivo_siguiente - dir_cluster_siguiente
        # Comprueba si el espacio libre es suficiente para la copia del archivo.
        if espacio_libre >= tamano_de_archivo_copia:
            # Retorna el espacio encontrado.
            return dir_cluster_siguiente
    # Devuelve -1 si no se encuentra un espacio.
    return -1       

def siguiente_cluster(cluster_inicial, tamano_archivo, cluster):
    # Calcula el residuo al dividir el Peso del archivo entre el Peso de un cluster.
    sobrante = tamano_archivo % cluster
    # Calcula la cantidad de espacio adicional necesario para completar el cluster actual.
    valor_a_aumentar = 1024 - sobrante
    # Retorna la dirección del siguiente cluster sumando la posición inicial,
    # el Peso del archivo y el espacio adicional necesario.
    return (cluster_inicial) * 1024 + tamano_archivo + valor_a_aumentar

# Función que calcula espacios.
def espacio_dir(sistema_archivos, cluster):
    # Llevamos el puntero sobre 'fiunamfs' a cluster.
    sistema_archivos.seek(cluster)
    # Iteramos desde 1 hasta cluster * 4 en pasos de 64 bytes.
    for i in range(1, cluster * 4, 64):
        # Llevamos el puntero sobre 'fiunamfs' a cluster + i.
        sistema_archivos.seek(cluster + i)
        # Leemos los 15 sig caracteres de 'fiunamfs' y lo añadimos a archivo convertido en ASCII.
        archivo = sistema_archivos.read(15).decode("ascii")
        # Si los siguientes 14 caracteres son "..............."
        if archivo[:14] == "..............":
            # Entonces incrementamos cluster + i.
            return cluster + i
    # Si no sucede el if, entonces mandamos de valor -1.
    return -1

def desfragmentar_archivo(archivo_original, archivo_destino):
    try:
        # Verificar si el archivo original existe.
        if os.path.exists(archivo_original):
            # Copiar el contenido del archivo original a uno nuevo.
            with open(archivo_original, 'rb') as original:
                with open(archivo_destino, 'wb') as destino:
                    shutil.copyfileobj(original, destino)
            # Archivo desfragmentado.
            print(f'Archivo desfragmentado: {archivo_destino}')

        else:
            # No existe el archivo.
            print(f'Error: El archivo en FIUNAMFS "{archivo_original}" no existe.')

    except Exception as e:
        print(f'Error al desfragmentar el archivo: {e}')

# Función que elimina de 'fiunamfs' un archivo.
def eliminar_archivo(sistema_archivos, cluster):
    # Solicita al usuario el nombre del archivo que se desea eliminar.
    archivo_a_eliminar = input("---|Ingrese nombre del archivo a eliminar: ")
    # Establece el puntero al inicio del cluster en el sistema de archivos.
    sistema_archivos.seek(cluster)
    # Itera sobre los clusters en incrementos de 64 bytes.
    for i in range(1, cluster * 4, 64):
        # Mueve el puntero al inicio del cluster actual.
        sistema_archivos.seek(cluster + i)
        # Lee el nombre del archivo del cluster y lo decodifica como ASCII.
        archivo1 = sistema_archivos.read(15).decode("ascii")[:-1]
        archivo = archivo1.replace("-","")
        print(archivo)
        if archivo == 0:
           return 
        # Comprueba si el nombre del archivo coincide con el que se desea eliminar.
        if archivo.strip() == archivo_a_eliminar.strip():
            # Mueve el puntero al inicio del cluster del archivo a eliminar.
            sistema_archivos.seek(cluster + i)
            # Marca la entrada del archivo como no utilizada (eliminada).
            sistema_archivos.write("/..............".encode("ascii"))
            print("\nArchivo eliminado... :( ")
            return
    print("\n¡Archivo a eliminar no encontrado! :(")
    
# Asignamos constantes para sector y cluster.
sector = 256
cluster = sector * 4
# Sistema de archivos relacionado con 'fiunamfs.img'.
sistema_archivos = open("fiunamfs.img", "r+b")




def info_archivo():
    # Establece el puntero al inicio del archivo (posición 0).
    sistema_archivos.seek(0)

    # Lee y decodifica los primeros 9 bytes del archivo como el nombre del sistema de archivos.
    nombre_sistema = leer_info_sistema_archivos(sistema_archivos, 0, 9)
    print("Nombre del Archivo Principal:", nombre_sistema)

    # Lee los siguientes 5 bytes como la versión de la implementación.
    version_implementacion = leer_info_sistema_archivos(sistema_archivos, 10, 5)
    print("Versión:", version_implementacion)

    # Lee los siguientes 19 bytes como la etiqueta del volumen.
    etiqueta_volumen = leer_info_sistema_archivos(sistema_archivos, 20, 19)
    print("Volumen de Etiqueta:", etiqueta_volumen)

    # Lee los siguientes 4 bytes como el Peso del cluster en bytes.
    tamaño_cluster = leer_entero(sistema_archivos, 40)
    print("Peso del cluster en bytes:", tamaño_cluster)

    # Lee los siguientes 4 bytes como el número de clusters que mide el directorio.
    num_clusters_directorio = leer_entero(sistema_archivos, 45)
    print("Número de clusters del directorio:", num_clusters_directorio)

    # Lee los siguientes 4 bytes como el número de clusters que mide la unidad completa.
    num_clusters_unidad = leer_entero(sistema_archivos, 51)
    print("Número de clusters totales:", num_clusters_unidad)

print("\n****Proyecto 3 Sistema de Archivos****\n")
# Mandamos a llamar la función que nos da la información general de 'fiunamfs.img'.
info_archivo()
# Mostramos el menú principal.
menu()

# Pausa de 1 segundo.
time.sleep(1)
# Indica el mensaje de despedida si se sale del menú.
print("\n\n---|¡Hasta luego! Este es el Proyecto 3 de Sistemas Operativos.")
print("---|Realizado por:\n---|Jonathan Emmanuel Hernández Ortiz.\n---|Paola Celina de Jesus Pérez Avin.\n\n")

# Pausa de 3 segundos.
time.sleep(3)

# Otras funciones auxiliares que realizan operaciones específicas como leer información, copiar archivos, etc.

# Código principal
# Abre el archivo 'fiunamfs.img' para trabajar con él.
# Invoca la función de información de archivo.
# Muestra el menú principal para interactuar con el sistema de archivos.