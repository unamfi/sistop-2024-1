
# Tarea 2: Comparación de planificadores

¡Hola! Este archivo Python aborda la simulación y comparación de algoritmos de planificación de procesos en un entorno computacional. El propósito principal de esta tarea es evaluar y comparar el rendimiento de diferentes algoritmos de planificación de procesos en términos de analizar el tiempo de espera de los procesos en un sistema.

## Planteamiento

Para esta tarea, se pide escribir un programa que genere múltiples cargas de datos aleatorios y compare los resultados obtenidos a lo largo de varias ejecuciones. La tarea consiste en presentar al menos cinco ejecuciones independientes del programa, lo que permitirá analizar los patrones de los resultados. Además, se solicita revisar manualmente al menos algunos de los resultados generados para confirmar su exactitud.

## Algoritmo FCFS (First-Come, First-Served)

FCFS asigna procesos a la CPU en el orden en que llegan. 
El algoritmo realiza lo siguiente: 
- Se ajusta el tiempo actual si es menor que el tiempo de llegada del primer proceso. 
- Se calcula el tiempo de inicio y finalización de cada proceso. 
- Se registran el tiempo de respuesta `T`, el tiempo de espera `E` y la proporción de tiempo de respuesta `P`.
- Se imprime el nombre del proceso multiplicado por su tiempo de ejecución.

## Algoritmo RR (Round Robin)

RR asigna procesos a la CPU en base a un quantum. 
El algoritmo se ejecuta de la siguiente manera: 
- Se usa una cola para administrar los procesos.
- Si el proceso actual tiene tiempo restante mayor que el quantum, se ejecuta por un tiempo igual al quantum y se coloca nuevamente en la cola.
- Si el proceso tiene un tiempo restante menor que el quantum, se ejecuta completamente.
- Se mide el tiempo de espera promedio.
- Se registran métricas de tiempo y se imprime el nombre del proceso multiplicado por su tiempo de ejecución.

## Algoritmo SPN (Shortest Process Next) 

SPN selecciona el proceso más corto para ejecutar a continuación.
El algoritmo realiza lo siguiente: 
- Se ordenan los procesos por tiempo de ejecución y tiempo de llegada.
- Se calcula el tiempo de inicio y finalización de cada proceso.
- Se registran el tiempo de respuesta `T`, el tiempo de espera `E` y la proporción de tiempo de respuesta `P`.
- Se imprime el nombre del proceso multiplicado por su tiempo de ejecución.

## Definición de Procesos 

Se definen varios procesos con sus respectivos nombres, tiempos de llegada y tiempos de ejecución. Estos procesos se utilizan para evaluar el rendimiento de los algoritmos de planificación. 

## Ejecución de Algoritmos 

Los algoritmos FCFS, RR1 (Round Robin con quantum 1), RR4 (Round Robin con quantum 4) y SPN se ejecutan con listas de procesos. Se muestran resultados en términos de tiempo de respuesta `T`, tiempo de espera `E` y proporción de tiempo de respuesta `P`. Finalmente, se presentan los resultados de la primera y segunda ronda de procesos, junto con el tiempo total de ejecución. Además, el programa se pausa durante 15 segundos y se limpia la pantalla (utilizando 'cls' en sistemas Windows) para una mejor visualización.

## Requisitos

¿Deseas ejecutar este programa y su simulación en tu computadora? A continuación, se detallan los pasos para ejecutar el programa. 

1. **Python**: Asegúrate de tener Python instalado en tu computadora. En efecto, este código está diseñado para funcionar con Python 3. Si aún no tienes Python instalado, no te preocupes. Puedes descargarlo desde el [sitio web oficial de Python](https://www.python.org/downloads/).

### Ejecución

1. **Descarga**: Puedes obtener el código de dos maneras copiando y pegando el código en un archivo de Python con extensión `.py`, o descargando el archivo `planificadores.py` que se adjunta.

2. **Ejecución en la terminal**: Para ejecutar el programa, abre una terminal o línea de comandos en tu computadora. Luego, navega al directorio donde se encuentra el archivo de código.

3. **Iniciar el programa**: Utiliza alguna de las siguientes opciones para iniciar la ejecución del programa.

Escribe simplemente el nombre del programa y teclea `enter`:

   ```
   planificadores.py
   ```

Escribe `py`, el nombre del programa y teclea `enter`:

 ```
py planificadores.py
 ```
Escribe `python`, el nombre del programa y teclea `enter`:

 ```
python planificadores.py
 ```

- **Ejecución desde una IDE**: Además de la ejecución en la terminal, también puedes ejecutar el programa directamente desde un Entorno de Desarrollo Integrado (IDE) como PyCharm, Visual Studio Code u otro IDE de Python de tu elección. Abre el archivo en la IDE y utiliza la opción de ejecución o depuración proporcionada por la misma IDE para iniciar el programa.
---

> Realizado por:
> - Hernández Ortiz Jonathan Emmanuel.
> - Pérez Avin Paola Celina de Jesús.


