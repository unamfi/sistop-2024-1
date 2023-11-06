# Tarea 2: Planificadores de procesos
		
		Cervantes García Eduardo
				 

En este archivo se explica el  programa realizado, el cual simula los algoritmos de planificación estudiados más sencillos. Con el fin de entender de mejor manera el planificador y cada algoritmo, así como realizar pruebas similares a las que realizó Finkel.

## Planteamiento del problema

Para la realización de este programa, más que como un programa que calcula los valores que obtendría cada algoritmo según una carga de procesos, el programa se planteo como una simulación u aproximado del funcionamiento de los planificadores con los procesos. Es decir, mediante un arreglo de tuplas se representó la creación de procesos aleatorios llegando al sistema, con ejecución desconocida para dos de los algoritmos y tiempo de llegada aleatorio. Cada algoritmo realizado, recibe el arreglo de procesos y lo procesa como si los procesos pasaran por las estrcuturas de datos del sistema operativo mediante los algoritmos que son el objetivo de esta tarea. Con la simulación realizada para cada algoritmo se obtienen métricas o datos, sobre todo el tiempo de respuesta de cada proceso, en cada algoritmo, con el cual se calculan los demás datos de la ronda de ejecución en cada algoritmo y se presentan como se verá en la ejecución.

-Para entender el orden y los datos del arreglo de tuplas, es necesario leer las notas que se encuentran más abajo.

## Ejecución del programa
Los siguientes dos ejemplos son dos ejecuciones de cinco rondas del programa, donde se pueden obsevar las tablas con los datos para cada algoritmo.

### Ejecución 1:
								----RONDA 0----

	Estas son las cargas de la prueba de la ronda:
	[('A', 12, 0), ('B', 9, 5), ('C', 11, 1), ('D', 9, 7), ('E', 9, 18), ('F', 11, 39)]


							---FCFS---
	Proceso:        T:      E:      P:
	A               12      0       1
	C               22      11      2
	B               27      18      3
	D               34      25      3
	E               32      23      3
	F               22      11      2

	Promedios:      T:24.833333     E:14.666667     P:2.555556

	Gráfico de la corrida:

	deque(['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F'])
							---ROUND ROBIN---
	Proceso:        T:      E:      P:
	A               32      20      2
	C               42      31      3
	B               41      32      4
	D               42      33      4
	E               36      27      4
	F               22      11      2

	Promedios:      T:35.833333     E:25.666667     P:3.617845

	Gráfico de la corrida:

	['A', 'A', 'A', 'A', 'C', 'C', 'A', 'A', 'C', 'C', 'B', 'B', 'A', 'A', 'D', 'D', 'C', 'C', 'B', 'B', 'A', 'A', 'D', 'D', 'C', 'C', 'E', 'E', 'B', 'B', 'A', 'A', 'D', 'D', 'C', 'C', 'E', 'E', 'B', 'B', 'D', 'D', 'C', 'E', 'E', 'B', 'F', 'F', 'D', 'E', 'E', 'F', 'F', 'E', 'F', 'F', 'F', 'F', 'F', 'F', 'F']
							---SPN---
	Proceso:        T:      E:      P:
	A               12      0       1
	C               60      49      5
	B               34      25      3
	D               14      5       1
	E               12      3       1
	F               11      0       1

	Promedios:      T:23.833333     E:13.666667     P:2.353535

	Gráfico de la corrida:

	deque(['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C'])
	----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
							----RONDA 1----

	Estas son las cargas de la prueba de la ronda:
	[('A', 13, 0), ('B', 1, 13), ('C', 1, 6), ('D', 13, 5)]


							---FCFS---
	Proceso:        T:      E:      P:
	A               13      0       1
	D               21      8       1
	C               21      20      21
	B               15      14      15

	Promedios:      T:17.500000     E:10.500000     P:9.653846

	Gráfico de la corrida:

	deque(['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'B'])
							---ROUND ROBIN---
	Proceso:        T:      E:      P:
	A               21      8       1
	D               23      10      1
	C               5       4       5
	B               5       4       5

	Promedios:      T:13.500000     E:6.500000      P:3.346154

	Gráfico de la corrida:

	['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'D', 'D', 'C', 'A', 'A', 'D', 'D', 'A', 'A', 'B', 'D', 'D', 'A', 'D', 'D', 'D', 'D', 'D', 'D', 'D']
							---SPN---
	Proceso:        T:      E:      P:
	A               13      0       1
	D               23      10      1
	C               9       8       9
	B               1       0       1

	Promedios:      T:11.500000     E:4.500000      P:3.192308

	Gráfico de la corrida:

	deque(['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'C', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D'])
	----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
							----RONDA 2----

	Estas son las cargas de la prueba de la ronda:
	[('A', 12, 0), ('B', 5, 7), ('C', 14, 11), ('D', 2, 29), ('E', 14, 10), ('F', 5, 3)]


							---FCFS---
	Proceso:        T:      E:      P:
	A               12      0       1
	F               14      9       2
	B               15      10      3
	E               26      12      1
	C               39      25      2
	D               23      21      11

	Promedios:      T:21.500000     E:12.833333     P:3.823810

	Gráfico de la corrida:

	deque(['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'F', 'F', 'F', 'F', 'F', 'B', 'B', 'B', 'B', 'B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'D', 'D'])
							---ROUND ROBIN---
	Proceso:        T:      E:      P:
	A               25      13      2
	F               16      11      3
	B               23      18      4
	E               40      26      2
	C               41      27      2
	D               7       5       3

	Promedios:      T:25.333333     E:16.666667     P:3.194841

	Gráfico de la corrida:

	['A', 'A', 'A', 'A', 'A', 'A', 'F', 'F', 'A', 'A', 'F', 'F', 'B', 'B', 'A', 'A', 'E', 'E', 'F', 'C', 'C', 'B', 'B', 'A', 'A', 'E', 'E', 'C', 'C', 'B', 'E', 'E', 'C', 'C', 'D', 'D', 'E', 'E', 'C', 'C', 'E', 'E', 'C', 'C', 'E', 'E', 'C', 'C', 'E', 'E', 'C', 'C']
							---SPN---
	Proceso:        T:      E:      P:
	A               12      0       1
	F               49      44      9
	B               24      19      4
	E               37      23      2
	C               15      1       1
	D               4       2       2

	Promedios:      T:23.500000     E:14.833333     P:3.552381

	Gráfico de la corrida:

	deque(['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'B', 'B', 'B', 'B', 'B', 'D', 'D', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'F', 'F', 'F', 'F', 'F'])
	----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
							----RONDA 3----

	Estas son las cargas de la prueba de la ronda:
	[('A', 13, 0), ('B', 7, 1), ('C', 12, 16), ('D', 10, 29)]


							---FCFS---
	Proceso:        T:      E:      P:
	A               13      0       1
	B               19      12      2
	C               16      4       1
	D               13      3       1

	Promedios:      T:15.250000     E:4.750000      P:1.586905

	Gráfico de la corrida:

	deque(['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D'])
							---ROUND ROBIN---
	Proceso:        T:      E:      P:
	A               22      9       1
	B               16      9       2
	C               16      4       1
	D               13      3       1

	Promedios:      T:16.750000     E:6.250000      P:1.652839

	Gráfico de la corrida:

	['A', 'A', 'A', 'A', 'B', 'B', 'A', 'A', 'B', 'B', 'A', 'A', 'B', 'B', 'A', 'A', 'B', 'A', 'A', 'C', 'C', 'A', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D']
							---SPN---
	Proceso:        T:      E:      P:
	A               13      0       1
	B               19      12      2
	C               16      4       1
	D               13      3       1

	Promedios:      T:15.250000     E:4.750000      P:1.586905

	Gráfico de la corrida:

	deque(['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D'])
	----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
							----RONDA 4----

	Estas son las cargas de la prueba de la ronda:
	[('A', 14, 0), ('B', 6, 8), ('C', 3, 1), ('D', 10, 8), ('E', 14, 3)]


							---FCFS---
	Proceso:        T:      E:      P:
	A               14      0       1
	C               16      13      5
	E               28      14      2
	B               29      23      4
	D               39      29      3

	Promedios:      T:25.200000     E:15.800000     P:3.413333

	Gráfico de la corrida:

	deque(['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'C', 'C', 'C', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B', 'B', 'B', 'B', 'B', 'B', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D'])
							---ROUND ROBIN---
	Proceso:        T:      E:      P:
	A               37      23      2
	C               10      7       3
	E               44      30      3
	B               23      17      3
	D               35      25      3

	Promedios:      T:29.800000     E:20.400000     P:3.290476

	Gráfico de la corrida:

	['A', 'A', 'A', 'A', 'C', 'C', 'A', 'A', 'E', 'E', 'C', 'A', 'A', 'B', 'B', 'D', 'D', 'E', 'E', 'A', 'A', 'B', 'B', 'D', 'D', 'E', 'E', 'A', 'A', 'B', 'B', 'D', 'D', 'E', 'E', 'A', 'A', 'D', 'D', 'E', 'E', 'D', 'D', 'E', 'E', 'E', 'E']
							---SPN---
	Proceso:        T:      E:      P:
	A               14      0       1
	C               32      29      10
	E               44      30      3
	B               12      6       2
	D               22      12      2

	Promedios:      T:24.800000     E:15.400000     P:3.801905

	Gráfico de la corrida:

	deque(['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'B', 'B', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'C', 'C', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'])
	----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Ejecución 2:

								----RONDA 0----

	Estas son las cargas de la prueba de la ronda:
	[('A', 11, 0), ('B', 10, 6), ('C', 14, 16), ('D', 4, 26), ('E', 11, 5)]


							---FCFS---
	Proceso:        T:      E:      P:
	A               11      0       1
	E               17      6       1
	B               26      16      2
	C               30      16      2
	D               24      20      6

	Promedios:      T:21.600000     E:11.600000     P:2.657662

	Gráfico de la corrida:

	deque(['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'D', 'D', 'D', 'D'])
							---ROUND ROBIN---
	Proceso:        T:      E:      P:
	A               19      8       1
	E               35      24      3
	B               33      23      3
	C               34      20      2
	D               16      12      4

	Promedios:      T:27.400000     E:17.400000     P:2.927532

	Gráfico de la corrida:

	['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'E', 'E', 'B', 'B', 'A', 'A', 'E', 'E', 'B', 'B', 'A', 'E', 'E', 'C', 'C', 'B', 'B', 'E', 'E', 'C', 'C', 'B', 'B', 'E', 'E', 'D', 'D', 'C', 'C', 'B', 'B', 'E', 'D', 'D', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C']
							---SPN---
	Proceso:        T:      E:      P:
	A               11      0       1
	E               45      34      4
	B               15      5       1
	C               19      5       1
	D               13      9       3

	Promedios:      T:20.600000     E:10.600000     P:2.239610

	Gráfico de la corrida:

	deque(['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'D', 'D', 'D', 'D', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'])
	----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
							----RONDA 1----

	Estas son las cargas de la prueba de la ronda:
	[('A', 11, 0), ('B', 15, 10), ('C', 11, 4), ('D', 3, 24), ('E', 8, 16)]


							---FCFS---
	Proceso:        T:      E:      P:
	A               11      0       1
	C               18      7       1
	B               27      12      1
	E               29      21      3
	D               24      21      8

	Promedios:      T:21.800000     E:12.200000     P:3.212273

	Gráfico de la corrida:

	deque(['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'D', 'D', 'D'])
							---ROUND ROBIN---
	Proceso:        T:      E:      P:
	A               19      8       1
	C               34      23      3
	B               38      23      2
	E               27      19      3
	D               15      12      5

	Promedios:      T:26.600000     E:17.000000     P:3.145303

	Gráfico de la corrida:

	['A', 'A', 'A', 'A', 'A', 'A', 'C', 'C', 'A', 'A', 'C', 'C', 'A', 'A', 'B', 'B', 'C', 'C', 'A', 'B', 'B', 'E', 'E', 'C', 'C', 'B', 'B', 'E', 'E', 'C', 'C', 'D', 'D', 'B', 'B', 'E', 'E', 'C', 'D', 'B', 'B', 'E', 'E', 'B', 'B', 'B', 'B', 'B']
							---SPN---
	Proceso:        T:      E:      P:
	A               11      0       1
	C               18      7       1
	B               38      23      2
	E               14      6       1
	D               9       6       3

	Promedios:      T:18.000000     E:8.400000      P:1.983939

	Gráfico de la corrida:

	deque(['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'D', 'D', 'D', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'])
	----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
							----RONDA 2----

	Estas son las cargas de la prueba de la ronda:
	[('A', 7, 0), ('B', 1, 3), ('C', 10, 6), ('D', 12, 5), ('E', 12, 10), ('F', 4, 11)]


							---FCFS---
	Proceso:        T:      E:      P:
	A               7       0       1
	B               5       4       5
	D               15      3       1
	C               24      14      2
	E               32      20      2
	F               35      31      8

	Promedios:      T:19.666667     E:12.000000     P:3.511111

	Gráfico de la corrida:

	deque(['A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'F', 'F', 'F', 'F'])
							---ROUND ROBIN---
	Proceso:        T:      E:      P:
	A               8       1       1
	B               4       3       4
	D               37      25      3
	C               34      24      3
	E               36      24      3
	F               17      13      4

	Promedios:      T:22.666667     E:15.000000     P:3.146032

	Gráfico de la corrida:

	['A', 'A', 'A', 'A', 'A', 'A', 'B', 'A', 'D', 'D', 'C', 'C', 'D', 'D', 'E', 'E', 'C', 'C', 'F', 'F', 'D', 'D', 'E', 'E', 'C', 'C', 'F', 'F', 'D', 'D', 'E', 'E', 'C', 'C', 'D', 'D', 'E', 'E', 'C', 'C', 'D', 'D', 'E', 'E', 'E', 'E']
							---SPN---
	Proceso:        T:      E:      P:
	A               7       0       1
	B               31      30      31
	D               41      29      3
	C               11      1       1
	E               23      11      1
	F               10      6       2

	Promedios:      T:20.500000     E:12.833333     P:6.822222

	Gráfico de la corrida:

	deque(['A', 'A', 'A', 'A', 'A', 'A', 'A', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'F', 'F', 'F', 'F', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D'])
	----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
							----RONDA 3----

	Estas son las cargas de la prueba de la ronda:
	[('A', 3, 0), ('B', 6, 3), ('C', 5, 8), ('D', 6, 14), ('E', 14, 1)]


							---FCFS---
	Proceso:        T:      E:      P:
	A               3       0       1
	E               16      2       1
	B               20      14      3
	C               20      15      4
	D               20      14      3

	Promedios:      T:15.800000     E:9.000000      P:2.561905

	Gráfico de la corrida:

	deque(['A', 'A', 'A', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'B', 'B', 'B', 'B', 'B', 'B', 'C', 'C', 'C', 'C', 'C', 'D', 'D', 'D', 'D', 'D', 'D'])
							---ROUND ROBIN---
	Proceso:        T:      E:      P:
	A               3       0       1
	E               33      19      2
	B               14      8       2
	C               18      13      3
	D               18      12      3

	Promedios:      T:17.200000     E:10.400000     P:2.458095

	Gráfico de la corrida:

	['A', 'A', 'A', 'E', 'E', 'B', 'B', 'E', 'E', 'B', 'B', 'E', 'E', 'C', 'C', 'B', 'B', 'E', 'E', 'C', 'C', 'D', 'D', 'E', 'E', 'C', 'D', 'D', 'E', 'E', 'D', 'D', 'E', 'E']
							---SPN---
	Proceso:        T:      E:      P:
	A               3       0       1
	E               33      19      2
	B               6       0       1
	C               6       1       1
	D               6       0       1

	Promedios:      T:10.800000     E:4.000000      P:1.311429

	Gráfico de la corrida:

	deque(['A', 'A', 'A', 'B', 'B', 'B', 'B', 'B', 'B', 'C', 'C', 'C', 'C', 'C', 'D', 'D', 'D', 'D', 'D', 'D', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'])
	----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
							----RONDA 4----

	Estas son las cargas de la prueba de la ronda:
	[('A', 7, 0), ('B', 10, 6), ('C', 9, 9), ('D', 1, 6), ('E', 7, 16)]


							---FCFS---
	Proceso:        T:      E:      P:
	A               7       0       1
	B               11      1       1
	D               12      11      12
	C               18      9       2
	E               18      11      2

	Promedios:      T:13.200000     E:6.400000      P:3.734286

	Gráfico de la corrida:

	deque(['A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'D', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'E', 'E', 'E', 'E', 'E', 'E', 'E'])
							---ROUND ROBIN---
	Proceso:        T:      E:      P:
	A               7       0       1
	B               20      10      2
	D               4       3       4
	C               24      15      2
	E               18      11      2

	Promedios:      T:14.600000     E:7.800000      P:2.447619

	Gráfico de la corrida:

	['A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'D', 'B', 'B', 'C', 'C', 'B', 'B', 'C', 'C', 'B', 'B', 'E', 'E', 'C', 'C', 'B', 'B', 'E', 'E', 'C', 'C', 'E', 'E', 'C', 'E']
							---SPN---
	Proceso:        T:      E:      P:
	A               7       0       1
	B               12      2       1
	D               2       1       2
	C               25      16      2
	E               9       2       1

	Promedios:      T:11.000000     E:4.200000      P:1.652698

	Gráfico de la corrida:

	deque(['A', 'A', 'A', 'A', 'A', 'A', 'A', 'D', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C'])
	----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Lenguaje y entorno de desarrollo

El programa fue escrito en el lenguaje de alto nivel Python, en su versión 3 y en el editor de texto Visual Studio Code. Se decidió la utlilización de python debido a que es un lenguaje que constantemente utilizo y en el que ya tengo como una herramienta sólida el uso de algunas librerías.

- **Requisitos**: Necesita alguna computadora con sistema operativo Linux o Windows, un editor de texto y el inteprete de Python en su versión 3.

-En el caso de Linux(distribuciones basadas en debian) la mayoría de distribuciones tienen instalado el interprete de Python en su versión 3, para evitar cualquie problema puede usar los siguientes comandos en terminal:

	$ sudo apt get update
	$ sudo apt get upgrade

Si no tiene instalado el interprete en Linux, basta con escribir en terminal el comando:

	$ sudo apt install Python

-Si tiene windows puede dirigirse a [Python3](https://www.python.org/downloads/) y descargar el ejecutable, después seguir el instalador y estará correctamente instalado el interprete de python.

-Para el editor de texto puede usar el que esta por defecto en cualquier instalación de windows, o el de su preferencia, también algún entorno de desarrollo. Para Linux aplican las misma recomendaciones, siendo lo más común que pueda abrir el archivo de código en vim o neovim ya que suelen estar por defecto en muchas distribuciones.

- **Ejecución del programa**: para ejecutar el programa basta con que vaya a powershell en windows o a la terminal de su distribución en linux, mediante comandos deberá dirigirse al directorio donde el repositorio tiene guardado los archivo de la tarea, los archivos deben de estar juntos. Estando en el directorio de la tarea, en la terminal, deberá ejecutar el siguiente comando:

		$ python3 Main.py

 ## Conclusiones del programa


 Como se mencionó en el planteamiento, se intentó realizar una simulación. La simulación dió mayor entendimiento de cada algoritmo, debido a que se encontaron problemas que en lápiz y papel no son sencillos de ver. Con una perspectiva más amplia, se pudo notar que a pesar de que la lógica es sencilla, al involucrar los "procesos" e intentar simular todo, la creación del programa se volvió más compleja de lo pensado. Si bien, se cumplió con el objetivo de la tarea, el código es bastante mejorable en su lógica y en su practicidad.

 ## Posibilidades de mejora

 Existen líneas que se podrían simplificar o partes que se podrían hacer más pequeñas, lo primero con el uso de algunas librerías que no se usaron  y con el uso más inteligente de algunas funciones. El código podría ser más pequeño mejorando algunas cosas en los ciclos y analizando todas las variables, probablemente hay algunas que no son necesarias, y hay sitios donde sería mejor usar una o guardar el resultado de una operación.

 ## Notas:

 - El siguiente comentario se encuntra en el código, pero es importante para entender la lista de tuplas usada:
		'''
		Tuplas - (Nombre,número de ticks, momento de llegada)
		se usan enteros para obsevar el tiempo discreto
		Se añade a la  tupla el número de ticks del proceso para tenerlo como información en SPN
		'''
 - Existe un bug el cual no se ha podido resolver ni detectar con presición aún, en el algoritmo de ROUND ROBIN. Este bug hace que el programa de error o se para en el momento en que se presenta, no suele ser muy habitual, pero si sucede basta con volver a corre una u otra vez más el programa para que entregue una ejecución completa.
