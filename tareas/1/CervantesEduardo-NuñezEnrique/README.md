# Tarea 1: Intersección de caminos
		
		Alumnos: Cervantes García Eduardo
				 Nuñez Rodas Abraham Enrique

En este archivo se explica nuestro programa, el cual es una simulación del problema de "Intersección de caminos". Se escogió este programa porque para los dos integrantes del equipo nos pareció retador. El propósito de nuestra simulación más que recrear el programa, es presentar un escenario en el que se resuelve ligeramente refinada, es decir, en nivel 1.

## Planteamiento del problema

Si bien el planteamiento o el problema tal cual se encuentra en una presentación en la plataforma del profesor. En esta sección se presentará nuestro planteamiento para resolver el problema. La manera en que se realizó la abstracción para su realización.

- **Mapeo**: se siguió la ilustración provista por el profesor en la diaposotiva, mediante ella se acordó que cada carril sería designado por un número, de esta manera sabríamos en que carril esta cada carro y que no ocurran cambios de carril. Cada carril sería representado por una variable entera en el código.

- **Intersección**: Se identificó la intersección como la sección crítica. Se dividió como se observa en la imagen, en cuatro cuadrantes. Para designar el número de cuadrantes se tomo en cuenta el número de carril que puede acceder primero a cada intersección y se le asigno el número del carril respetivamente a cada intersección. Además, cada cuadrante sería representado por una lista en el código.

- **Autos**: de manera muy natural, se llegó a la conclusión de que cada carro sería un hilo.

De esta manera, pensamos, recordamos y probamos lo necesario para ejecutar un modelo en el que los hilos tenían que escribir en ciertos cuadrantes según el carril por el que fueran e implementamos semáforos y un patrón multiplex para que esto fuera posible de manera sincronizada, sin afectar la información y evitando en la medida de lo posible la inanición de algún hilo.

## Lenguaje y entorno de desarrollo

El programa fue escrito en el lenguaje de alto nivel Python, en su versión 3 y en el editor de texto Visual Studio Code. Se decidió la utlilización de python debido a que es un lenguaje que esta vigente en la cabeza de los dos integrantes, también fue un factor influyente que muchos ejemplos resueltos en clase fueron hechos en este mismo lenguaje. Se escogió Visual Studio Code como preferencia del equipo.

- **Requisitos**: Necesita alguna computadora con sistema operativo Linux o Windows, un editor de texto y el inteprete de Python en su versión 3.

-En el caso de Linux(distribuciones basadas en debian) la mayoría de distribuciones tienen instalado el interprete de Python en su versión 3, para evitar cualquie problema puede usar los siguientes comandos en terminal:

	$ sudo apt get update
	$ sudo apt get upgrade

Si no tiene instalado el interprete en Linux, basta con escribir en terminal el comando:

	$ sudo apt install Python

-Si tiene windows puede dirigirse a [Python3](https://www.python.org/downloads/) y descargar el ejecutable, después seguir el instalador y estará correctamente instalado el interprete de python.

-Para el editor de texto puede usar el que esta por defecto en cualquier instalación de windows, o el de su preferencia, también algún entorno de desarrollo. Para Linux aplican las misma recomendaciones, siendo lo más común que pueda abrir el archivo de código en vim o neovim ya que suelen estar por defecto en muchas distribuciones.

- **Ejecución del programa**: para ejecutar el programa basta con que vaya a powershell en windows o a la terminal de su distribución en linux, mediante comandos deberá dirigirse al directorio donde el repositorio tiene guardado el archivo de la tarea. Estando en el directorio de la tarea, en la terminal, deberá ejecutar el siguiente comando:
	
	$ python3 Interseccion_de_caminos.py
 
 Con eso realizará una correcta ejecución de nuestra solución al problema.

 ## Estrategia de sincronización

 Como se mencionó en el planteamiento, fueron usados semáforos. Se siguió el patrón multiplex de forma general en la sección crítica, combinado con semáforos sencillos para poder obtener un mayor refinamiento en la solución del problema. Pudimos haber utilizado un solo semáforo en toda la sección crítica y eso hubiera solucionado el problema, pero al pensar mejor la solución descrubimos que un multiplex mejoraría el tráfico en general y nos podría llevar a lograr el primer refinamiento.

 ## Refinamientos

 Se logró resolver el problema y se intentó, creemos con éxito llevar al nivel de refinamiento 1. Como se mencionó en la sección anterior, al visualizar el problema con un patrón multiplex, la implementación de un semáforo por cada arreglo, para evitar choques o proteger la escritura en los arreglos de intersección, resultó muy lógica. Esto permitió no bloquear toda la intersección, bloquearla por zonas de manera que pasarán más carros sin chocar, lo que nos llevo a disminuir la inanición, mientras que el multiplex protege la zona crítica en general y permite un buen flujo de tráfico.

 ## Notas:

 - En el código se nota mejor la disminución de la inanición si se quitan los "sleep", pero fueron puestos para poder visualizar de mejor forma como sucedía la concurrencía y que lo hiciera sin errores.

 - Creemos que el manejo de variables pudo ser mejor, ya que nos confundió un poco los límites entre las variables de las funciones y como las toman los hilos. Aunque gracias a esta tarea las variables globales o memoria compartida por los hilos, quedó mucho más claro.

 - También pudo ser mejor la división y ordenamiento de funciones, así como la limpieza. Sacrificó un poco la limpieza los comentarios agregados, pero creemos que mejoraron mucho nuestro entendimiento y pueden ayudar a alguien más a leer el código.

 - Tenemos como duda y nos gustaría entender en un futuro como se llega a la resolución del refinamiento 2.
