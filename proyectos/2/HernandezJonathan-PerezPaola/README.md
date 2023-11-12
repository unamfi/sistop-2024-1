---
title: 'PROYECTO 02: EL CINE'
created: '2023-11-01T06:37:56.610Z'
modified: '2023-11-07T10:07:02.500Z'
---

# PROYECTO 02: EL CINE

## SITUACIÓN A MODELAR
Imagina que estamos organizando una emocionante noche de cine en una sala con capacidad para 10 espectadores. La película que proyectaremos es extremadamente popular y ha generado un gran entusiasmo, con 100 clientes deseando ingresar a la sala para disfrutarla. Para garantizar que esta experiencia sea fluida y justa para todos, necesitamos encontrar una manera de coordinar el acceso de estos 100 clientes a una sala con una capacidad máxima de 10 personas a la vez. El objetivo principal de esta coordinación es asegurarnos de que todos los clientes tengan la oportunidad de disfrutar de la película sin enfrentar problemas ni aglomeraciones.

## CONSECUENCIAS NOCIVAS DE LA CONCURRENCIA

1. **Competencia por recursos**: La concurrencia en la asignación de asientos podría llevar a problemas como la asignación incorrecta de asientos o el acceso a asientos ya ocupados.

2. **Posible inanición o bloqueo**: Aunque se usa un semáforo para evitar bloqueos, en situaciones más complejas, podrían ocurrir bloqueos si los hilos no se manejan adecuadamente.

3. **Recursos compartidos sin protección**: Variables compartidas, como la variable `abandonos`, no están protegidas adecuadamente, lo que podría causar problemas de concurrencia.

4. **Problemas de sincronización**: El uso de `time.sleep` para simular eventos y retrasos puede ser ineficiente y conducir a resultados no deseados en situaciones más complejas.

5. **Manejo de errores**: La falta de manejo de errores en hilos individuales podría llevar a bloqueos o problemas inesperados en aplicaciones más grandes y complejas.

## EVENTOS QUE QUERAMOS CONTROLAR

1. **Llegada de espectadores**: Es posible controlar cuándo y cómo llegan los espectadores a la sala de cine. Por ejemplo, se puede ajustar el tiempo de llegada de los espectadores o simular diferentes patrones de llegada.

2. **Asignación de asientos**: Se puede gestionar cómo se asignan los asientos a los espectadores. En el código actual, se utiliza un semáforo para limitar la cantidad de espectadores en la sala al mismo tiempo. Esto se puede personalizar.

3. **Comportamiento de los espectadores**: Se puede controlar el comportamiento de los espectadores mientras ven la película. En el código, se simulan comportamientos como comprar palomitas o ir al baño. Se pueden agregar más comportamientos o ajustar las probabilidades de que ocurran.

4. **Deserción de espectadores**: Se puede controlar cuándo y cómo los espectadores abandonan la sala de cine. En el código, hay una función que simula la deserción aleatoria de espectadores. Se puede ajustar la probabilidad de deserción o implementar otras condiciones para la deserción.

5. **Finalización de la película**: Es posible controlar cuándo finaliza la película y cuándo todos los espectadores han abandonado la sala. En el código, se espera a que todos los hilos de espectadores finalicen y se muestra un mensaje al final. Esto se puede personalizar.

6. **Manejo de errores**: Se puede gestionar errores o situaciones inesperadas que puedan ocurrir, como la falta de asientos disponibles, problemas con los hilos de espectadores, etc.

7. **Interacción de los hilos**: Se puede controlar la interacción y sincronización de los hilos para asegurarse de que los espectadores no accedan a asientos ocupados al mismo tiempo, evitando condiciones de carrera.

8. **Visualización y registro de eventos**: Es posible personalizar la forma en que se muestran los eventos en la consola o registrar eventos en un archivo de registro para su posterior análisis.

## EVENTOS CONCURRENTES DE ORDENAMIENTO RELATIVO

En este código al menos, varios eventos concurrentes sí requieren de un ordenamiento relativo. Considerando que lo que se idea es un funcionamiento adecuadamente correcto y coherente en una situación cotidiana de concurrencia.

1. **Asignación de asientos**: El uso del semáforo `semaforo_cine` garantiza que no más de 10 espectadores accedan a la sala de cine al mismo tiempo. El orden en el que los hilos intentan adquirir un asiento es importante para evitar que más espectadores ocupen asientos de los disponibles.

2. **Comportamiento de los espectadores**: Los comportamientos de los espectadores, como comprar palomitas o ir al baño, ocurren de manera concurrente con la visualización de la película. El orden relativo de estos eventos puede afectar la simulación y el resultado final.

3. **Deserción de espectadores**: La función `desercion_aleatoria` simula la deserción aleatoria de espectadores. El orden en que los espectadores deciden abandonar es importante, ya que esto afecta la disponibilidad de asientos en la sala.

4. **Finalización de la película**: El orden en que los hilos de espectadores finalizan de ver la película es importante para determinar cuándo todos han terminado y se puede mostrar el mensaje de que todos han abandonado el cine.

El orden en el que estos eventos ocurren puede influir en el resultado y en la simulación de una experiencia realista en una sala de cine. Por lo tanto, es importante gestionar adecuadamente la concurrencia y la sincronización de hilos para garantizar una ejecución adecuada.

## REQUISITOS

¿Deseas ejecutar este programa y su simulación en tu computadora? A continuación, se detallan los pasos para ejecutar el programa. 

1. **Python**: Asegúrate de tener Python instalado en tu computadora. En efecto, este código está diseñado para funcionar con Python 3. Si aún no tienes Python instalado, no te preocupes. Puedes descargarlo desde el [sitio web oficial de Python](https://www.python.org/downloads/).

## EJECUCIÓN

1. **Descarga**: Puedes obtener el código de dos maneras copiando y pegando el código en un archivo de Python con extensión `.py`, o descargando el archivo `cine_final.py` que se adjunta.

2. **Ejecución en la terminal**: Para ejecutar el programa, abre una terminal o línea de comandos en tu computadora. Luego, navega al directorio donde se encuentra el archivo de código.

3. **Iniciar el programa**: Utiliza alguna de las siguientes opciones para iniciar la ejecución del programa.

Escribe simplemente el nombre del programa y teclea `enter`:

   ```
   cine_final.py
   ```

Escribe `py`, el nombre del programa y teclea `enter`:

 ```
py cine_final.py
 ```
Escribe `python`, el nombre del programa y teclea `enter`:

 ```
python cine_final.py
 ```

 Se recomienda tener instalada la biblioteca `colorama` en la terminal. Que es una biblioteca de Python que facilita la impresión de texto en colores y estilos en terminales y consolas.*

   ---

> Realizado por:
> - Hernández Ortiz Jonathan Emmanuel.
> - Pérez Avin Paola Celina de Jesús.
