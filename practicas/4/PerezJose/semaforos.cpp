#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>

// Declaración de semáforos
sem_t semaforo;

// Función que simula el uso de un recurso compartido
void *proceso1(void *arg) {
    printf("Proceso 1: Esperando para acceder al recurso compartido...\n");
    sem_wait(&semaforo); // Esperar al semáforo
    printf("Proceso 1: Accediendo al recurso compartido...\n");
    // Realizar operaciones en el recurso compartido
    printf("Proceso 1: Liberando el recurso compartido...\n");
    sem_post(&semaforo); // Liberar el semáforo
    pthread_exit(NULL);
}

// Función que simula el uso del mismo recurso compartido
void *proceso2(void *arg) {
    printf("Proceso 2: Esperando para acceder al recurso compartido...\n");
    sem_wait(&semaforo); // Esperar al semáforo
    printf("Proceso 2: Accediendo al recurso compartido...\n");
    // Realizar operaciones en el recurso compartido
    printf("Proceso 2: Liberando el recurso compartido...\n");
    sem_post(&semaforo); // Liberar el semáforo
    pthread_exit(NULL);
}

int main() {
    pthread_t hilo1, hilo2;

    // Inicializar el semáforo
    sem_init(&semaforo, 0, 1); // Inicializado en 1 (recurso libre)

    // Crear los hilos
    pthread_create(&hilo1, NULL, proceso1, NULL);
    pthread_create(&hilo2, NULL, proceso2, NULL);

    // Esperar a que los hilos terminen
    pthread_join(hilo1, NULL);
    pthread_join(hilo2, NULL);

    // Destruir el semáforo
    sem_destroy(&semaforo);

    return 0;
}
