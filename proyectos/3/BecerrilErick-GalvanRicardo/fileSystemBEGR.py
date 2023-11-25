import os
import struct 
import time

#ruta del sistema
nombre_archivo_img = r"/Users/PC/Desktop/SO/Proyecto3/fiunamfs.img"

def validar_superbloque(nombre_archivo):
    with open(nombre_archivo, "rb") as f:
        data = f.read(54) #obtener 56 bytes del bloque
        #implementación un poco "sucia", pero que permite obtener la cadena del sistema y de la versión:
        magic, versionk = struct.unpack("<8s6s", data[:14]) #se obtienen 8 y 6 caracteres; para sistema y versión
        version = struct.unpack("<4s", data[10:14]) #la version se obtiene de 10 a 14 bytes
        version = versionk[2:6] #esta linea fuerza que "version" sea string, para aplicar decode después.

        #comprobación de cadena que identifica al sistema de archivos
        if magic.decode("ascii") != "FiUnamFS":
            print("¡Error! No es un sistema de archivos FiUnamFS.")
            return False
        else:
            print("El sistema es correcto.")

        #comprobación de versión
        if version.decode("ascii") != "24.1":
            print("¡Error! Versión no compatible.")
            return False
        else:
            print("La versión es compatible.\n\n")

        return True
      

def leer_superbloque(nombre_archivo):
    if validar_superbloque(nombre_archivo):
        with open(nombre_archivo, "rb") as f:
            data = f.read(54)
            #Al obtener los datos "de golpe" se generaban problemas, por lo que se obtienen uno por uno
            #Las variables dump y dumpy tienen como único propósito guardar bytes irrelevantes entre los datos:
            dump, label, dumpy = struct.unpack("<20s19s15s", data)
            print(label.decode("ascii"))
            dump, cluster_size, dumpy = struct.unpack("<40sI10s", data)
            print("Tamanio de clusters: %d bytes." % cluster_size)
            dump, dir_clusters, dumpy = struct.unpack("<45sI5s", data)
            print("Clusters del directorio: %d." % cluster_size)
            dump, total_clusters = struct.unpack("<50sI", data)
            print("Clusters de la unidad completa: %d." % total_clusters)

            return {
                "label": label.decode("ascii").rstrip('\x00'),
                "cluster_size": cluster_size,
                "dir_clusters": dir_clusters,
                "total_clusters": total_clusters
            }
    else:
        return None

def listar_contenidos(nombre_archivo):
    superbloque = leer_superbloque(nombre_archivo)

    if superbloque:
        with open(nombre_archivo, "rb") as f: #abre el sistema
            f.seek(superbloque["cluster_size"]) #se coloca en el superbloque
            for _ in range(superbloque["dir_clusters"]): #por cada cluster en el directorio
                entrada = f.read(64)
                #se obtienen los datos del archivo a listar
                tipo, nombre, tamaño, cluster_inicial, creacion, modificacion, dump = struct.unpack("<c15sI3s14s14s13s", entrada)

                #cluster_inicial_int = int.from_bytes(cluster_inicial, "little") #convertir cluster inicial, de bytes a entero
                if nombre.decode("ascii").rstrip('\x00') != "---------------":
                    print("Nombre: {}, Tamaño: {}, Cluster Inicial: {}".format(
                        nombre.decode('ascii').rstrip('\x00'), tamaño, cluster_inicial))

def copiar_desde_fiunamfs(nombre_archivo, nombre_archivo_img):
    superbloque = leer_superbloque(nombre_archivo_img)

    if superbloque:
        with open(nombre_archivo_img, "rb") as f:
            f.seek(superbloque["cluster_size"])
            for _ in range(superbloque["dir_clusters"]):
                entrada = f.read(64) #obtiene 64 bytes de la entrada del directorio
                #obtiene todos los valores, dump recibe los bytes no relevantes:
                tipo, nombre, tamaño, cluster_inicial, creacion, modificacion, dump = struct.unpack("<c15sI3s14s14s13s", entrada)
                #al utilizar rstrip no se eliminaban los caracteres nulos o espacios en blanco, por lo que
                #se resuelve usando las longitudes de los nombres de archivo para hacer la comparación
                longitud = len(nombre_archivo)
                nombred = nombre.decode("ascii")
                nombre = nombred[0:longitud] 
                if nombre == nombre_archivo and tipo == b'-':
                    with open(nombre_archivo, "wb") as destino:
                        #se convierte el valor del cluster inicial, de bytes a un valor entero con little endian
                        #para poder realizar la escritura correctamente
                        cluster_inicial_int = int.from_bytes(cluster_inicial, "little")
                        f.seek(cluster_inicial_int * superbloque["cluster_size"])
                        contenido = f.read(tamaño)
                        destino.write(contenido)
                        print(f"Archivo {nombre_archivo} copiado exitosamente.")
                        return

        print(f"No se encontró el archivo {nombre_archivo} en FiUnamFS.")

def copiar_a_fiunamfs_desde_sistema(nombre_archivo, nombre_archivo_img):
    superbloque = leer_superbloque(nombre_archivo_img)

    if superbloque:
        with open(nombre_archivo, "rb") as origen:
            tamaño = os.path.getsize(nombre_archivo)

            with open(nombre_archivo_img, "r+b") as f:
                f.seek(superbloque["cluster_size"])
                for _ in range(superbloque["dir_clusters"]):
                    entrada = f.read(64)
                    tipo, nombre, tamaño, cluster_inicial, creacion, modificacion, dump = struct.unpack("<c15sI3s14s14s13s", entrada)

                    #identifica si la entrada del directorio no está en uso, y escribe los datos al archivo
                    if nombre.decode("ascii").rstrip('\x00') == nombre_archivo or nombre.decode("ascii").rstrip('\x00') == "---------------":
                        f.seek(f.tell() - 64)
                        f.write(struct.pack("<s15sIQ14s14s14s", b'-', nombre_archivo.ljust(15, '\x00').encode('ascii'), tamaño,
                                            superbloque["total_clusters"], time.strftime("%Y%m%d%H%M%S").encode('ascii'),
                                            time.strftime("%Y%m%d%H%M%S").encode('ascii'), b''))

                        #se escribe el contenido leido en el archivo copia
                        for _ in range(superbloque["total_clusters"]):
                            contenido = origen.read(superbloque["cluster_size"])
                            f.write(contenido)

                            f.seek(44)
                            f.write(struct.pack("<I", superbloque["total_clusters"] - 1))

                            print(f"Archivo {nombre_archivo} copiado exitosamente.")
                            return

                print("No hay espacio en el directorio para el nuevo archivo.")

def eliminar_archivo(nombre_archivo, nombre_archivo_img):
    superbloque = leer_superbloque(nombre_archivo_img)

    if superbloque:
        with open(nombre_archivo_img, "r+b") as f:
            f.seek(superbloque["cluster_size"])
            for _ in range(superbloque["dir_clusters"]):
                entrada = f.read(64)
                tipo, nombre, tamaño, cluster_inicial, creacion, modificacion, dump = struct.unpack("<c15sI3s14s14s13s", entrada)

                longitud = len(nombre_archivo)
                nombred = nombre.decode("ascii")
                nombre = nombred[0:longitud]
                if nombre == nombre_archivo and tipo == b'-':
                    # Actualiza la entrada del directorio con información de eliminación
                    f.seek(f.tell() - 64)
                    f.write(struct.pack("<s15sIQ14s14s14s", b'/', "---------------".encode('ascii'), 0, 0, b'', b'', b''))
                    print(f"Archivo {nombre_archivo} eliminado exitosamente.")
                    return

            print(f"No se encontró el archivo {nombre_archivo} en FiUnamFS.")

def desfragmentar_fiunamfs(nombre_archivo_img):
    superbloque = leer_superbloque(nombre_archivo_img)

    if superbloque:
        with open(nombre_archivo_img, "r+b") as f:
            f.seek(superbloque["cluster_size"])
            entries = []

            for _ in range(superbloque["dir_clusters"]):
                entrada = f.read(64)
                tipo, nombre, tamaño, cluster_inicial, creacion, modificacion, dump = struct.unpack("<c15sI3s14s14s13s", entrada)

                if nombre.decode("ascii").rstrip('\x00') != "---------------":
                    entries.append((tipo, nombre, tamaño, cluster_inicial))

            # Ordenar las entradas por el cluster inicial
            entries.sort(key=lambda x: x[3])

            # Reescribir el directorio con las entradas ordenadas
            f.seek(superbloque["cluster_size"])
            for entry in entries:
                tipo, nombre, tamaño, cluster_inicial = entry
                f.write(struct.pack("<s15sIQ14s14s14s", tipo, nombre, tamaño, cluster_inicial, b'', b'', b''))

        print("FiUnamFS desfragmentado exitosamente.")

if __name__ == "__main__":
    while True:
        print("\nSeleccione una opción:")
        print("1. Listar contenidos del directorio")
        print("2. Copiar archivo desde FiUnamFS al sistema")
        print("3. Copiar archivo desde el sistema a FiUnamFS")
        print("4. Eliminar archivo de FiUnamFS")
        print("5. Desfragmentar FiUnamFS")
        print("6. Salir")

        opcion = input("Ingrese el número de la opción deseada: ")

        if opcion == "1":
            listar_contenidos(nombre_archivo_img)
        elif opcion == "2":
            nombre_archivo = input("Ingrese el nombre del archivo a copiar desde FiUnamFS al sistema: ")
            copiar_desde_fiunamfs(nombre_archivo, nombre_archivo_img)
        elif opcion == "3":
            nombre_archivo = input("Ingrese el nombre del archivo a copiar desde el sistema a FiUnamFS: ")
            copiar_a_fiunamfs_desde_sistema(nombre_archivo, nombre_archivo_img)
        elif opcion == "4":
            nombre_archivo = input("Ingrese el nombre del archivo a eliminar de FiUnamFS: ")
            eliminar_archivo(nombre_archivo, nombre_archivo_img)
        elif opcion == "5":
            desfragmentar_fiunamfs(nombre_archivo_img)
        elif opcion == "6":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, ingrese un número válido.")
