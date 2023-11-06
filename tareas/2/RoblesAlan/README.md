# Comparación de planificadores

**_Robles Reyes Alan_**

## Lenguaje

El programa fue desarrollado en **python** y para ejecutarlo se necesita poner lo siguiente: _"python3 tarea2.py"_

## Explicación del código [_tarea2.py_](tarea2.py)

- ### " Importación de bibliotecas "

    Se importa la biblioteca **'random'** para generar valores aleatorios.

- ### " Función fcfs "
	
	Se define la función _fcfs(processes)_ que implementa el algoritmo de planificación de "First-Come, First-Served" (FCFS). Esta función calcula el tiempo total, el tiempo promedio de retorno y el tiempo promedio de espera para una lista de procesos. La función recibe una lista de procesos como entrada.

	Dentro de _fcfs_, se inicializan tres variables para llevar un seguimiento del tiempo total, el tiempo de retorno y el tiempo de espera.

	Luego, se itera sobre la lista de procesos. Para cada proceso, se actualizan las variables según las fórmulas típicas de cálculo de tiempo total, tiempo de retorno y tiempo de espera en el algoritmo FCFS.

	La función _fcfs_ devuelve una tupla que contiene el tiempo total, el tiempo promedio de retorno y el tiempo promedio de espera.

- ### " Función rr "

	La función _rr(processes, quantum)_ implementa el algoritmo de planificación de "Round Robin" (RR) con un valor de quantum dado. Al igual que fcfs, calcula el tiempo total, el tiempo promedio de retorno y el tiempo promedio de espera. Esta función también toma una lista de procesos como entrada y el valor del quantum.

	Dentro de _rr_, se inicializan variables similares a las de _fcfs_ para llevar un seguimiento del tiempo total, el tiempo de retorno y el tiempo de espera.

	Luego, se crea una copia de la lista de procesos llamada _queue_ para simular la cola de procesos pendientes.

	Se inicia un bucle _while_ que continúa mientras haya procesos en la cola.

	En cada iteración del bucle, se toma el primer proceso de la cola (el proceso que está en la posición 0) y se verifica si su ráfaga de CPU es mayor que el quantum. Si es así, se resta el quantum de su ráfaga de CPU y se coloca de nuevo al final de la cola. Si no, se procesa completamente.

	Se actualizan las variables de tiempo de acuerdo con el proceso procesado.

	La función _rr_ devuelve una tupla con el tiempo total, el tiempo promedio de retorno y el tiempo promedio de espera.

- ### " Función spn "

	La función _spn(processes)_ implementa el algoritmo de planificación "Shortest Process Next" (SPN). Al igual que las otras dos funciones, calcula el tiempo total, el tiempo promedio de retorno y el tiempo promedio de espera para una lista de procesos.

	Dentro de _spn_, se inicializan variables similares a las de las otras funciones.

	Se crea una copia de la lista de procesos llamada _remaining_processes_, que se ordena según el tiempo de ráfaga de CPU de cada proceso en orden ascendente utilizando la función _sort_.

	Luego, se procesan los procesos en orden ascendente de ráfaga de CPU. Se actualizan las variables de tiempo de acuerdo con el proceso procesado.

	La función _spn_ devuelve una tupla con el tiempo total, el tiempo promedio de retorno y el tiempo promedio de espera.

- ### " Función run_simulation() "

	La función _run_simulation()_ ejecuta cinco simulaciones. En cada simulación, se genera una lista de procesos aleatorios con tiempos de llegada y ráfagas de CPU aleatorias. Estos procesos se agregan a una lista y se muestra su información en la pantalla.

	Luego, se calculan los tiempos utilizando las tres funciones definidas anteriormente: _fcfs_, _rr_, _spn_.

	Los resultados de las simulaciones se imprimen en la pantalla.

	Finalmente, el programa se ejecuta si el archivo se ejecuta directamente (es decir, no se importa como un módulo).