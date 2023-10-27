using Spectre.Console;

namespace Tarea2;

/// <summary>
/// Utilidades para el color de texto en terminal.
/// </summary>
public abstract class ColorUtils
{
    /// <summary>
    /// Obtiene el color complementario de un color dado.
    /// </summary>
    /// <param name="color">Color inicial</param>
    /// <returns>Color complementario</returns>
    public static Color GetComplementaryColor(Color color)
    {
        var r = (byte)(255 - color.R);
        var g = (byte)(255 - color.G);
        var b = (byte)(255 - color.B);
        return new Color(r, g, b);
    }

    /// <summary>
    /// Obtiene un color aleatorio.
    /// </summary>
    /// <returns>Spectre.Color</returns>
    public static Color GetRandomColor()
    {
        var r = (byte)Random.Shared.Next(0, 255);
        var g = (byte)Random.Shared.Next(0, 255);
        var b = (byte)Random.Shared.Next(0, 255);
        return new Color(r, g, b);
    }

    /// <summary>
    /// Obtiene el listado de colores de Spectre.Console a partir de las propiedades de Spectre.Console.Color.
    /// Los colores se encuentran en un struct parcial generado aparte (Color.Generated.cs si se utiliza alguna
    /// herramienta externa).
    /// Al final no usé esto y opté por un color aleatorio (con limitaciones en algunas terminales).
    /// </summary>
    /// <returns>Lista de colores</returns>
    /// <exception cref="InvalidOperationException">Error al obtener las propiedades</exception>
    // ReSharper disable once UnusedMember.Global
    public static List<Color> GetColorList()
    {
        return (from prop in typeof(Color).GetProperties()
            let type = Nullable.GetUnderlyingType(prop.PropertyType) ?? prop.PropertyType
            where type == typeof(Color)
            select (Color)(prop.GetValue(prop, null) ?? throw new InvalidOperationException())).ToList();
    }
}