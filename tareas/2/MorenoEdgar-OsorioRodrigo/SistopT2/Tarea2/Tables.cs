using Spectre.Console;

namespace Tarea2;

/// <summary>
/// Creación de las tablas de resultados.
/// </summary>
public static class Tables
{
    /// <summary>
    /// Crea la tabla del resúmen rápido de los procesos (sin resultados).
    /// </summary>
    /// <param name="procesos">Lista de procesos</param>
    /// <returns>Objeto <see cref="Spectre.Console.Table"/> para su muestra en pantalla</returns>
    public static Table CreateProcessTable(List<Process> procesos)
    {
        var procTable = new Table
        {
            Border = TableBorder.Rounded,
            Title = new TableTitle("Lista de procesos"),
            UseSafeBorder = true
        };
        procTable.Centered();
        procTable.AddColumn("Proceso")
            .AddColumn("Tiempo de llegada")
            .AddColumn("Tiempo requerido(t)");
        procesos.ForEach(p => procTable.AddRow(p.Nombre!, p.Llegada.ToString(), p.Ticks.ToString()));
        procTable.AddRow("Promedio", "", $"{procesos.Average(p => p.Ticks)}");
        return procTable;
    }
    
    /// <summary>
    /// Crea la tabla del resumen de ejecución.
    /// </summary>
    /// <param name="procesos">Lista de procesos</param>
    /// <param name="title">Título de la tabla</param>
    /// <param name="timeline">Orden de ejecución</param>
    /// <returns>Objeto <see cref="Spectre.Console.Table"/> para su muestra en pantalla</returns>
    public static Table CreateSummaryTable(List<Process> procesos, string title, string timeline)
    {
        var table = CreateResultsTable(procesos);
        var chart = CreateChart(procesos);
        var total = procesos.Sum(p => p.Ticks);
        var container = new Table
        {
            Border = TableBorder.Rounded,
            Title = new TableTitle(title),
            Expand = true
        };
        container.AddColumns("Resultados", "Información adicional");
        container.AddRow(table, new Rows(chart,
            new Panel(new Markup(timeline))
            {
                Header = new PanelHeader($"Ejecución (Total: {total})"),
                Expand = true,
                Border = BoxBorder.Rounded
            }) { Expand = true });
        return container;
    }

    /// <summary>
    /// Creación de la tabla de resultados.
    /// </summary>
    /// <param name="procesos">Lista de procesos</param>
    /// <returns>Objeto <see cref="Spectre.Console.Table"/> para agregarlo en la tabla final.</returns>
    private static Table CreateResultsTable(List<Process> procesos)
    {
        var procTable = new Table
        {
            Border = TableBorder.Rounded,
            UseSafeBorder = true
        };
        procTable.Centered();
        procTable.AddColumn("Proceso")
            .AddColumn("Llegada")
            .AddColumn("t")
            .AddColumn("Inicio")
            .AddColumn("Fin")
            .AddColumn("T").AddColumn("E").AddColumn("P");
        procesos
            .ForEach(p => procTable.AddRow(p.Nombre!,
                    p.Llegada.ToString(),
                    p.Ticks.ToString(),
                    p.Inicio.ToString(),
                    p.Final.ToString(),
                    p.TiempoRespuesta.ToString(),
                    p.TiempoEspera.ToString(),
                    p.Penalizacion.ToString("0.00")
                )
            );
        procTable.AddRow("Promedio", string.Empty, procesos.Average(p => p.Ticks).ToString("0.00"),
            string.Empty, string.Empty,
            procesos.Average(p => p.TiempoRespuesta).ToString("0.00"),
            procesos.Average(p => p.TiempoEspera).ToString("0.00"),
            procesos.Average(p => p.Penalizacion).ToString("0.00")
        );
        return procTable;
    }

    /// <summary>
    /// Creación de la gráfica de la proporción de penalización.
    /// </summary>
    /// <param name="procesos">Lista de procesos</param>
    /// <returns>Objeto <see cref="Spectre.Console.Panel"/> para agregarlo en la tabla final.</returns>
    private static Panel CreateChart(List<Process> procesos)
    {
        var chart = new BarChart().CenterLabel();
        procesos.ForEach(p => chart.AddItem(p.Nombre!, p.Penalizacion, p.BgColor));
        var panel = new Panel(chart)
        {
            Header = new PanelHeader("Gráfico"),
            Border = BoxBorder.Rounded
        };
        return panel;
    }
}