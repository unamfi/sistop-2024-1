# Tarea 1: El elevador

¡Hola! Este archivo Markdown explica un código de simulación que implementa un sistema de ascensor con múltiples hilos en Python. ¿Con qué propósito? Pues con el propósito de proponer una solución al comportamiento de un elevador y personas que esperan en diferentes pisos.

## Planteamiento

El elevador de la Facultad se descompone demasiado, y la razón principal es que sus usuarios no respetan los límites establecidos. ¡Es momento de tomar medidas para evitar este desgaste y el peligro potencial que eso conlleva! Juntos. 

- **Hilos**: Implementa el elevador como un hilo independiente y permite que cada persona que desee utilizarlo lo haga como otro hilo separado. Esto permite un mejor control del uso del elevador, ya que cada entidad (`elevador` y `personas`) opera de manera independiente, lo que mejora la gestión y la eficiencia del sistema.

- **Pisos**: El elevador de la Facultad de Ingeniería está diseñado para dar servicio a cinco pisos distintos. Por lo tanto, es crucial cerciorarse de que la implementación evidencie este detalle, de modo que el elevador pueda atender a las necesidades de las personas en cada uno de los cinco pisos.

- **Llamadas**: Cualquier persona tiene la capacidad de llamar al elevador desde cualquiera de los cinco pisos. La flexibilidad tiene una importancia fundamental en la mejora de la eficiencia del sistema, ya que las personas al poder acceder al servicio de elevador desde cualquier ubicación, será posible agilizar el proceso y brindar cierta comodidad.

- **Destinos**: ¡Las personas pueden tener distintos destinos en mente! Por lo tanto, es esencial que el elevador sea capaz de llevar a las personas a cualquier otro piso según sus solicitudes. Esto garantiza que el sistema pueda satisfacer las necesidades de las personas de manera adecuada.

## Reglas
  
Por supuesto, para este problema hay reglas a considerar de suma importancia. 

- **Capacidad**: El elevador tiene una capacidad máxima de cinco pasajeros, lo que significa que puede llevar hasta cinco personas a la vez. Esto limita la cantidad de personas que pueden utilizar el elevador simultáneamente.

- **Recorrido**: Para ir del piso `x` al piso `y`, el elevador debe atravesar todos los pisos intermedios entre `x` y `y`. Esto asegura que el elevador atienda a todas las solicitudes de las personas que desean bajar en cualquier piso intermedio.

- **Espera**: Las personas prefieren esperar dentro del elevador en lugar de esperar fuera de él. Esta preferencia permite llenar el elevador de manera eficiente y evitar que esperen exhaustivamente en los pasillos.

- **Abordaje**: Si el elevador está subiendo y pasa por el piso `x`, donde una persona A está esperando para bajar, A puede abordar el elevador de inmediato, sin esperar a que el elevador esté yendo en la dirección correcta. Esta regla agiliza el proceso de recogida de pasajeros en el elevador.

## Sincronización

Este código utiliza una estrategia de sincronización basada en mutex (abreviatura de "mutual exclusion" o exclusión mutua) para garantizar que múltiples hilos puedan acceder de manera segura a un estado compartido, evitando condiciones de carrera y asegurando la coherencia del programa. Por ende, los mutex actúan como candados que permiten que solo un hilo a la vez acceda a secciones críticas del código.

El código emplea un mutex denominado `mutex` para controlar el acceso concurrente a dos aspectos clave:

1. **Estado del elevador**: El estado del elevador se almacena en el diccionario `estado_elevador`, que contiene información sobre el piso actual, las personas dentro del elevador y la dirección del movimiento. El acceso a este estado se sincroniza mediante el `mutex`. Cada vez que el elevador se mueve, recoge o deja personas, o cambia de dirección, se utiliza el `mutex` para garantizar que estas operaciones se realicen de manera coherente y segura.

2. **Listas de espera**: Las personas que esperan en cada piso se organizan en listas que representan su ubicación. Cuando el elevador llega a un piso, verifica si hay personas esperando y, si es necesario, permite que algunas de ellas aborden. El `mutex` también controla el acceso a estas listas, asegurando que las personas esperando se administren de manera sincronizada.

## Código

El código se divide en dos partes principales: 
- El **hilo del elevador**.
- Los **hilos de las personas** que esperan en los pisos.

A continuación, se detallan los componentes clave:

### Elevador

- Se define la capacidad del elevador (`cap_elevador`) y el número de pisos (`num_pisos`).
- El estado del elevador se almacena en un diccionario llamado `estado_elevador`, que incluye el piso actual, las personas dentro del elevador y la dirección del movimiento.
- Se utiliza debidamente un mutex (`mutex`) para sincronizar el acceso al estado compartido. El elevador se mueve de arriba a abajo y viceversa. Asimismo, recoge y deja a las personas en los pisos según corresponda.
- Por último, se simula el tiempo de viaje del elevador utilizando `time.sleep()`.

### Personas

- Cada persona se modela como un hilo separado. Las personas tienen un origen, un destino y una dirección de movimiento.
- Se utiliza el mismo mutex para controlar el acceso a las listas de personas esperando en cada piso y al estado del elevador.
- Las personas intentan subir al elevador si cumplen con ciertas condiciones (como la dirección y la capacidad).
- Si no pueden subir, esperan en su piso correspondiente y vuelven a intentar después de un tiempo.

### Inicialización

- Se inicia un hilo para el elevador (`elevador_thread`) y múltiples hilos para las personas (`persona_thread`).
- El programa se ejecuta en un bucle infinito para simular la operación continua.

## Refinamiento

Este código implementa un refinamiento que evita la inanición de las personas que esperan en diferentes pisos. La inanición se refiere a la situación en la que un conjunto de procesos o hilos siempre tiene prioridad sobre otros, lo que podría conllevar a que algunos usuarios queden excluidos indefinidamente del acceso al elevador. ¿Cómo se evita este escenario? Pues, el código incorpora un mecanismo que garantiza que todas las personas tengan la oportunidad de utilizar el elevador.

### Evitando

El código aborda la inanición de la siguiente manera:

- Si el elevador está lleno y no hay espacio para más personas en su dirección actual, las personas que desean subir en ese piso deben esperar en una lista de espera específica para ese piso.

- Cuando el elevador llega a un piso en el que haya personas esperando, verifica si hay espacio disponible y si las personas en el piso tienen la misma dirección que el elevador.

- Si se cumplen estas condiciones, el elevador permite que las personas esperando en ese piso se suban. Sin embargo, si el elevador está lleno, estas personas también se colocarán en la lista de espera y tendrán la oportunidad de abordar en posteriores paradas.

### Equidad

Este mecanismo garantiza la equidad al permitir que todas las personas esperando en diferentes pisos tengan la oportunidad de abordar el elevador. ¡Sí! Incluso si las personas que viajan entre dos pisos podrían ocuparlo en repetidas ocasiones. 

Este refinamiento en el código se cerciora de que todas las personas que esperan tengan la oportunidad de usar el elevador y que no se produzca una situación de inanición para los usuarios que viajan entre dos pisos. Consiguiéndose mediante la gestión de las listas de espera y una sincronización adecuada de los hilos establecidos.

## Requisitos

¿Deseas ejecutar este programa y su simulación en tu computadora? A continuación, se detallan los pasos para ejecutar el programa. 

1. **Python**: Asegúrate de tener Python instalado en tu computadora. En efecto, este código está diseñado para funcionar con Python 3. Si aún no tienes Python instalado, no te preocupes. Puedes descargarlo desde el [sitio web oficial de Python](https://www.python.org/downloads/).

### Ejecución

1. **Descarga**: Puedes obtener el código de dos maneras copiando y pegando el código en un archivo de Python con extensión `.py`, o descargando el archivo `elevador.py` que se adjunta.

2. **Ejecución en la terminal**: Para ejecutar el programa, abre una terminal o línea de comandos en tu computadora. Luego, navega al directorio donde se encuentra el archivo de código.

3. **Iniciar el programa**: Utiliza alguna de las siguientes opciones para iniciar la ejecución del programa.

Escribe simplemente el nombre del programa y teclea `enter`:

   ```
   elevador.py
   ```

Escribe `py`, el nombre del programa y teclea `enter`:

 ```
py elevador.py
 ```
Escribe `python`, el nombre del programa y teclea `enter`:

 ```
python elevador.py
 ```

- **Ejecución desde una IDE**: Además de la ejecución en la terminal, también puedes ejecutar el programa directamente desde un Entorno de Desarrollo Integrado (IDE) como PyCharm, Visual Studio Code u otro IDE de Python de tu elección. Abre el archivo en la IDE y utiliza la opción de ejecución o depuración proporcionada por la misma IDE para iniciar el programa.

## Mejoras

La implementación proporcionada es un punto de partida para la simulación de un sistema de ascensores, pero existen áreas donde se podrían realizar mejoras, como:

- Manejo de excepciones.
- Finalización controlada.
- Tiempos de espera ajustables.
- Control de hilos activos.
- Seguridad y concurrencia mejorada.

Este es un ejemplo de la implementación de un sistema de ascensores y personas que esperan, utilizando hilos y sincronización. El propósito de esta simulación es ofrecer una solución a un problema de sincronización común en situaciones cotidianas.

---

> Realizado por:
> - Hernández Ortiz Jonathan Emmanuel.
> - Pérez Avin Paola Celina de Jesús.

