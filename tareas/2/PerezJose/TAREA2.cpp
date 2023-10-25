//Perez Uribe Jose Alberto
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <limits.h>
#define NUM_PROCESOS 5
#define MAX_TIEMPO_LLEGADA 15
#define MAX_TIEMPO_RUPTURA 10

// Estructura para representar un proceso
typedef struct {
    char nombre;
    int tiempo_llegada;
    int tiempo_ruptura;
} Proceso;

// Estructura para representar los resultados de un algoritmo
typedef struct {
    double tiempo_respuesta;
    double tiempo_espera;
    double tiempo_respuesta_n;
    char orden_ejecucion[MAX_TIEMPO_LLEGADA * NUM_PROCESOS]; // Para esquema visual
} resultadoalgoritmo;

// Función para ordenar procesos por tiempo de llegada
int comparaciontiempo(const void *a, const void *b) {
    return ((Proceso*)a)->tiempo_llegada - ((Proceso*)b)->tiempo_llegada;
}

// Función para  FCFS
resultadoalgoritmo ejecFCFS(Proceso Procesos[]) {
    // Ordenar procesos por tiempo de llegada
    qsort(Procesos, NUM_PROCESOS, sizeof(Proceso), comparaciontiempo);

    int tiempo_actual = 0;
    resultadoalgoritmo resultado = {0.0, 0.0, 0.0, ""};
    char secuencia_ejec[MAX_TIEMPO_LLEGADA * NUM_PROCESOS] = "";

    for (int i = 0; i < NUM_PROCESOS; i++) {
        if (Procesos[i].tiempo_llegada > tiempo_actual) {
            tiempo_actual = Procesos[i].tiempo_llegada;
        }
        for (int j = 0; j < Procesos[i].tiempo_ruptura; j++) {
            resultado.orden_ejecucion[tiempo_actual] = Procesos[i].nombre;
            strncat(secuencia_ejec, &Procesos[i].nombre, 1);
            tiempo_actual++;
        }
    }

    // Calcular tiempo de vuelta y tiempo de espera
    int total_tiempovuelta = 0;
    int total_espera = 0;
    for (int i = 0; i < NUM_PROCESOS; i++) {
        int ciclo = tiempo_actual - Procesos[i].tiempo_llegada;
        total_tiempovuelta += ciclo;
        total_espera += ciclo - Procesos[i].tiempo_ruptura;
    }

    resultado.tiempo_respuesta = (double)total_tiempovuelta / NUM_PROCESOS;
    resultado.tiempo_espera = (double)total_espera / NUM_PROCESOS;
    resultado.tiempo_respuesta_n = resultado.tiempo_respuesta / resultado.tiempo_espera;
    strcpy(resultado.orden_ejecucion, secuencia_ejec);

    return resultado;
}

// Función para RR
resultadoalgoritmo ejecRR(Proceso Procesos[], int tiempo_c) {
    // Ordenar procesos por tiempo de llegada
    qsort(Procesos, NUM_PROCESOS, sizeof(Proceso), comparaciontiempo);

    int tiempo_actual = 0;
    resultadoalgoritmo resultado = {0.0, 0.0, 0.0, ""};
    char secuencia_ejec[MAX_TIEMPO_LLEGADA * NUM_PROCESOS] = "";

    int tiempo_restante[NUM_PROCESOS];
    for (int i = 0; i < NUM_PROCESOS; i++) {
        tiempo_restante[i] = Procesos[i].tiempo_ruptura;
    }

    int done = 0; // Variable para rastrear si todos los procesos han terminado
    while (!done) {
        done = 1;
        for (int i = 0; i < NUM_PROCESOS; i++) {
            if (tiempo_restante[i] > 0) {
                done = 0; // Al menos un proceso sigue en ejecución
                int corte_tiempo = (tiempo_restante[i] > tiempo_c) ? tiempo_c : tiempo_restante[i];
                for (int j = 0; j < corte_tiempo; j++) {
                    resultado.orden_ejecucion[tiempo_actual] = Procesos[i].nombre;
                    strncat(secuencia_ejec, &Procesos[i].nombre, 1);
                    tiempo_actual++;
                }
                tiempo_restante[i] -= corte_tiempo;
            }
        }
    }

    // Calcular turnaround time y waiting time
    for (int i = 0; i < NUM_PROCESOS; i++) {
        int ciclo = tiempo_actual - Procesos[i].tiempo_llegada;
        resultado.tiempo_respuesta += ciclo;
        resultado.tiempo_espera += ciclo  - Procesos[i].tiempo_ruptura;
    }

    resultado.tiempo_respuesta /= NUM_PROCESOS;
    resultado.tiempo_espera /= NUM_PROCESOS;
    resultado.tiempo_respuesta_n = resultado.tiempo_respuesta / resultado.tiempo_espera;
    strcpy(resultado.orden_ejecucion, secuencia_ejec);

    return resultado;
}

// Función para simular el planificador SPN
resultadoalgoritmo ejecSPN(Proceso Procesos[]) {
    // Ordenar procesos por tiempo de llegada
    qsort(Procesos, NUM_PROCESOS, sizeof(Proceso), comparaciontiempo);

    int tiempo_actual = 0;
    resultadoalgoritmo resultado = {0.0, 0.0, 0.0, ""};
    char secuencia_ejec[MAX_TIEMPO_LLEGADA * NUM_PROCESOS] = "";

    int tiempo_restante[NUM_PROCESOS];

    for (int i = 0; i < NUM_PROCESOS; i++) {
        tiempo_restante[i] = Procesos[i].tiempo_ruptura;
    }

    int completado = 0;
    while (completado < NUM_PROCESOS) {
        int ruptura_min = INT_MAX;
        int siguiente_proceso = -1;

        for (int i = 0; i < NUM_PROCESOS; i++) {
            if (Procesos[i].tiempo_llegada <= tiempo_actual && tiempo_restante[i] < ruptura_min && tiempo_restante[i] > 0) {
                ruptura_min = tiempo_restante[i];
                siguiente_proceso = i;
            }
        }

        if (siguiente_proceso == -1) {
            tiempo_actual++;
        } else {
            char sig_proceso_n = Procesos[siguiente_proceso].nombre;
            for (int j = 0; j < Procesos[siguiente_proceso].tiempo_ruptura; j++) {
                resultado.orden_ejecucion[tiempo_actual] = sig_proceso_n;
                strncat(secuencia_ejec, &sig_proceso_n, 1);
                tiempo_actual++;
            }
            tiempo_restante[siguiente_proceso] = 0;
            completado++;
        }
    }

    // Calcular turnaround time y waiting time
    for (int i = 0; i < NUM_PROCESOS; i++) {
        int ciclo = tiempo_actual - Procesos[i].tiempo_llegada;
        resultado.tiempo_respuesta += ciclo;
        resultado.tiempo_espera += ciclo - Procesos[i].tiempo_ruptura;
    }

    resultado.tiempo_respuesta /= NUM_PROCESOS;
    resultado.tiempo_espera /= NUM_PROCESOS;
    resultado.tiempo_respuesta_n = resultado.tiempo_respuesta / resultado.tiempo_espera;
    strcpy(resultado.orden_ejecucion, secuencia_ejec);

    return resultado;
}

int main() {
    srand(time(NULL));
    int ronda = 1;
    char input;
    do {
        printf("Presiona Enter para ejecutar el programa o 'x' para salir: ");
        input = getchar();
        if (input == 'x') {
            break; // Salir del bucle si el usuario ingresa 'x'
        }

        Proceso Procesos[NUM_PROCESOS];
        for (int i = 0; i < NUM_PROCESOS; i++) {
            Procesos[i].nombre = 'A' + i;
            Procesos[i].tiempo_llegada = rand() % (MAX_TIEMPO_LLEGADA + 1);
            Procesos[i].tiempo_ruptura = 1 + rand() % MAX_TIEMPO_RUPTURA;
        }

        // Simular los algoritmos y obtener resultados
        resultadoalgoritmo fcfs_resultado = ejecFCFS(Procesos);
        resultadoalgoritmo rr1_resultado = ejecRR(Procesos, 1);
        resultadoalgoritmo rr4_resultado = ejecRR(Procesos, 4);
        resultadoalgoritmo spn_resultado = ejecSPN(Procesos);

        // Imprimir los resultados en el formato requerido
        printf("Ronda %d:\n", ronda);
        int tiempo_total_prim = 0; 

        for (int i = 0; i < NUM_PROCESOS; i++) {
            printf(" %c:%d, t=%d;", Procesos[i].nombre, Procesos[i].tiempo_llegada, Procesos[i].tiempo_ruptura);
            tiempo_total_prim += Procesos[i].tiempo_ruptura;
        }
        printf("\n");
        printf("  (tot:%d)\n", tiempo_total_prim); 

        printf("  FCFS: T=%.1lf, E=%.1lf, P=%.2lf\n", fcfs_resultado.tiempo_respuesta, fcfs_resultado.tiempo_espera,
               fcfs_resultado.tiempo_respuesta_n);
        printf("  %s\n", fcfs_resultado.orden_ejecucion);

        printf("  RR1: T=%.1lf, E=%.1lf, P=%.2lf\n", rr1_resultado.tiempo_respuesta, rr1_resultado.tiempo_espera,
               rr1_resultado.tiempo_respuesta_n);
        printf("  %s\n", rr1_resultado.orden_ejecucion);

        printf("  RR4: T=%.1lf, E=%.1lf, P=%.2lf\n", rr4_resultado.tiempo_respuesta, rr4_resultado.tiempo_espera,
               rr4_resultado.tiempo_respuesta_n);
        printf("  %s\n", rr4_resultado.orden_ejecucion);

        printf("  SPN: T=%.1lf, E=%.1lf, P=%.2lf\n", spn_resultado.tiempo_respuesta, spn_resultado.tiempo_espera,
               spn_resultado.tiempo_respuesta_n);
        printf("  %s\n", spn_resultado.orden_ejecucion);

        while (getchar() != '\n');
        ronda++;
    } while (input != 'q');
    return 0;
}

