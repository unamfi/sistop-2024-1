#Miranda Barajas Victor
import os
import struct


TAMANO_CLUSTER = 1024
TAMANO_ENTRADA = 64
DIRECTORIO_INICIO = TAMANO_CLUSTER  # Cluster 1
DIRECTORIO_TAMANO = 4 * TAMANO_CLUSTER  # 4 clusters para el directorio
MAXIMO_CLUSTERS = 1440 // 4  # Asumiendo que el tamaño total es 1440KB

def leer_superbloque(fiunamfs_img):
    with open(fiunamfs_img, 'rb') as f:
        f.seek(0)
        nombre_fs = f.read(8).decode('ascii').strip()
        f.seek(10)
        version = f.read(5).decode('ascii').rstrip('\x00').strip()
        print(f"Nombre FS leído: {nombre_fs}, Versión leída: {version}")
        #print(f"Hexadecimal: {nombre_fs.encode('ascii').hex()}, {version.encode('ascii').hex()}")
        if nombre_fs != "FiUnamFS" or version.strip() != "24.1":
            print("Valores no coinciden, se esperaba FiUnamFS y  24.1")
            #raise ValueError("No es un sistema FiUnamFS válido o versión no soportada.")
        else:
            print("Superbloque válido") 

def listar_directorio(fiunamfs_img):
    with open(fiunamfs_img, 'rb') as f:
        f.seek(DIRECTORIO_INICIO)
        for _ in range(DIRECTORIO_TAMANO // TAMANO_ENTRADA):
            entrada = f.read(TAMANO_ENTRADA)
            nombre = entrada[1:16].decode('ascii').rstrip()
            if nombre != '-' * 15:
                print(f"Archivo: {nombre}")

def copiar_a_sistema(fiunamfs_img, nombre_archivo, destino):
    with open(fiunamfs_img, 'rb') as f:
        f.seek(DIRECTORIO_INICIO)
        for _ in range(DIRECTORIO_TAMANO // TAMANO_ENTRADA):
            entrada = f.read(TAMANO_ENTRADA)
            tipo_archivo = entrada[0:1]
            if tipo_archivo == b'-':
                nombre, tam, cluster_ini = (
                    entrada[1:16].decode('ascii').rstrip(),
                    struct.unpack('<I', entrada[16:20])[0],
                    struct.unpack('<I', entrada[20:24])[0]
                )
                print(f"Nombre encontrado: {nombre}, Tamaño: {tam}, Cluster inicial: {cluster_ini}")  # Para depuración
                if nombre.rstrip('\x00').strip() == nombre_archivo.rstrip('\x00').strip():
                    f.seek(cluster_ini * TAMANO_CLUSTER)
                    datos = f.read(tam)
                    with open(destino, 'wb') as archivo_destino:
                        archivo_destino.write(datos)
                    return
    raise FileNotFoundError("Archivo no encontrado en FiUnamFS")

def copiar_a_fiunamfs(fiunamfs_img, archivo_origen, nombre_destino):
    with open(fiunamfs_img, 'r+b') as f:
        tam_origen = os.path.getsize(archivo_origen)
        cluster_libre = 5
        posicion_entrada_libre = None

        f.seek(DIRECTORIO_INICIO)
        for _ in range(DIRECTORIO_TAMANO // TAMANO_ENTRADA):
            posicion_actual = f.tell()
            entrada = f.read(TAMANO_ENTRADA)
            tipo_archivo = entrada[0:1]
            cluster_ini = struct.unpack('<I', entrada[20:24])[0]

            if tipo_archivo == b'/' and posicion_entrada_libre is None:  # Verifica si la entrada está vacía
                posicion_entrada_libre = posicion_actual
                print(f"Encontrada entrada libre en posición {posicion_entrada_libre}")  # Para depuración

            if cluster_ini >= cluster_libre:
                cluster_libre = cluster_ini + 1
                print(f"Nuevo cluster libre: {cluster_libre}")  # Para depuración

        if posicion_entrada_libre is None:
            raise Exception("No hay espacio en el directorio")
        else:
            print(f"Espacio libre en la entrada: {posicion_entrada_libre}, Cluster libre para el archivo: {cluster_libre}")  # Para depuración

        with open(archivo_origen, 'rb') as archivo_origen_f:
            f.seek(cluster_libre * TAMANO_CLUSTER)
            f.write(archivo_origen_f.read())

        f.seek(posicion_entrada_libre)
        f.write(b'-' + nombre_destino.ljust(15).encode('ascii'))
        f.write(struct.pack('<I', tam_origen))
        f.write(struct.pack('<I', cluster_libre))

def eliminar_archivo(fiunamfs_img, nombre_archivo):
    with open(fiunamfs_img, 'r+b') as f:
        f.seek(DIRECTORIO_INICIO)
        for _ in range(DIRECTORIO_TAMANO // TAMANO_ENTRADA):
            posicion = f.tell()
            entrada = f.read(TAMANO_ENTRADA)
            nombre = entrada[1:16].decode('ascii').rstrip()
            if nombre.rstrip('\x00').strip() == nombre_archivo.rstrip('\x00').strip():
                f.seek(posicion)
                f.write(b'/' + b' ' * 15)
                print("Archivo eliminado")
                return
    raise FileNotFoundError("Archivo no encontrado en FiUnamFS")


