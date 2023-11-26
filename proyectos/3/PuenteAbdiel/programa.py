import struct
import os
import datetime
# Definir constantes y variables globales
cluster_size = 1024
directory_start = 1
directory_cluster_size = 4

# Función para leer el superbloque y validar el sistema de archivos
def list_directory():
    try:
        with open('FiUnamFS', 'rb') as file:
            file.seek(cluster_size * directory_start)
            data = file.read(directory_cluster_size * cluster_size)

            for i in range(0, len(data), 64):
                entry = struct.unpack("<c15sI14s14s14s", data[i:i+64])

                file_type = entry[0].decode('utf-8')
                file_name = entry[1].decode('utf-8').rstrip('\x00')
                file_size = entry[2]
                creation_time = datetime.datetime.strptime(entry[3].decode('utf-8'), '%Y%m%d%H%M%S')
                modification_time = datetime.datetime.strptime(entry[4].decode('utf-8'), '%Y%m%d%H%M%S')

                if file_type != '/':
                    print(f"Tipo: {file_type}, Nombre: {file_name}, Tamaño: {file_size} bytes")
                    print(f"Fecha de creación: {creation_time}, Fecha de modificación: {modification_time}")
                    print("--------------------")
    except FileNotFoundError:
        print("El archivo 'FiUnamFS' no se encuentra en la ruta especificada.")

# Función para listar los contenidos del directorio
def list_directory():
    with open('FiUnamFS', 'rb') as file:
        file.seek(cluster_size * directory_start)
        data = file.read(directory_cluster_size * cluster_size)

        # Iterar sobre las entradas del directorio (de 64 bytes cada una)
        for i in range(0, len(data), 64):
            entry = struct.unpack("<c15sI14s14s14s", data[i:i+64])
            
            # Extraer información de la entrada del directorio
            file_type = entry[0].decode('utf-8')  # Tipo de archivo
            file_name = entry[1].decode('utf-8').rstrip('\x00')  # Nombre del archivo
            file_size = entry[2]  # Tamaño del archivo en bytes
            creation_time = datetime.datetime.strptime(entry[3].decode('utf-8'), '%Y%m%d%H%M%S')  # Fecha de creación
            modification_time = datetime.datetime.strptime(entry[4].decode('utf-8'), '%Y%m%d%H%M%S')  # Fecha de modificación
            
            # Mostrar la información de la entrada del directorio
            if file_type != '/':
                print(f"Tipo: {file_type}, Nombre: {file_name}, Tamaño: {file_size} bytes")
                print(f"Fecha de creación: {creation_time}, Fecha de modificación: {modification_time}")
                print("--------------------")
        
# Función para copiar un archivo desde FiUnamFS a tu sistema
def copy_from_FiUnamFS(file_name):
    with open('FiUnamFS', 'rb') as file_fs:
        file_fs.seek(cluster_size * directory_start)
        data = file_fs.read(directory_cluster_size * cluster_size)

        # Buscar el archivo en el directorio
        found = False
        for i in range(0, len(data), 64):
            entry = struct.unpack("<c15sI", data[i:i+20])
            file_type = entry[0].decode('utf-8')
            file_name_fs = entry[1].decode('utf-8').rstrip('\x00')
            file_cluster = entry[2]

            if file_type != '/' and file_name_fs == file_name:
                found = True
                # Leer los datos del archivo en el sistema de archivos
                file_fs.seek(cluster_size * file_cluster)
                file_data = file_fs.read(cluster_size)
                
                # Escribir los datos en un archivo en tu sistema
                with open(f'copied_{file_name}', 'wb') as local_file:
                    local_file.write(file_data)
                print(f"Archivo {file_name} copiado exitosamente al sistema")
                break
        
        if not found:
            print(f"El archivo {file_name} no fue encontrado en el directorio")

# Función para copiar un archivo desde tu sistema a FiUnamFS
def copy_to_FiUnamFS(file_name):
    try:
        with open(file_name, 'rb') as local_file:
            # Leer los datos del archivo en tu sistema
            file_data = local_file.read()
            
            # Escribir los datos en el sistema de archivos simulado
            with open('FiUnamFS', 'r+b') as file_fs:
                # Buscar espacio libre en el sistema de archivos para escribir los datos
                # Esto implica encontrar un cluster disponible y escribir los datos allí
                
                # Supongamos que 'free_cluster' contiene el número de un cluster libre
                free_cluster = find_free_cluster()
                if free_cluster is not None:
                    file_fs.seek(cluster_size * free_cluster)
                    file_fs.write(file_data)
                    
                    # Actualizar la entrada del directorio con la información del nuevo archivo
                    # Esto implica encontrar la entrada libre en el directorio y actualizarla con los detalles del nuevo archivo
                    update_directory_entry(file_name, free_cluster, len(file_data))
                    
                    print(f"Archivo {file_name} copiado exitosamente a FiUnamFS")
                else:
                    print("No hay espacio disponible en FiUnamFS para copiar el archivo")
    except FileNotFoundError:
        print(f"No se pudo encontrar el archivo {file_name} en tu sistema")
    except Exception as e:
        print(f"Ocurrió un error al copiar el archivo a FiUnamFS: {e}")

    # Función para encontrar un cluster libre en el sistema de archivos
def find_free_cluster():
    with open('FiUnamFS', 'r+b') as file_fs:
        # Supongamos que el superbloque indica información sobre clústeres libres
        # y tiene un mapa de bits que indica qué clústeres están ocupados o libres
        # Aquí se lee ese mapa de bits y se busca un clúster libre
        
        # Suponiendo que el mapa de bits empieza después del superbloque
        file_fs.seek(64)  # Suponiendo un superbloque de 64 bytes
        bit_map = file_fs.read(cluster_size)  # Leer el mapa de bits
        
        for i, byte in enumerate(bit_map):
            for j in range(8):
                bit = (byte >> j) & 1
                if bit == 0:
                    # Encontramos un bit (cluster) libre
                    return i * 8 + j  # Devolvemos el número del cluster libre

        # Si no se encuentra ningún clúster libre
        return None

# Función para actualizar la entrada del directorio con la información del nuevo archivo
def find_empty_directory_entry():
    with open('FiUnamFS', 'r+b') as file_fs:
        file_fs.seek(cluster_size * directory_start)
        data = file_fs.read(directory_cluster_size * cluster_size)

        # Buscar una entrada libre en el directorio
        for i in range(0, len(data), 64):
            entry = struct.unpack("<c15sI", data[i:i+20])
            file_type = entry[0].decode('utf-8')
            if file_type == '/':
                return i // 64  # Devolvemos el número de la entrada libre (índice)

        # Si no se encuentra ninguna entrada libre
        return None

# Función para actualizar la entrada del directorio con la información del nuevo archivo
def update_directory_entry(file_name, cluster, file_size):
    empty_entry_index = find_empty_directory_entry()
    if empty_entry_index is not None:
        with open('FiUnamFS', 'r+b') as file_fs:
            file_fs.seek(cluster_size * directory_start + empty_entry_index * 64)

            # Crear la nueva entrada para el archivo
            file_type = b'-'
            file_name_encoded = file_name.ljust(15, '\x00').encode('utf-8')
            file_cluster = struct.pack("<I", cluster)
            file_size_packed = struct.pack("<I", file_size)
            creation_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S').encode('utf-8')
            modification_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S').encode('utf-8')
            
            # Componer la nueva entrada y escribirla en el directorio
            new_entry = file_type + file_name_encoded + file_size_packed + file_cluster + creation_time + modification_time
            file_fs.write(new_entry)

# Función para eliminar un archivo de FiUnamFS
# Función para eliminar un archivo del directorio y liberar sus clusters
def delete_from_FiUnamFS(file_name):
    with open('FiUnamFS', 'r+b') as file_fs:
        file_fs.seek(cluster_size * directory_start)
        data = file_fs.read(directory_cluster_size * cluster_size)

        # Buscar el archivo en el directorio
        found = False
        for i in range(0, len(data), 64):
            entry = struct.unpack("<c15sI", data[i:i+20])
            file_type = entry[0].decode('utf-8')
            file_name_fs = entry[1].decode('utf-8').rstrip('\x00')

            if file_type != '/' and file_name_fs == file_name:
                found = True
                # Marcar la entrada como vacía en el directorio
                file_fs.seek(cluster_size * directory_start + i)
                file_fs.write(b'/---------------')

                # Liberar los clusters asociados al archivo
                cluster_to_free = entry[2]
                free_clusters(cluster_to_free)
                print(f"Archivo {file_name} eliminado exitosamente del directorio")
                break
        
        if not found:
            print(f"El archivo {file_name} no fue encontrado en el directorio")

# Función para liberar los clusters asociados a un archivo eliminado
def free_clusters(start_cluster):
    with open('FiUnamFS', 'r+b') as file_fs:
        file_fs.seek(cluster_size * directory_start + 64)  # Supongamos que el mapa de bits comienza después del directorio
        byte_offset = start_cluster // 8
        bit_offset = start_cluster % 8
        
        file_fs.seek(byte_offset, 1)  # Ir a la posición del byte en el mapa de bits
        byte = ord(file_fs.read(1))
        
        # Marcar el cluster inicial como libre
        byte &= ~(1 << bit_offset)  # Se borra el bit correspondiente para marcarlo como libre
        
        file_fs.seek(byte_offset)
        file_fs.write(bytes([byte]))

# Función para desfragmentar FiUnamFS
def defragment_FiUnamFS():
    with open('FiUnamFS', 'r+b') as file_fs:
        # Leer el directorio para obtener los archivos activos
        file_fs.seek(cluster_size * directory_start)
        directory_data = file_fs.read(directory_cluster_size * cluster_size)
        
        # Crear una lista para mantener un seguimiento de los clústeres ocupados por archivos
        occupied_clusters = set()
        for i in range(0, len(directory_data), 64):
            entry = struct.unpack("<c15sI", directory_data[i:i+20])
            file_type = entry[0].decode('utf-8')
            file_cluster = entry[2]
            if file_type != '/':
                occupied_clusters.add(file_cluster)
        
        # Crear un nuevo archivo FiUnamFS_temp para realizar la desfragmentación
        with open('FiUnamFS_temp', 'wb') as temp_fs:
            # Escribir el superbloque en FiUnamFS_temp
            file_fs.seek(0)
            superbloque = file_fs.read(64)
            temp_fs.write(superbloque)
            
            # Escribir el directorio en FiUnamFS_temp
            temp_fs.seek(cluster_size * directory_start)
            temp_fs.write(directory_data)
            
            # Copiar los archivos activos a FiUnamFS_temp (compactando)
            for cluster in sorted(occupied_clusters):
                file_fs.seek(cluster_size * cluster)
                data = file_fs.read(cluster_size)
                temp_fs.seek(cluster_size * cluster)
                temp_fs.write(data)
    
    # Reemplazar FiUnamFS con FiUnamFS_temp
    os.remove('FiUnamFS')
    os.rename('FiUnamFS_temp', 'FiUnamFS')
def read_superblock():
    try:
        with open('FiUnamFS', 'rb') as file:
            data = file.read(64)  # Tamaño del superbloque
            superblock = struct.unpack("<9s5s20sI3I", data)
            # Validar sistema de archivos
            if superblock[0].decode('utf-8') != 'FiUnamFS':
                raise ValueError("El sistema de archivos no es FiUnamFS")
            if superblock[1].decode('utf-8') != '24.1  ':
                raise ValueError("Versión incorrecta del sistema de archivos")
            return superblock
    except FileNotFoundError:
        print("El archivo 'FiUnamFS' no se encuentra en la ruta especificada.")
        # Realiza alguna acción o manejo de error apropiado aquí

# ... (Otras funciones)

def list_directory():
    try:
        with open('FiUnamFS', 'rb') as file:
            file.seek(cluster_size * directory_start)
            data = file.read(directory_cluster_size * cluster_size)

            # Resto de la lógica de la función...
    except FileNotFoundError:
        print("El archivo 'FiUnamFS' no se encuentra en la ruta especificada.")
        # Realiza alguna acción o manejo de error apropiado aquí

# ... (Otras funciones)

def main():
    print("Seleccione una acción:")
    print("1. Listar directorio")
    print("2. Copiar archivo desde FiUnamFS al sistema")
    print("3. Salir")

    choice = input("Ingrese el número de la acción que desea realizar: ")

    if choice == '1':
        list_directory()
    elif choice == '2':
        file_name = input("Ingrese el nombre del archivo que desea copiar desde FiUnamFS al sistema: ")
        copy_from_FiUnamFS(file_name)
    elif choice == '3':
        print("Saliendo...")
    else:
        print("Selección no válida")

if __name__ == "__main__":
    main()
