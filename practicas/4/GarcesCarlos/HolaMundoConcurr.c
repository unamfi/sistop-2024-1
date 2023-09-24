#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>

sem_t semaforo1, semaforo2;

void *fun_hilo1() {
	while (1){
		sem_wait(&semaforo1);
		printf("Hilo 1: ¡Hola!\n" );
		sem_post(&semaforo2);
	}
	return NULL;
}

void *fun_hilo2() {
	while (1){
		sem_wait(&semaforo2);
		printf("Hilo 2: ¡Mundo!\n" );
		sem_post(&semaforo1);
	}
	return NULL;
}

int main() {
	pthread_t hilo1, hilo2

	sem_init(&semaforo1, 0, 1); //disponible
	sem_init(&semaforo2, 0, 0); //bloqueado

	//creacion de hilos
	pthread_create(&hilo1, NULL, fun_hilo1, NULL);
	pthread_create(&hilo2, NULL, fun_hilo2, NULL);

	pthread_join(hilo1, NULL);
	pthread_join(hilo2, NULL);
	sem_destroy(semaforo1);
	sem_destroy(semaforo2);
	
	return 0;
}
