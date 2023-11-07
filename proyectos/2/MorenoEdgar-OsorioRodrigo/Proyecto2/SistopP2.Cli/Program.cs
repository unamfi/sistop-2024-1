using System.Diagnostics.CodeAnalysis;
using Mono.Options;
using Spectre.Console;

// Por alguna razón tuve que agregar que ignore un warning al crear un Task con la función de la torre de control,
// solicita agregar un await a la llamada de la función, lo cual no debería, ya que este aplica solo después de torre.Start().
#pragma warning disable CS4014 // Because this call is not awaited, execution of the current method continues before the call is completed

namespace SistopP2.Cli;

internal static class Program
{
    private static readonly SemaphoreSlim Pista = new(0);
    private static readonly SemaphoreSlim ComunicacionAvion = new(1);
    private static readonly SemaphoreSlim ComunicacionTorre = new(1);
    private static SemaphoreSlim _andenPasajeros = new(6);
    private static SemaphoreSlim _andenMercancia = new(2);

    private static int _nAndenesPasajeros = 6;
    private static int _nAndenesMercancia = 2;
    private static int _numeroAviones = 15;

    private static string _solicitud = "";

    /// <summary>
    /// Un enum para indicar de que tipo es un avión, si de carga o de pasajeros.
    /// </summary>
    private enum TipoAvion
    {
        Comercial,
        Pasajeros
    }

    /// <summary>
    /// Representa un avión, para no repetir la función para cada tipo de avión, se utiliza el enum
    /// declarado unas líneas más arriba, y se asignan las variables necesarias a partir de este
    /// dato asignado.
    /// </summary>
    /// <param name="id">ID del avión</param>
    /// <param name="tipo">Tipo de avión</param>
    private static void Avion(int id, TipoAvion tipo)
    {
        // Obtiene el anden que le corresponde de acuerdo al tipo de avión.
        // Básicamente obtiene la referencia del semáforo que le corresponde.
        var anden = tipo == TipoAvion.Comercial ? _andenMercancia : _andenPasajeros;
        // Obtiene un string con el tipo de avión.
        var tipoStr = tipo.ToString();
        // Se le asigna un color distinto a cada tipo de avión.
        var color = tipo == TipoAvion.Comercial ? "purple" : "teal";

        AnsiConsole.MarkupLine($"[{color}]:airplane:({tipoStr}) Avión {id} solicita aterrizaje.[/]");
        // El avión solicita aterrizaje en la pista.
        ComunicacionAvion.Wait();
        // Envía un mensaje a la torre de control, indicando su id y la acción que quiere realizar, separados por coma.
        _solicitud = $"{id},aterrizar";
        // Libera la comunicación con la torre.
        ComunicacionTorre.Release();

        // Ocupa la pista temporalmente
        Pista.Wait();
        // Descarga de tripulantes o de mercancía
        AnsiConsole.MarkupLine($"[{color}]:airplane_arrival:({tipoStr}) Avión {id} ha aterrizado.[/]");
        // Ocupa uno de los andenes que le corresponden
        anden.Wait();
        AnsiConsole.MarkupLine($"[{color}]:airplane_arrival:({tipoStr}) Avión {id} toma 1 lugar de {anden.CurrentCount + 1} de los andenes.[/]");
        // Pequeña espera...
        Thread.Sleep(Random.Shared.Next(1000, 4000));
        AnsiConsole.MarkupLine($"[{color}]:airplane:({tipoStr}) Avión {id} se ha terminado de descargar.[/]");

        // Carga de otros tripulantes o de mercancía
        AnsiConsole.MarkupLine($"[{color}]:airplane:({tipoStr}) Avión {id} esperando a estar listo para el siguiente vuelo[/].");
        // Otra espera...
        Thread.Sleep(Random.Shared.Next(1000, 4000));
        // Libera el andén que había utilizado
        anden.Release();
        AnsiConsole.MarkupLine($"[{color}]:airplane:({tipoStr}) Avión {id} solicitando despegue.[/]");
        // Envía un mensaje a la torre de control
        ComunicacionAvion.Wait();
        _solicitud = $"{id},despegar";
        ComunicacionTorre.Release();
        // Ocupa la pista para despegar y se retira.
        Pista.Wait();
        AnsiConsole.MarkupLine($"[{color}]:airplane_departure:({tipoStr}) Avión {id} sale del aereopuerto.[/]");
    }

    /// <summary>
    /// Representa la torre de control para los aviones.
    /// </summary>
    /// <param name="token">Token de cancelación para detener la ejecución.</param>
    [SuppressMessage("Reliability", "CA2016:Forward the \'CancellationToken\' parameter to methods")]
    [SuppressMessage("ReSharper", "MethodSupportsCancellation")]
    [SuppressMessage("ReSharper", "MethodHasAsyncOverloadWithCancellation")]
    private static async Task TorreControl(CancellationToken token)
    {
        // Da "chance" para que llegue al menos un avión, si no "mensaje" será un string vacío
        // y al hacer un Split tendrá error al intentar acceder a las partes del mensaje 
        await Task.Delay(1000);
        AnsiConsole.MarkupLine("[green]:satellite_antenna: Torre de control lista[/]");

        // Continúa operaciones mientras no se solicite que se detenga.
        while (!token.IsCancellationRequested)
        {
            // Espera a que haya comunicación con la torre.
            ComunicacionTorre.Wait();
            // Obtiene el mensaje y lo "decodifica".
            var mensaje = _solicitud.Split(",", StringSplitOptions.TrimEntries);
            // Libera la pista de maniobras.
            Pista.Release();
            // Libera la comunicacion con el avión.
            ComunicacionAvion.Release();
            AnsiConsole.MarkupLine($"[green]:satellite_antenna: Torre de control dice: {mensaje[0]} puede {mensaje[1]}.[/]");
        }

        AnsiConsole.MarkupLine("[green]:satellite_antenna: Las actividades han terminado... Por hoy.[/]");
    }

    [SuppressMessage("ReSharper", "MethodSupportsCancellation")]
    public static async Task Main(string[] args)
    {
        var options = new OptionSet()
        {
            { "a|aviones=", "Número de aviones a lanzar. Default = 15.", (int? i) => { _numeroAviones = i ?? _numeroAviones; } },
            { "p|pasajeros=", "Número de andenes de pasajeros. Default = 6.", (int? i) => { _nAndenesPasajeros = i ?? _nAndenesPasajeros; } },
            { "m|mercancia=", "Número de andenes de mercancía. Default = 2.", (int? i) => { _nAndenesMercancia = i ?? _nAndenesMercancia; } }
        };

        // Se añade la opción de ayuda.
        options.Add("h|help", "Show help", _ =>
        {
            options.WriteOptionDescriptions(Console.Out);
            Environment.Exit(0);
        });

        // Se procesan las entradas de la terminal.
        options.Parse(args);

        _andenPasajeros = new SemaphoreSlim(_nAndenesPasajeros);
        _andenMercancia = new SemaphoreSlim(_nAndenesMercancia);

        var salir = new CancellationTokenSource();
        var aviones = new List<Task>();
        // ReSharper disable once MethodSupportsCancellation
        // var torre = new Task(() => TorreControl(salir.Token));
        var torre = new Task(() => TorreControl(salir.Token));
        torre.Start();

        for (var i = 0; i < _numeroAviones; i++)
        {
            var tipo = Random.Shared.Next(0, 2) == 0 ? TipoAvion.Pasajeros : TipoAvion.Comercial;
            var id = i;
            var task = new Task(() => Avion(id, tipo));
            task.Start();
            AnsiConsole.MarkupLine($"[default]:red_exclamation_mark: Se lanzó un avión de tipo {tipo.ToString()}[/]");
            aviones.Add(task);
            await Task.Delay(Random.Shared.Next(500, 1000));
        }

        await Task.WhenAll(aviones);
        salir.Cancel();
        await torre;
    }
}