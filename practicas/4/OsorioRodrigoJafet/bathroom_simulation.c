/*Osorio Angeles Rodrigo Jafet
Realización de concurrencia de ejercicio en clase en .py*/

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <time.h>

#define NUM_THREADS 5

pthread_mutex_t bathroom_lock;

void *concurrent_function(void *thread_id) {
    int my_id = *((int *)thread_id);
    srand(time(NULL));

    for (int i = 0; i < 5; i++) {
        printf("%3d quiere entrar a la sección crítica!\n", my_id);
        pthread_mutex_lock(&bathroom_lock);
        printf("%3d entrando a la sección crítica por %d-ésima vez...\n", my_id, i);
        usleep((int)(1000000 * (rand() / (RAND_MAX + 1.0)))); // Sleep for a random time
        printf("%3d sale de la sección crítica\n", my_id);
        pthread_mutex_unlock(&bathroom_lock);
        usleep((int)(1000000 * (rand() / (RAND_MAX + 1.0)))); // Sleep for a random time
    }

    pthread_exit(NULL);
}

int main() {
    pthread_t threads[NUM_THREADS];
    int thread_ids[NUM_THREADS];

    pthread_mutex_init(&bathroom_lock, NULL);

    for (int i = 0; i < NUM_THREADS; i++) {
        thread_ids[i] = i;
        pthread_create(&threads[i], NULL, concurrent_function, (void *)&thread_ids[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    pthread_mutex_destroy(&bathroom_lock);

    return 0;
}