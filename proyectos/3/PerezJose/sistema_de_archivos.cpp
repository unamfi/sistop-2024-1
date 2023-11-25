#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
// Definir la estructura del superbloque
struct Superblock {
    char filesystem_name[8];  // 8 caracteres 
    char version[4];          // 4 caracteres 
};

struct Superblock2 {
    char volume_label[20];      // Etiqueta del volumen
    uint32_t cluster_size;      // Tamaño del cluster en bytes
    uint32_t dir_clusters;      // Número de clusters que mide el directorio
    uint32_t total_clusters;    // Número de clusters que mide la unidad completa
};

struct DirectoryEntry {
	char novacio[1];
    char file_type[1];
    char file_name[15];
    time_t creation_time;  // Cambiado a time_t para almacenar la fecha y hora
    time_t modification_time;
    char unused_space[12];
    uint32_t file_size;
    uint32_t initial_cluster;
};


void listarDirectorio(FILE *file, uint32_t cluster_size,uint32_t dir_clusters) {
	int entradas = 64;
	int cluster=0;
	system("cls");	
    struct DirectoryEntry entry;
    printf("Tamaño del cluster en bytes: %u\n",cluster_size);
    fread(&entry, sizeof(struct DirectoryEntry), 1, file);
    printf("Listando los contenidos del directorio...\n");
    	
	while(1) {
		fseek(file, cluster_size + cluster, SEEK_SET);
	    if(entry.novacio[0] == '-') {
			fseek(file, cluster_size + cluster, SEEK_SET);
        	fread(&entry.file_type, sizeof(char), 1, file);
        	printf("Tipo: %s\n", entry.file_type);
        	
        	fseek(file, cluster_size + cluster + 1, SEEK_SET);
			fread(&entry.file_name, sizeof(char), 14, file);
			printf("Nombre: %s\n", entry.file_name);
			
			fseek(file, cluster_size + cluster + 16, SEEK_SET);
			fread(&entry.file_size, sizeof(uint32_t), 3, file);
			printf("Tamaño: %u\n", entry.file_size);
			
			
			fseek(file, cluster_size + cluster + 20, SEEK_SET);
			fread(&entry.file_name, sizeof(uint32_t), 3, file);
			printf("Cluster inicial: %u\n", entry.initial_cluster);
			
			char creation_time_str[15], modification_time_str[15];
			strftime(creation_time_str, sizeof(creation_time_str), "%Y%m%d%H%M%S", localtime(&entry.creation_time));
    		strftime(modification_time_str, sizeof(modification_time_str), "%Y%m%d%H%M%S", localtime(&entry.modification_time));
			printf("Fecha y hora de creación: %s\n", creation_time_str);
    		printf("Fecha y hora de modificación: %s\n", modification_time_str);
			
			//fseek(file, cluster_size + cluster + 24, SEEK_SET);
			//fread(&entry.creation_time, sizeof(char), 14, file);
			//printf("Fecha creacion: %s\n", entry.creation_time);
			
			//fseek(file, cluster_size + cluster + 38, SEEK_SET);
			//fread(&entry.modification_time, sizeof(char), 14, file);
			//printf("Fecha modificacion: %s\n", entry.modification_time);
			
        	cluster += entradas;
	        continue; 
	    }
	    if(entry.novacio[0] == '/') {
	        cluster += 64; 
	        continue;
	    }
			
	}
	sleep(5);
    printf("Contenidos listados correctamente.\n");
}

void copiarDesdeFiUnamFS() {
	system("cls");
    printf("Copiando un archivo desde FiUnamFS hacia tu sistema...\n");
    // Código para copiar un archivo desde FiUnamFS
    
    sleep(5);
}

void copiarHaciaFiUnamFS() {
	system("cls");
    printf("Copiando un archivo desde tu computadora hacia FiUnamFS...\n");
    // Código para copiar un archivo hacia FiUnamFS
    
    sleep(5);
}

void eliminarDesdeFiUnamFS() {
	system("cls");
    printf("Eliminando un archivo desde FiUnamFS...\n");
    // Código para eliminar un archivo desde FiUnamFS
    
    sleep(5);
}

void desfragmentarFiUnamFS() {
	system("cls");
    printf("Desfragmentando FiUnamFS...\n");
    // Código para desfragmentar FiUnamFS
    
    sleep(5);
}

int main() {
    FILE *file = fopen("fiunamfs.img", "rb");
    if (file == NULL) {
        perror("Error al abrir el archivo");
        return 0;
    } else {
        printf("archivo abierto correctamente\n");
        sleep(2);
    }
    
    // Leer el superbloque
    struct Superblock2 superblock2;
    struct Superblock superblock;
    fread(&superblock, sizeof(struct Superblock), 1, file);

    /////////////////////////////////////////////////////////////////////
	// Validar el nombre del sistema de archivos
    if (strcmp(superblock.filesystem_name, "FiUnamFS") != 0) {
        printf("El nombre del sistema de archivos no es válido.\n");
        fclose(file);
        return 0;
    } 
    printf("Nombre del sistema de archivos: %s\n", superblock.filesystem_name);
   
    // Validar la versión del sistema de archivos
    fseek(file, 10, SEEK_SET);
    fread(superblock.version, sizeof(char), 4, file);
    printf("Versión del sistema de archivos: %s\n", superblock.version);
    //sleep(2);
    if (strcmp(superblock.version, "24.1") != 0) {
        printf("La versión del sistema de archivos no es compatible.\n");
        fclose(file);
        return 0;
    }
    
    ////////////////////////////////////////////////////////////////////
    
    fread(&superblock2, sizeof(struct Superblock2), 1, file);
    
    //volumen
    fseek(file, 20, SEEK_SET);
	fread(superblock2.volume_label, sizeof(char), 19, file);
	printf("Etiqueta del volumen: %s\n", superblock2.volume_label);
	
	//tamaño cluster
	fseek(file, 40, SEEK_SET);
	fread(&superblock2.cluster_size, sizeof(uint32_t), 4, file);
	printf("Tamaño del cluster en bytes: %u\n", superblock2.cluster_size);
	
	//directorio
    fseek(file, 45, SEEK_SET);
	fread(&superblock2.dir_clusters, sizeof(uint32_t), 4, file);
	printf("Número de clusters que mide el directorio: %u\n", superblock2.dir_clusters);
	
	//unidad completa
	fseek(file, 50, SEEK_SET);
	fread(&superblock2.total_clusters, sizeof(uint32_t), 4, file);
	printf("Número de clusters que mide la unidad completa: %u\n", superblock2.total_clusters);	
    //sleep(7);
    ////////////////////////////////////////////////////////////////////////
	
    int opcion;
    do {
        // Mostrar el menú
        //system("cls");
        printf("Menú:\n");
        printf("1. Listar contenidos del directorio\n");
        printf("2. Copiar desde FiUnamFS hacia tu sistema\n");
        printf("3. Copiar desde tu computadora hacia FiUnamFS\n");
        printf("4. Eliminar un archivo desde FiUnamFS\n");
        printf("5. Desfragmentar FiUnamFS\n");
        printf("6. Salir\n");

        // Solicitar la opción al usuario
        printf("Ingresa el número de la opción deseada: ");
        scanf("%d", &opcion);
	
        // Realizar acciones según la opción seleccionada
        switch (opcion) {
            case 1:
                listarDirectorio(file, superblock2.cluster_size, superblock2.dir_clusters);
                break;
            case 2:
                copiarDesdeFiUnamFS();
                break;
            case 3:
                copiarHaciaFiUnamFS();
                break;
            case 4:
                eliminarDesdeFiUnamFS();
                break;
            case 5:
                desfragmentarFiUnamFS();
                break;
            case 6:
                printf("Saliendo del programa. ¡Hasta luego!\n");
                break;
            default:
                printf("Opción no válida. Por favor, ingresa un número válido.\n");
                sleep(3);
        }
    } while (opcion != 6);

    fclose(file);

    return 0;
}
