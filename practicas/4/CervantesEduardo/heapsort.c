
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdbool.h>
#include <iso646.h>
#define NUM_ELEMS 5000
#define PRINTE 50

size_t g_comparaciones = 0;

void print ( int* list, size_t tam, char* msg )
{
	printf ( "%s", msg );
	for ( size_t i = 0; i < tam; ++i ){
		printf ( "%d, ", list[ i ] );
	}
	printf ( "\n" );
}

void swap ( int* val1, int* val2 )
{
    int aux = *val1;
    *val1 = *val2;
    *val2 = aux;
}

/**
 * @brief Mantiene el heap.
 *
 * @param list[] Una lista
 * @param n El número total de elementos en la lista
 * @param k El nivel del nodo raíz (0 para el primer nivel, 1, para el segundo
 * nivel, y así sucesivamente.)
 */
void heapify ( int list[], size_t n, size_t root )
{
    size_t left = (root * 2) + 1;
    size_t right = (root * 2) + 2;
    size_t largest = root;

    g_comparaciones++;
    if ( (left < n) && (list [left] > list [root]) ){
        largest = left;
    }

    g_comparaciones++;
    if ( (right < n) && (list [right] > list [largest]) ){
        largest = right;
    }

    g_comparaciones++;
    if (largest != root){
        swap (&list [root], &list[largest]);
        heapify (list, n, largest);
    }
}

/**
 * @brief Convierte una lista de números en un montículo.
 *
 * @param list[] Una lista.
 * @param num_elems El número de elementos totales en la lista.
 *
 * @post El montículo se ve reflejado en la lista original.
 */
void build_max_heap ( int list[], size_t num_elems )
{
    for ( size_t root = (num_elems / 2); root > 0; root-- ){
        heapify (list, num_elems, root - 1);
    }
}

/**
 * @brief Ordena una lista de números utilizando al algoritmo heap sort en forma
 * ascendente.
 *
 * @param list[] Una lista.
 * @param num_elems El número de elementos totales en la lista.
 */
void heap_sort ( int list[], size_t num_elems )
{
    build_max_heap (list, num_elems);

    for ( size_t i = num_elems; i > 1; i--){
        swap ( &list [0], &list [i-1]);
        heapify (list, i - 1, 0);
    }
}

int main()
{
	srand (time(NULL));

	int list [ NUM_ELEMS ];

	for (size_t i = 0; i < NUM_ELEMS; i++){
		list [i] = -100 + rand () %500;
	}

	print ( list, PRINTE, "Antes: " );

    g_comparaciones = 0;
	heap_sort ( list, NUM_ELEMS );

	print ( list, PRINTE, "Despues: " );

    printf( "Se realizaron %ld comparaciones.\n", g_comparaciones );
    system("pause");

}
