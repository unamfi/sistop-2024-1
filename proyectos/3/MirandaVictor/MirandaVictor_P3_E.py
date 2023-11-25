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

