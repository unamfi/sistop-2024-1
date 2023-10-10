#include <stdio.h>

int main() {
    char nombreArchivo[100];
    FILE *archivo;
    int contadorLineas = 0;
    char caracter;

    // Solicita al usuario el nombre del archivo
    printf("Ingrese el nombre del archivo: ");
    scanf("%s", nombreArchivo);

    // Abre el archivo en modo lectura
    archivo = fopen(nombreArchivo, "r");

    // Verifica si el archivo se abrió correctamente
    if (archivo == NULL) {
        printf("No se pudo abrir el archivo.\n");
        return 1;  // Salir del programa con código de error
    }

    // Lee el archivo caracter por caracter y cuenta las líneas
    while ((caracter = fgetc(archivo)) != EOF) {
        if (caracter == '\n') {
            contadorLineas++;
        }
    }

    // Cierra el archivo
    fclose(archivo);

    // Muestra el número de líneas contadas
    printf("El archivo tiene %d líneas.\n", contadorLineas);

    return 0;
}

