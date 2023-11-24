import os
import struct 
import time

nombre_archivo_img = r"/Users/PC/Desktop/SO/Proyecto3/fiunamfs.img"

def validar_superbloque(nombre_archivo):
    with open(nombre_archivo, "rb") as f:
        data = f.read(54)
        magic, versionk = struct.unpack("<8s6s", data[:14])
        version = struct.unpack("<4s", data[10:14])
        version = versionk[2:6]

        if magic.decode("ascii") != "FiUnamFS":
            print("¡Error! No es un sistema de archivos FiUnamFS.")
            return False
        else:
            print("El sistema es correcto.")

        if version.decode("ascii") != "24.1":
            print("¡Error! Versión no compatible.")
            return False
        else:
            print("La versión es compatible.")

        return True
      

def leer_superbloque(nombre_archivo):
    if validar_superbloque(nombre_archivo):
        with open(nombre_archivo, "rb") as f:
            data = f.read(54)
            magic, version, label, cluster_size, dir_clusters, total_clusters = struct.unpack("<8s5s20sIQQ", data)

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
        with open(nombre_archivo, "rb") as f:
            f.seek(superbloque["cluster_size"])
            for _ in range(superbloque["dir_clusters"]):
                entrada = f.read(64)
                tipo, nombre, tamaño, cluster_inicial, _, _ = struct.unpack("<s15sIQ14s14s14s", entrada)

                if nombre.decode("ascii").rstrip('\x00') != "---------------":
                    print("Nombre: {}, Tamaño: {}, Cluster Inicial: {}".format(
                        nombre.decode('ascii').rstrip('\x00'), tamaño, cluster_inicial))

def copiar_desde_fiunamfs(nombre_archivo, nombre_archivo_img):
    superbloque = leer_superbloque(nombre_archivo_img)

    if superbloque:
        with open(nombre_archivo_img, "rb") as f:
            f.seek(superbloque["cluster_size"])
            for _ in range(superbloque["dir_clusters"]):
                entrada = f.read(64)
                tipo, nombre, tamaño, cluster_inicial, _, _ = struct.unpack("<s15sIQ14s14s14s", entrada)

                if nombre.decode("ascii").rstrip('\x00') == nombre_archivo and tipo == b'-':
                    with open(nombre_archivo, "wb") as destino:
                        f.seek(cluster_inicial * superbloque["cluster_size"])
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
                    tipo, nombre, _, _, _, _ = struct.unpack("<s15sIQ14s14s14s", entrada)

                    if nombre.decode("ascii").rstrip('\x00') == nombre_archivo or nombre.decode("ascii").rstrip('\x00') == "---------------":
                        f.seek(f.tell() - 64)
                        f.write(struct.pack("<s15sIQ14s14s14s", b'-', nombre_archivo.ljust(15, '\x00').encode('ascii'), tamaño,
                                            superbloque["total_clusters"], time.strftime("%Y%m%d%H%M%S").encode('ascii'),
                                            time.strftime("%Y%m%d%H%M%S").encode('ascii'), b''))

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
                tipo, nombre, _, _, _, _ = struct.unpack("<s15sIQ14s14s14s", entrada)

                if nombre.decode("ascii").rstrip('\x00') == nombre_archivo and tipo == b'-':
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
                tipo, nombre, tamaño, cluster_inicial, _, _ = struct.unpack("<s15sIQ14s14s14s", entrada)

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
