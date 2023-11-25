#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

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
  
};

void listarContenidos(FILE *file) {
	system("cls");
    printf("Listando los contenidos del directorio...\n");
    sleep(5);
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
void informacion(){
	FILE *file = fopen("fiunamfs.img", "rb");
	struct Superblock2 superblock2;
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
    sleep(7);
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
    struct Superblock superblock;
    fread(&superblock, sizeof(struct Superblock), 1, file);

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
    sleep(2);
    if (strcmp(superblock.version, "24.1") != 0) {
        printf("La versión del sistema de archivos no es compatible.\n");
        fclose(file);
        return 0;
    }
    
    informacion();
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
                listarContenidos(file);
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
