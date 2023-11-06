using Spectre.Console;

namespace Tarea2;

public class Process
{
    public string? Nombre { get; init; }

    /// <summary>
    /// Tiempo del procesador = t
    /// </summary>
    public int Ticks { get; init; }

    public int ConteoTicks { get; set; }
    public int Llegada { get; set; }

    /// <summary>
    /// TiempoRespuesta = T
    /// </summary>
    public int TiempoRespuesta { get; set; }

    public int TiempoEspera { get; set; }
    public double Penalizacion { get; set; }
    public int Inicio { get; set; }
    public int Final { get; set; }
    public Color Color { get; set; } = Color.Default;
    public Color BgColor { get; set; } = Color.Default;
    public double Prioridad { get; set; }

    /// <summary>
    /// Reinicia los valores para cada que se ejecuten los algoritmos.
    /// </summary>
    public void ResetValues()
    {
        TiempoEspera = 0;
        TiempoRespuesta = 0;
        Penalizacion = 0;
        Inicio = 0;
        Final = 0;
    }

    public override string ToString() => $"Proceso: {Nombre} [Prioridad {Prioridad}]";
}