import os
import struct
import time

class FiUnamFS:
    def __init__(self, disco_path):
        self.disco_path = disco_path
        self.superbloque = bytearray(64)  # Usar bytearray en lugar de bytes
        self.datos = bytearray(1440 * 1024)  # inicializar la variable de datos
        self.directorio = bytearray(1440 * 1024)  # inicializar la variable de directorio
        self.cargar_superbloque()

    def cargar_superbloque(self):
        with open(self.disco_path, 'rb') as file:
            file.readinto(self.superbloque)
            file.readinto(self.directorio)  # cargar el directorio
            file.readinto(self.datos)  # cargar los datos

    def guardar_superbloque(self):
        with open(self.disco_path, 'r+b') as file:
            file.seek(0)
            file.write(self.superbloque)
            file.write(self.directorio)  # guardar el directorio
            file.write(self.datos)  # guardar los datos

    def listar_contenidos(self):
        print("Contenidos del directorio:")
        for i in range(0, len(self.directorio), 64):
            tipo_archivo = self.directorio[i]
            if tipo_archivo == 0x0f:
                continue
            nombre = self.directorio[i + 1:i + 16].decode('ascii').rstrip('-')
            print(nombre)

    def copiar_desde_fiunamfs_a_sistema(self, origen, destino):
        entrada = self._buscar_entrada_directorio(origen)
        if entrada is None:
            print(f"No se encontró el archivo {origen} en FiUnamFS.")
            return

        contenido = self.datos[entrada['cluster_inicial']:entrada['cluster_inicial'] + entrada['tamano']]
        print(f"Archivo {origen} copiado desde FiUnamFS a {destino}. Dirección de inicio en FiUnamFS: {entrada['cluster_inicial']}")

        with open(destino, 'wb') as dest_file:
            dest_file.write(contenido)

        print(f"Archivo {origen} copiado desde FiUnamFS a {destino}.")

    def copiar_a_fiunamfs_desde_sistema(self, origen, destino):
        # Verificar si el archivo local existe, y crearlo si no (Lo hice porque no vi el archivo .img en git)
        if not os.path.exists(origen):
            with open(origen, 'w') as local_file:
                local_file.write("Este es el contenido del archivo_local.txt.\n")

        with open(origen, 'rb') as src_file:
            contenido = src_file.read()

        # Buscar un espacio libre en el directorio para el nuevo archivo
        entrada_vacia = self.directorio.find(b'\x0f' * 16)
        if entrada_vacia == -1:
            print("No hay espacio en el directorio.")
            return

        # Escribir la entrada en el directorio
        nombre_archivo = os.path.basename(destino)[:15].encode('ascii').ljust(15, b'-')
        self.directorio[entrada_vacia:entrada_vacia + 16] = b'\x2d' + nombre_archivo

        # Buscar un espacio libre en el área de datos
        espacio_libre = self.datos.find(b'\x00' * len(contenido))
        if espacio_libre == -1:
            print("No hay suficiente espacio en FiUnamFS.")
            return

        # Escribir el contenido en el área de datos
        self.datos[espacio_libre:espacio_libre + len(contenido)] = contenido

        # Actualizar la entrada en el directorio con la información del nuevo archivo
        self._actualizar_entrada_directorio(entrada_vacia, len(contenido), espacio_libre)

        print(f"Archivo {nombre_archivo.decode('ascii')} copiado a FiUnamFS.")

    def eliminar_en_fiunamfs(self, archivo):
        entrada = self._buscar_entrada_directorio(archivo)
        if entrada is None:
            print(f"No se encontró el archivo {archivo} en FiUnamFS.")
            return

        self.directorio[entrada['offset']:entrada['offset'] + 16] = b'\x0f' * 16

        print(f"Archivo {archivo} eliminado de FiUnamFS.")

    def desfragmentar_fiunamfs(self):
        archivos = self._obtener_archivos_directorio()
        self.datos = bytearray(1440 * 1024)

        offset = 0
        for archivo in archivos:
            contenido = archivo['contenido']
            self.datos[offset:offset + len(contenido)] = contenido
            archivo['cluster_inicial'] = offset
            archivo['offset'] = offset  # Actualizar el valor de 'offset' en la información del archivo
            offset += len(contenido)

            self._actualizar_entrada_directorio(archivo['offset'], len(contenido), archivo['cluster_inicial'])

        print("FiUnamFS desfragmentado.")

    def _buscar_entrada_directorio(self, nombre_archivo):
        for i in range(0, len(self.directorio), 64):
            tipo_archivo = self.directorio[i]
            if tipo_archivo == 0x0f:
                continue
            nombre = self.directorio[i + 1:i + 16].decode('ascii').rstrip('-')
            if nombre == nombre_archivo:
                return {
                    'offset': i,
                    'tamano': struct.unpack('<I', self.directorio[i + 16:i + 20])[0],
                    'cluster_inicial': struct.unpack('<I', self.directorio[i + 20:i + 24])[0],
                }
        return None

    def _obtener_archivos_directorio(self):
        archivos = []
        for i in range(0, len(self.directorio), 64):
            tipo_archivo = self.directorio[i]
            if tipo_archivo == 0x0f:
                continue
            nombre = self.directorio[i + 1:i + 16].decode('ascii').rstrip('-')
            tamano = struct.unpack('<I', self.directorio[i + 16:i + 20])[0]
            cluster_inicial = struct.unpack('<I', self.directorio[i + 20:i + 24])[0]
            contenido = self.datos[cluster_inicial:cluster_inicial + tamano]
            archivos.append({
                'nombre': nombre,
                'tamano': tamano,
                'cluster_inicial': cluster_inicial,
                'contenido': contenido,
            })
        return archivos

    def _actualizar_entrada_directorio(self, offset, tamano, cluster_inicial):
        self.directorio[offset + 16:offset + 20] = struct.pack('<I', tamano)
        self.directorio[offset + 20:offset + 24] = struct.pack('<I', cluster_inicial)

        fecha_modificacion = time.strftime('%Y%m%d%H%M%S', time.localtime())
        self.directorio[offset + 38:offset + 52] = fecha_modificacion.encode('ascii')

        self.guardar_superbloque()

# Uso
disco_path = 'fiunamfs.img'

if not os.path.exists(disco_path):
    with open(disco_path, 'wb') as f:
        f.write(b'\x00' * (1440 * 1024))

# Copiar un archivo a FiUnamFS
fiunamfs = FiUnamFS(disco_path)

# Listar contenidos
print("Contenidos del directorio después de copiar:")
fiunamfs.listar_contenidos()

# Copiar un archivo desde FiUnamFS al sistema
fiunamfs.copiar_desde_fiunamfs_a_sistema('archivo_fiunamfs.txt', 'archivo_local_copiado.txt')

# Copiar un archivo desde el sistema a FiUnamFS
fiunamfs.copiar_a_fiunamfs_desde_sistema('archivo_local.txt', 'archivo_fiunamfs.txt')

# Eliminar un archivo en FiUnamFS
fiunamfs.eliminar_en_fiunamfs('archivo_fiunamfs.txt')

# Listar contenidos
print("Contenidos del directorio después de eliminar:")
fiunamfs.listar_contenidos()

# Desfragmentar FiUnamFS
fiunamfs.desfragmentar_fiunamfs()

# Listar contenidos
print("Contenidos del directorio después de desfragmentar:")
fiunamfs.listar_contenidos()
