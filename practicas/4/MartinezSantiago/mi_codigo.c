#include <stdio.h>
#include <time.h>

int main() {
    // Obtener la fecha y hora actual
    time_t tiempo_actual;
    struct tm *info_tiempo;
    char fecha_actual[80];

    time(&tiempo_actual);
    info_tiempo = localtime(&tiempo_actual);

    // Formatear la fecha actual
    strftime(fecha_actual, sizeof(fecha_actual), "Hola, es el dia %d del mes %m del anio %Y", info_tiempo);

    // Imprimir la fecha actual
    printf("%s\n", fecha_actual);

    return 0;
}
