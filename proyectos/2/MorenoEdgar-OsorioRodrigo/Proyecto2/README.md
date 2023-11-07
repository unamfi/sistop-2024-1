# Proyecto: Aereopuerto.

## Integrantes del equipo.
- Moreno Chalico Edgar Ulises
- Osorio Ángeles Rodrigo Jafet

## Identificación del problema.

Para poder viajar a otros países de manera más rápida y eficaz, debemos tener en cuenta el uso de viajes por avión. Nuestro problema de paralelización se basa en el aeropuerto. 

### Descripción del problema.

En un aeropuerto se tienen zonas específicas de operación y sincronización para los despegues y el aterrizaje de los aviones. Por lo que tenemos que considerar las siguientes áreas en el planteamiento: 

- Andenes para pasajeros y comercial. 
- Torre de control (comunicación).
- Pista de aterrizaje/despegue. 
- Área de abordaje y descenso de pasajeros.
- Área de carga y descarga comercial.

En el contexto de un proyecto de paralelismo, se conoce que se recibe un flujo constante de solicitudes de aterrizaje en la pista de aterrizaje, y estas solicitudes son manejadas por la torre de control. La torre de control debe administrar los aterrizajes y despegues en función del orden en que llegan las solicitudes de los aviones, asegurando que ninguno de los aviones quede esperando indefinidamente. Cada avión que aterriza regresará a despegar después de dejar a sus pasajeros o mercancía y ser cargado nuevamente con pasajeros o mercancía.

El área de abordaje/descenso de pasajeros puede manejar simultáneamente hasta 10 aviones, mientras que el área de carga/descarga de mercancía puede operar con hasta 6 aviones de carga al mismo tiempo. Cuando un avión no puede aterrizar, se le mantendrá en espera en la zona aérea designada, y si un avión no puede despegar, se quedará en la zona de espera en tierra.

## Planteamiento y estrategia del programa.

Se maneja la sincronización y los procesos paralelos mediante la torre de control, ya que es la encargada de tener el orden y funcionamiento de las operaciones de los aviones y las pistas de aterrizaje/despegue. Por lo que tenemos declarado la función para la torre de la siguiente manera: 

 ```
private static void TorreControl(CancellationToken token)
    {
        AnsiConsole.MarkupLine("[green]:satellite_antenna: Torre de control lista[/]");
        // Continúa operaciones mientras no se solicite que pare
        while (!token.IsCancellationRequested)
        {
            ComunicacionTorre.Wait();
            var mensaje = _solicitud.Split(",", StringSplitOptions.TrimEntries);
            AnsiConsole.MarkupLine($"[green]:satellite_antenna: Torre de control dice: {mensaje[0]} puede {mensaje[1]}.[/]");
            PistaAterrizaje.Release();
            ComunicacionAvion.Release();
        }
    }
  ```
Observamos que tiene una comunicación con el avión, por lo que, recibe las solicitudes de la operación a realizar. Se verifica esta solicitud con la parte de _solicitud.Split, que separa el mensaje para revisar el avión y la acción a realizar; considerando esto regresa un mensaje de vuelta para saber si se puede o no realizar la acción. 



## Lenguaje de programación y entorno.

Este programa fue desarrollado en el lenguaje de programación C# (.NET 7), totalmente en Linux.

Para ejecutarlo se necesita el paquete `dotnet`.


## Capturas de la ejecución.

Inicio de la ejecución:

Final de la ejecución: