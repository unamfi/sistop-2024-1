using System.Diagnostics.CodeAnalysis;
/* Edgar says: Esta biblioteca permite escribir en terminal de una manera un poco
 * más avanzada que solo con la salida normal de C#.
 * https://spectreconsole.net
 */
using Spectre.Console;

// ReSharper disable MethodSupportsCancellation
// ReSharper disable InconsistentNaming

namespace sistop;

/// <summary>
/// Esta clase ejecuta el ejercicio de sincronización: "De gatos y ratones".
/// </summary>
[SuppressMessage("Reliability",
    "CA2016:Forward the \'CancellationToken\' parameter to methods")] // Esto es necesario para ignorar algunas advertencias del IDE que utilizo.
public class CatsAndRats
{
    public CatsAndRats(int conteoGatos, int conteoRatones, int platosComedor)
    {
        this.conteoGatos = conteoGatos;
        this.conteoRatones = conteoRatones;
        gatoMutex = new SemaphoreSlim(1);
        ratonMutex = new SemaphoreSlim(1);
        hayRatones = new SemaphoreSlim(1);
        platos = new SemaphoreSlim(platosComedor);
    }

    private readonly int conteoGatos; // Conteo de gatos que habrá
    private readonly int conteoRatones; // Conteo de ratones que habrá

    private int ratones; // Ratones comiendo
    private int gatos; // Gatos comiendo

    private readonly SemaphoreSlim gatoMutex; // Mutex para los gatos
    private readonly SemaphoreSlim ratonMutex; // Mutex para los ratones
    private readonly SemaphoreSlim platos; // Mutex para los platos
    private readonly SemaphoreSlim hayRatones; // Mutex para que los gatos esperen mientras comen los ratones...

    /// <summary>
    /// Esta función representa a un gato.
    /// </summary>
    /// <param name="id">Este es el "nombre" del gato</param>
    /// <param name="salir">El Token de cancelación es necesario para
    /// poder detener la función cuando no haya más ratones</param>
    private void Gato(int id, CancellationToken salir)
    {
        AnsiConsole.MarkupLine($":grinning_cat: ¡Gato {id} entra a la sala!"); // Solo avisa que ha comenzado su ejecución

        // Mientras haya ratones, este ciclo estará ejecutándose
        while (!salir.IsCancellationRequested)
        {
            hayRatones.Wait(); // Si hay ratones, espera unos momentos...
            hayRatones.Release(); // ¡A comer!

            platos.Wait(); // Gato toma un plato.
            ratonMutex.Wait(); // Esto solo es para mostrar que no hay ratones.
            AnsiConsole.MarkupLine($"[black on aqua]:grinning_cat: {id} Dice: \"¡Ya puedo comer!\" Hay {ratones} ratones comiendo.[/]");
            ratonMutex.Release();

            gatoMutex.Wait(); // Aumenta el contador de gatos comiendo
            gatos++;
            gatoMutex.Release();

            // Come sus croquetas (¡No Whiskas por favor!)
            AnsiConsole.MarkupLine($":grinning_cat: [aqua]Gato {id} está comiendo en {platos.CurrentCount}[/]");
            // Tarda un poco en comer...
            Task.Delay(Random.Shared.Next(0, 200)).Wait();

            gatoMutex.Wait(); // Se retira y decrementa el contador de gatos comiendo
            gatos--;
            gatoMutex.Release();
            platos.Release();

            AnsiConsole.MarkupLine($":cat: [blue]Gato {id} regreza a dormir :zzz:[/]");
        }
    }

    /// <summary>
    /// Esta función representa un ratón.
    /// </summary>
    /// <param name="id">Este es el "nombre" del ratón</param>
    private void Raton(int id)
    {
        AnsiConsole.MarkupLine($":rat: ¡Ratón {id} entra a la sala!"); // Indica que comienza su ejecución.
        var vivo = true; // Comienza estando vivo.
        while (vivo)
        {
            Task.Delay(Random.Shared.Next(0, 2000)).Wait(); // Espera un poco para ir a comer...
            platos.Wait(); // El ratón toma un plato.
            ratonMutex.Wait(); // Aumenta el número de ratones comiendo
            ratones++;
            if (ratones == 1) // Si hay un ratón, avisa al gato para que no se lo coma.
                hayRatones.Wait();
            ratonMutex.Release();

            // Come (¡Bastante rápido!)
            AnsiConsole.MarkupLine($"[black on lime]:rat: {id} Dice: \"¡Espero que pueda comer en paz!\".[/]");
            AnsiConsole.MarkupLine($"[lime]:rat: Ratón {id} está comiendo en {platos.CurrentCount}[/]");

            gatoMutex.Wait(); // Revisa si un gato ha llegado mientras comía
            if (gatos > 0)
            {
                vivo = false; // ¡El ratón ha muerto en las garras del gato!.
                // Además, de esta manera indicamos que el ratón ya no se volverá a "ejecutar",
                // pero continúa la ejecución hasta el final para liberar los semáforos que haya ocupado.
                AnsiConsole.MarkupLine($"[black on red]:skull: ¡El ratón {id} ha sido aniquilado![/]");
            }

            gatoMutex.Release();

            ratonMutex.Wait(); // Decrementa el número de ratones
            ratones--;
            if (ratones == 0) // Si ya no hay ratones, avisa al gato que ya puede pasar.
                hayRatones.Release();
            ratonMutex.Release();
            platos.Release(); // El ratón libera el plato.

            if (vivo) // Si sigue vivo, puede regresar a su refugio.
                AnsiConsole.MarkupLine($":rat: [green]Ratón {id} regreza a refugiarse.[/]");
        }
    }

    /// <summary>
    /// Comienza la ejecución del programa.
    /// </summary>
    public async Task Start()
    {
        // Listas con los hilos de gatos y ratones.
        var threadsGatos = new List<Task>();
        var threadsRatones = new List<Task>();

        // Token de cancelación para cuando ya no haya ratones.
        var salir = new CancellationTokenSource();

        // Se inican los procesos de los gatos.
        for (var i = 0; i < conteoGatos; i++)
        {
            var id = i + 1; // Asignación del "nombre"
            var gato = new Task(() => Gato(id, salir.Token)); // Creación del proceso.
            threadsGatos.Add(gato); // Se añade a la lista de procesos.
            gato.Start(); // Se ejecuta el proceso.
        }

        // Procesos para los ratones.
        for (var i = 0; i < conteoRatones; i++)
        {
            var id = i + 1;
            var raton = new Task(() => Raton(id));
            threadsRatones.Add(raton);
            raton.Start();
        }

        // Task.WhenAll se queda a la espera de que todos los procesos de "ratones" hayan terminado.
        await Task.WhenAll(threadsRatones);
        AnsiConsole.MarkupLine("¡Ya no quedan ratones en la sala! :skull:");

        // Se lanza el aviso a los gatos para que detengan su ejecución.
        salir.Cancel();
        // Espera a que salgan todos, y termina el programa.
        await Task.WhenAll(threadsGatos);
        AnsiConsole.MarkupLine("¡Ganan los gatos! :cat_with_wry_smile: :3");
    }
}