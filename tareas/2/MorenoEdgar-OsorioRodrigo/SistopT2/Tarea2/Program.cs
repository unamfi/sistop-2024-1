using Spectre.Console;

namespace Tarea2;

public static class Program
{
    public static void Main(string[] args)
    {
        var procesos = new List<Process>
        {
            new() { Nombre = "A", Llegada = 0, Ticks = 3 },
            new() { Nombre = "B", Llegada = 1, Ticks = 5 },
            new() { Nombre = "C", Llegada = 3, Ticks = 2 },
            new() { Nombre = "D", Llegada = 9, Ticks = 5 },
            new() { Nombre = "E", Llegada = 12, Ticks = 5 }
        };
        EstablecerColores(procesos);
        AnsiConsole.Write(new Rule { Justification = Justify.Center, Title = "Primera ronda" });
        EjecutarRonda(procesos);

        procesos.Clear();
        // A: 0, t=5; B: 3, t=3; C: 3, t=7; D: 7, t=4; E:8, t=4 (tot:23)
        procesos = new List<Process>
        {
            new() { Nombre = "A", Llegada = 0, Ticks = 5 },
            new() { Nombre = "B", Llegada = 3, Ticks = 3 },
            new() { Nombre = "C", Llegada = 3, Ticks = 7 },
            new() { Nombre = "D", Llegada = 7, Ticks = 4 },
            new() { Nombre = "E", Llegada = 8, Ticks = 4 }
        };
        EstablecerColores(procesos);
        AnsiConsole.Write(new Rule { Justification = Justify.Center, Title = "Segunda Ronda" });
        EjecutarRonda(procesos);

        if (args.Contains("--rand")){
            // Ronda aleatoria
            procesos = GenerarRonda(6, 30);
            EstablecerColores(procesos);
            AnsiConsole.Write(new Rule { Justification = Justify.Center, Title = "Tercera Ronda" });
            EjecutarRonda(procesos);
        }
    }

    private static void EstablecerColores(List<Process> procesos)
    {
        procesos.ForEach(p =>
        {
            var color = ColorUtils.GetRandomColor();
            p.Color = color;
            p.BgColor = ColorUtils.GetComplementaryColor(color);
        });
    }

    private static void EjecutarRonda(List<Process> procesos)
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
        AnsiConsole.Write(procTable);

        AlgoritmosPlanificacion.FirstComeFirstServe(new List<Process>(procesos));
        procesos.ForEach(p => p.ResetValues());
        AlgoritmosPlanificacion.RoundRobin(procesos);
        procesos.ForEach(p => p.ResetValues());
        AlgoritmosPlanificacion.RoundRobin(procesos, 4);
        procesos.ForEach(p => p.ResetValues());
        AlgoritmosPlanificacion.ShortestProcessNext(procesos);
        procesos.ForEach(p => p.ResetValues());
        AlgoritmosPlanificacion.SelfishRoundRobin(procesos, 2, 1);
    }

    private static List<Process> GenerarRonda(int conteo, int maxTicks)
    {
        var procesos = Enumerable.Range(0, conteo)
            .Select(idx => new Process
            {
                Nombre = $"{(char)(65 + idx)}",
                Ticks = Random.Shared.Next(2, maxTicks / 2),
                Llegada = Random.Shared.Next(0, maxTicks / 2)
            }).ToList();
        if (procesos.FirstOrDefault(p => p.Llegada == 0) is null)
            procesos[Random.Shared.Next(0, conteo)].Llegada = 0;
        return procesos;
    }
}