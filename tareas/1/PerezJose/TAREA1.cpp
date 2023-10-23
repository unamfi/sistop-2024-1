#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>
#include <time.h>

#define NUM_GATOS 3
#define NUM_RATONES 5

sem_t platos_comida;
sem_t gato_puede_comer;
sem_t raton_puede_comer;

void *raton(void *arg) {
    int id = *((int *)arg);
    
    while (1) {
        printf("Horario de ratones: Raton %d -  sale de su escondite.\n", id);
        sem_wait(&raton_puede_comer);
        printf("Raton %d: encuentra un plato y come.\n", id);
        sleep(1); // Simula el tiempo de comida
        sem_post(&platos_comida);
        sem_post(&gato_puede_comer); // Cambio de turno a los gatos
    }

    free(arg);
    return NULL;
}

void *gato(void *arg) {
    int id = *((int *)arg);
    
    while (1) {
        printf("Horario de gatos:   Gato %d -  Esta patrullando.\n", id);

        int accion = rand() % 5;
        if (accion == 0) {
            printf("Horario de gatos:   Gato %d -  ve a un raton fuera de su horario y se lo come!\n", id);
            printf("GUNNAR:excelente gato haz hecho un buen trabajo.\n");
            sem_wait(&platos_comida);
            sem_post(&gato_puede_comer);
        } else if (accion == 1) {
            printf("Horario de gatos:   Gato %d -  se queda dormido.\n", id);
        } else if (accion == 2) {
        	sem_wait(&platos_comida);
            sem_post(&gato_puede_comer);
            printf("Horario de gatos:   Gato %d -  come de un plato.\n", id);
            printf("Horario de gatos:   Gato %d -  nota a un raton comiendo del plato de alado.\n", id);
            printf("Horario de gatos:   Gato %d -  se come al raton.\n", id);
        } else {
            sem_wait(&platos_comida);
            sem_post(&gato_puede_comer);
            printf("Horario de gatos:   Gato %d -  come de un plato.\n", id);
            sleep(1); // Simula el tiempo de comida
            sem_post(&platos_comida);
            sem_post(&raton_puede_comer); // Cambio de turno a los ratones
        }

        usleep(500000); // Pequeña pausa entre acciones
    }

    free(arg);
    return NULL;
}

int main() {
    srand(time(NULL));
    sem_init(&platos_comida, 0, 1);
    sem_init(&gato_puede_comer, 0, 0);
    sem_init(&raton_puede_comer, 0, NUM_GATOS);

    pthread_t gatos[NUM_GATOS];
    pthread_t ratones[NUM_RATONES];

    for (int i = 0; i < NUM_GATOS; i++) {
        int *id = (int *)malloc(sizeof(int));
        *id = i + 1;
        pthread_create(&gatos[i], NULL, gato, id);
    }

    for (int i = 0; i < NUM_RATONES; i++) {
        int *id = (int *)malloc(sizeof(int));
        *id = i + 1;
        pthread_create(&ratones[i], NULL, raton, id);
        sem_post(&raton_puede_comer); // Inicialmente, los ratones pueden comer
    }

    // El ciclo infinito se maneja aquí
    while (1) {
        // Este espacio está en blanco a propósito, el ciclo continúa infinitamente
    }
    // Nunca se llega a esta parte ya que en teoria este jercicio seria de manera infinita, por lo que la destrucción de los semáforos no se realiza
    //pero si se quiere algo controlado, se borra el ciclo infinito y se cambia por lo que queramos
    sem_destroy(&platos_comida);
    sem_destroy(&gato_puede_comer);
    sem_destroy(&raton_puede_comer);

    return 0;
}

