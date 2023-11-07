using System.Diagnostics.CodeAnalysis;
using Spectre.Console;

namespace SistopP2.Cli;

internal static class Program
{
    private static readonly SemaphoreSlim PistaAterrizaje = new(0);
    private static readonly SemaphoreSlim ComunicacionAvion = new(1);
    private static readonly SemaphoreSlim ComunicacionTorre = new(1);
    private static readonly SemaphoreSlim AndenPasajeros = new(10);
    private static readonly SemaphoreSlim AndenMercancia = new(6);

    private static object _lock = new();
    private static string _solicitud = "";

    /// <summary>
    /// Un enum para indicar de que tipo es un avión, si de carga o de pasajeros.
    /// </summary>
    public enum TipoAvion
    {
        Comercial,
        Pasajeros
    }

    /// <summary>
    /// Representa un avión.
    /// </summary>
    /// <param name="id">ID del avión</param>
    /// <param name="tipo">Tipo de avión</param>
    public static void Avion(int id, TipoAvion tipo)
    {
        // Obtiene el tipo de avión
        var anden = tipo == TipoAvion.Comercial ? AndenMercancia : AndenPasajeros;
        var tipoStr = tipo.ToString();
        // El avión solicita aterrizaje en la pista
        AnsiConsole.MarkupLine($"[purple]Avión {id} (Tipo: {tipoStr}) solicita aterrizaje.[/]");
        ComunicacionAvion.Wait();
        _solicitud = id.ToString();
        ComunicacionTorre.Release();

        PistaAterrizaje.Wait();
        // Descarga de tripulantes o de mercancía
        AnsiConsole.MarkupLine($"[purple]Avión {id} ha aterrizado.[/]");
        anden.Wait();
        Thread.Sleep(Random.Shared.Next(1000, 4000));
        AnsiConsole.MarkupLine($"[purple]Avión de {tipoStr} ha terminado de descargar.[/]");

        // Carga de otros tripulantes o de mercancía
        AnsiConsole.MarkupLine($"[purple]Avión de {tipoStr} esperando a estar listo para el siguiente vuelo[/].");
        Thread.Sleep(Random.Shared.Next(1000, 4000));
        anden.Release();
        AnsiConsole.MarkupLine($"[purple]Avión de {tipoStr} solicitando despegue.[/]");
        ComunicacionAvion.Wait();
        _solicitud = id.ToString();
        ComunicacionTorre.Release();
        PistaAterrizaje.Wait();
        AnsiConsole.MarkupLine($"[purple]Avión de {tipoStr} sale del aereopuerto.[/]");
    }

    /**
     * Representa la torre de control para comunicarse con los aviones.
     */
    private static void TorreControl(CancellationToken token)
    {
        AnsiConsole.MarkupLine("[green]:tower: Torre de control lista[/]");
        // Continúa operaciones mientras no se solicite que pare
        while (!token.IsCancellationRequested)
        {
            ComunicacionTorre.Wait();
            AnsiConsole.MarkupLine($"[green] Torre de control dice: {_solicitud} puede aterrizar.[/]");
            PistaAterrizaje.Release();
            ComunicacionAvion.Release();
        }
    }

    public static async Task Main(string[] args)
    {
        var salir = new CancellationTokenSource();
        var aviones = new List<Task>();
        // ReSharper disable once MethodSupportsCancellation
        var torre = new Task(() => TorreControl(salir.Token));
        torre.Start();

        const int numAviones = 15;

        for (var i = 0; i < numAviones; i++)
        {
            var tipo = Random.Shared.Next(0, 2) == 0 ? TipoAvion.Pasajeros : TipoAvion.Comercial;
            var id = i;
            var task = new Task(() => Avion(id, tipo));
            task.Start();
            aviones.Add(task);
            Task.Delay(Random.Shared.Next(500, 1000));
        }

        await Task.WhenAll(aviones);
        salir.Cancel();
    }
}