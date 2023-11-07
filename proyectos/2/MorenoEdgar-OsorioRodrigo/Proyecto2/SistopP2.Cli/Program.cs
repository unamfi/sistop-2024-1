namespace SistopP2.Cli;

internal static class Program
{
    private static readonly SemaphoreSlim PistaAterrizaje = new(0);
    private static readonly SemaphoreSlim Radio = new(1);
    private static readonly SemaphoreSlim Control = new(0);
    private static readonly SemaphoreSlim AndenPasajeros = new(10);
    private static readonly SemaphoreSlim AndenMercancia = new(6);
    
    /// <summary>
    /// Un enum para indicar de que tipo es un avión, si de carga o de pasajeros.
    /// </summary>
    public enum TipoAvion
    {
        Carga,
        Pasajeros
    }

    /// <summary>
    /// Representa un avión.
    /// </summary>
    /// <param name="id">ID del avión</param>
    /// <param name="tipo">Tipo de avión</param>
    public static void Avion(int id, TipoAvion tipo)
    {
        var anden = tipo == TipoAvion.Carga ? AndenMercancia : AndenPasajeros;
    }

    /**
     * Representa la torre de control para comunicarse con los aviones.
     */
    public static void TorreControl()
    {
        
    }
    
    public static void Main(string[] args)
    {
    }
}