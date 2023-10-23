using sistop;
using Mono.Options; // Opciones del programa
using Spectre.Console; // Manejo de la terminal

// Variables para los gatos, ratones y platos, por defecto estos son 5.
var conteoGatos = 5;
var conteoRatones = 5;
var platosComedor = 5;

// Opciones para el programa
var options = new OptionSet()
{
    { "g|gatos=", "Conteo de gatos. Default = 5.", (int? i) => { conteoGatos = i ?? conteoGatos; } },
    { "r|ratones=", "Conteo de ratones. Default = 5.", (int? i) => { conteoRatones = i ?? conteoRatones; } },
    { "p|platos=", "Número de platos disponibles. Default = 5.", (int? i) => { platosComedor = i ?? platosComedor; } }
};

// Se añade la opción de ayuda.
options.Add("h|help", "Show help", _ =>
{
    options.WriteOptionDescriptions(Console.Out);
    Environment.Exit(0);
});

// Se procesan las entradas de la terminal.
options.Parse(args);

// Creación del objeto para la ejecución del ejercicio.
var catsAndRats = new CatsAndRats(conteoGatos, conteoRatones, platosComedor);
// ¡Se lanza el progama!
await catsAndRats.Start();

/*
 * Esto es para el cartel final.
 */
var panel = new Panel(
    new Rows(
        Align.Center(
            new Markup("[red] Facultad de Ingeniería - UNAM [/]"), VerticalAlignment.Middle
        ),
        Align.Center(
            new Markup("Moreno Chalico Edgar Ulises"), VerticalAlignment.Middle
        ),
        Align.Center(
            new Markup("Osorio Ángeles Rodrigo Jafet"), VerticalAlignment.Middle
        ),
        Align.Center(
            new Markup("Sistemas Operativos - Semestre 2023-1"), VerticalAlignment.Middle
        )
    ))
{
    Border = BoxBorder.Rounded,
    Expand = true,
    Header = new PanelHeader("¡Gatos y Ratones!", Justify.Center)
};
AnsiConsole.Write(panel);