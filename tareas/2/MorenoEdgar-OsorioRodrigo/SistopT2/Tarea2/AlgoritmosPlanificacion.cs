using System.Text;
using Spectre.Console;
using Tarea2.Extensions;

namespace Tarea2;

public static class AlgoritmosPlanificacion
{
    /// <summary>
    /// Esquema más simple de planificación.
    /// El primero que llega, es el primero servido.
    /// First come, first serve.
    /// </summary>
    public static void FirstComeFirstServe(List<Process> procesos)
    {
        Queue<Process> qProcesos = new(); // Se crea una cola de procesos

        procesos // Se ordenan los procesos por su llegada y se encolan
            .OrderBy(p => p.Llegada)
            .ForEach(p => qProcesos.Enqueue(p));

        var timeline = new StringBuilder(); // Para crear la parte visual del orden de ejecución

        var tick = 0; // Ticks recorridos
        while (qProcesos.Count != 0) // El bucle continúa mientras haya procesos
        {
            var p = qProcesos.Dequeue(); // Se saca un proceso
            p.Inicio = tick; // Se establece su tick de inicio
            var conteoTicks = p.Ticks; // Comienza el conteo de ticks hasta que no requiera más
            while (conteoTicks > 0)
            {
                // Se resta un tick al proceso
                conteoTicks--;
                // Se suma un tick en el procesador
                tick++;
                // Se agrega en la "línea del tiempo"
                timeline.Append($"[{p.Color.ToMarkup()} on {p.BgColor.ToMarkup()}]")
                    .Append(p.Nombre!.First())
                    .Append("[/]");
            }

            // Cálculos finales para los parámetros de la tabla
            p.Final = tick;
            p.TiempoRespuesta = p.Final - p.Llegada;
            p.TiempoEspera = p.TiempoRespuesta - p.Ticks;
            p.Penalizacion = p.TiempoRespuesta * 1.0 / p.Ticks;
        }

        // Se muestran los resultados
        var container = Tables.CreateSummaryTable(procesos, "First come, first serve", timeline.ToString());
        AnsiConsole.Write(container);
    }

    /// <summary>
    /// Algoritmo Round Robin, va alternando entre los procesos conforme fueron llegando.
    /// </summary>
    /// <param name="procesos">Listado de procesos</param>
    /// <param name="quantum">Número de ticks seguidos disponibles por proceso</param>
    public static void RoundRobin(List<Process> procesos, int quantum = 1)
    {
        var total = procesos.Sum(p => p.Ticks); // Obtención del total de ticks requeridos.
        List<Process> processList = new(procesos.OrderBy(p => p.Llegada)); // Se ordenan los procesos en una lista temporal
        processList.ForEach(p => p.ConteoTicks = p.Ticks); // Se establece el conteo de ticks de cada proceso.

        var timeline = new StringBuilder();

        var tick = 0;
        while (tick < total) // Bucle principal mientras no se hayan ejecutado todos los procesos.
        {
            // Se establece el valor del quantum
            var qCount = quantum;

            // Obtiene un elemento de la lista y lo remueve
            var p = processList.First();
            processList.Remove(p);
            p.Inicio = (p.Inicio == 0 || tick == 0) ? tick : p.Inicio; // Se establece su tick de inicio si no ha sido establecido.

            // Mientras haya ticks del quantum, no se haya superado el total de ticks y el proceso no haya terminado.
            while (qCount > 0 && tick < total && p.ConteoTicks > 0)
            {
                tick++; // Se aumenta un tick
                qCount--; // Se resta un tick al quantum
                p.ConteoTicks--; // Se resta un tick al proceso
                // Se agrega a la "línea del tiempo"
                timeline.Append($"[{p.Color.ToMarkup()} on {p.BgColor.ToMarkup()}]")
                    .Append(p.Nombre!.First())
                    .Append("[/]");
            }

            // Si el proceso ya no requiere más ticks, se realizan los cálculos para
            // la tabla final
            if (p.ConteoTicks <= 0)
            {
                p.Final = tick;
                p.TiempoRespuesta = p.Final - p.Llegada;
                p.TiempoEspera = p.TiempoRespuesta - p.Ticks;
                p.Penalizacion = p.TiempoRespuesta * 1.0 / p.Ticks;
                continue;
            }

            // Se reinserta en la siguiente posición
            var nextIdx = processList.FindIndex(proceso => proceso.Llegada > tick);
            processList.Insert(nextIdx == -1 ? processList.Count : nextIdx, p);
        }

        var container = Tables.CreateSummaryTable(procesos, $"Round Robin (q = {quantum})", timeline.ToString());
        AnsiConsole.Write(container);
    }

    /// <summary>
    /// Algoritmo Shortest Process Next, se le da prioridad a los algoritmos que tienen una
    /// ejecución más corta.
    /// </summary>
    /// <param name="procesos">Listado de procesos</param>
    public static void ShortestProcessNext(List<Process> procesos)
    {
        var total = procesos.Sum(p => p.Ticks);
        List<Process> processList = new(procesos.OrderBy(p => p.Llegada));
        processList.ForEach(p => p.ConteoTicks = p.Ticks);

        var timeline = new StringBuilder();

        var tick = 0;
        while (tick < total)
        {
            var p = processList.First(); // Se obtiene el primer elemento y se remueve
            processList.Remove(p);
            p.Inicio = (p.Inicio == 0 || tick == 0) ? tick : p.Inicio; // Se establece el tick de inicio
            while (p.ConteoTicks > 0) // Mientras el proceso requiera ticks, se sigue ejecutando
            {
                tick++;
                p.ConteoTicks--;
                timeline.Append($"[{p.Color.ToMarkup()} on {p.BgColor.ToMarkup()}]")
                    .Append(p.Nombre!.First())
                    .Append("[/]");
            }

            // Cálculos para la tabla
            p.Final = tick;
            p.TiempoRespuesta = p.Final - p.Llegada;
            p.TiempoEspera = p.TiempoRespuesta - p.Ticks;
            p.Penalizacion = p.TiempoRespuesta * 1.0 / p.Ticks;

            // Se reordenan los elementos, para colocar hasta arriba los de menor ejecución pero mantener el orden de llegada.
            processList = (from proceso in processList orderby proceso.Ticks, proceso.Llegada select proceso).ToList();
        }

        var container = Tables.CreateSummaryTable(procesos, "Shortest Process Next", timeline.ToString());
        AnsiConsole.Write(container);
    }

    /// <summary>
    /// Algoritmo de Ronda egoísta (Selfish Round Robin). No estoy seguro de que sea 100% correcto.
    /// </summary>
    /// <param name="procesos">Lista de procesos</param>
    /// <param name="aInc">Ritmo en el cual se incrementará la prioridad de
    /// los procesos de la cola de procesos nuevos.</param>
    /// <param name="bInc">Ritmo de incremento de prioridad para procesos aceptados.</param>
    public static void SelfishRoundRobin(List<Process> procesos, int aInc, int bInc)
    {
        var total = procesos.Sum(p => p.Ticks);
        List<Process> procesosNuevos = new(procesos.OrderBy(p => p.Llegada));
        procesosNuevos.ForEach(p => p.ConteoTicks = p.Ticks);
        List<Process> procesosAceptados = new();
        List<Process> procesosEspera = new();

        var timeline = new StringBuilder();

        var tick = 0;
        while (tick < total)
        {
            // Entrada de los procesos
            var p = procesosNuevos.FirstOrDefault();
            if (p is not null && p.Llegada <= tick)
            {
                p.Prioridad = 0; // Se inicia en cero
                p.Inicio = (p.Inicio == 0 || tick == 0) ? tick : p.Inicio; // Se establece su tick de inicio.
                if (procesosAceptados.Count == 0)
                    procesosAceptados.Add(p); // Se añade a la fila de aceptados.
                else
                    procesosEspera.Add(p); // Se añade a la fila de espera.
                procesosNuevos.Remove(p); // Se remueve de la lista de procesos.
            }

            // Se obtiene el proceso de mayor prioridad
            p = procesosAceptados.FirstOrDefault();
            var e = procesosEspera.MaxBy(proceso => proceso.Prioridad); // Se busca el siguiente proceso con mayor prioridad
            // En esta parte se comparan los procesos con mayor prioridad en ambas filas.
            if (p is not null)
                procesosAceptados.Remove(p); // Se elimina ell proceso de la lista de aceptados
            else
                p = e; // Si no hay procesos aceptados, se utiliza el de mayor prioridad en espera.
            if (e is not null && (e.Prioridad >= p!.Prioridad))
            {
                procesosAceptados.Add(p); // Se agrega a la lista de procesos aceptados
                procesosEspera.Remove(e); // Se elimina de la lista de procesos en espera
                p = e; // Se establece el proceso a ejecutar como el proceso que estaba en espera
            }

            // Se resta un tick al proceso
            p!.ConteoTicks--;
            timeline.Append($"[{p.Color.ToMarkup()} on {p.BgColor.ToMarkup()}]")
                .Append(p.Nombre!.First())
                .Append("[/]");

            tick++;
            // Cálculos para las tablas
            if (p.ConteoTicks <= 0)
            {
                p.Final = tick;
                p.TiempoRespuesta = p.Final - p.Llegada;
                p.TiempoEspera = p.TiempoRespuesta - p.Ticks;
                p.Penalizacion = p.TiempoRespuesta * 1.0 / p.Ticks;
                procesosAceptados.Remove(p);
            }
            else
                procesosAceptados.Add(p); // Se reinserta el proceso

            // Recalculado de las prioridades
            procesosEspera.ForEach(proceso => proceso.Prioridad += aInc);
            procesosAceptados.ForEach(proceso => proceso.Prioridad += bInc);
        }

        var container = Tables.CreateSummaryTable(procesos, "Selfish Round Robin", timeline.ToString());
        AnsiConsole.Write(container);
    }
}