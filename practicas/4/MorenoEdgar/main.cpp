/*
 * Programa que simula una condición de carrera
 * Edgar Chalico
 */
#include <pthread.h>
#include <sched.h>
#include <stdio.h>
#include <thread>
#include <unistd.h>
#include <vector>

int conteo_global;
#define CONTEO_MAX 10000 // A partir de esta cantidad comienza a haber condición de carrera.

void *retirar(void *arg)
{
	pid_t tid = gettid();
	printf("(%d) Entra el hilo a la función y comienza a contar...\n", tid);
	for (int i = 0; i < CONTEO_MAX; i++)
		conteo_global++; // Incrementa el contador compartido
	return nullptr;
}

int main(int argc, char *argv[])
{
	std::vector<pthread_t> hilos;
	int conteo_hilos = std::thread::hardware_concurrency();

	printf("Utilizando %d hilos disponibles.\n", conteo_hilos);
	for (int i = 0; i < conteo_hilos; i++)
	{
		pthread_t hilo;
		pthread_create(&hilo, nullptr, retirar, nullptr);
		hilos.push_back(hilo);
	}

	for (auto const &hilo : hilos)
	{
		pthread_join(hilo, nullptr);
	}

	printf("Conteo final: %d\n", conteo_global);

	return 0;
}