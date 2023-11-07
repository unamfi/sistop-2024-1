using System.Diagnostics.CodeAnalysis;
using Spectre.Console;

namespace SistopP2.Cli;

internal static class Program
{
    private static readonly SemaphoreSlim PistaAterrizaje = new(0);
    private static readonly SemaphoreSlim ComunicacionAvion = new(1);
    private static readonly SemaphoreSlim ComunicationTorre = new(0);
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

    private static readonly Dictionary<TipoAvion, string> TipoAvionStr = new()
    {
        { TipoAvion.Comercial, "comercial" },
        { TipoAvion.Pasajeros, "pasajeros" }
    };

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
        AnsiConsole.MarkupLine($"[blue on purple]Avión {id} (Tipo: {tipoStr}) solicita aterrizaje.[/]");
        ComunicacionAvion.Wait();
        _solicitud = id.ToString();
        ComunicationTorre.Release();

        PistaAterrizaje.Wait();
        // Descarga de tripulantes o de mercancía
        AnsiConsole.MarkupLine($"[blue on magenta]Avión {id} ha aterrizado.[/]");
        anden.Wait();
        Thread.Sleep(Random.Shared.Next(1000, 4000));
        AnsiConsole.MarkupLine($"[blue on magenta]Avión de {tipoStr} ha terminado de descargar.[/]");
        
        // Carga de otros tripulantes o de mercancía
        AnsiConsole.MarkupLine($"[blue on magenta]Avión de {tipoStr} esperando a estar listo para el siguiente vuelo[/].");
        Thread.Sleep(Random.Shared.Next(1000, 4000));
        anden.Release();
        AnsiConsole.MarkupLine($"[blue on magenta]Avión de {tipoStr} solicitando despegue.[/]");
        ComunicacionAvion.Wait();
        _solicitud = id.ToString();
        ComunicationTorre.Release();
        PistaAterrizaje.Wait();
        AnsiConsole.MarkupLine($"[blue on magenta]Avión de {tipoStr} sale del aereopuerto.[/]");
    }

#pragma warning disable CA2016
    /**
     * Representa la torre de control para comunicarse con los aviones.
     */
    [SuppressMessage("ReSharper", "MethodSupportsCancellation")]
    public static void TorreControl(CancellationToken token)
    {
        AnsiConsole.Markup("[green]:tower: Torre de control lista[/]");
        // Continúa operaciones mientras no se solicite que pare
        while (!token.IsCancellationRequested)
        {
            ComunicationTorre.Wait();
            AnsiConsole.Markup($"[green on dark] Torre de control dice: {_solicitud} puede aterrizar.");
            PistaAterrizaje.Release();
            ComunicacionAvion.Release();
        }
    }
#pragma warning restore CA2016

    public static void Main(string[] args)
    {
    }
}