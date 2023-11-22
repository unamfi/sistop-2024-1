import struct
import os
import datetime

# Función para leer el superbloque
def read_superblock():
    with open('FiUnamFS', 'rb') as file:
        file.seek(0)
        data = file.read(64)  # Tamaño del superbloque
        # Leer y desempaquetar los datos del superbloque
        superblock = struct.unpack("<9s5s20sI3I", data)
        return superblock

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
def delete_from_FiUnamFS(file_name):
    # Eliminar el archivo del directorio y liberar sus clusters
    # ...

# Función para desfragmentar FiUnamFS
def defragment_FiUnamFS():
    # Implementar la lógica para desfragmentar el sistema de archivos
    # ...

# Ejemplo de uso
if __name__ == "__main__":
    # Definir tamaños y posiciones según la especificación
    cluster_size = 1024
    directory_start = 1
    directory_cluster_size = 4
    
    # Leer el superbloque para validar el sistema de archivos
    superblock = read_superblock()
    # Realizar las operaciones requeridas utilizando las funciones definidas
    # ...
