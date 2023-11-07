namespace Tarea2.Extensions;

/// <summary>
/// Extensiones para IEnumerable.
/// </summary>
public static class EnumerableExtensions
{
    public static void ForEach<T>(this IEnumerable<T> @this, Action<T> action)
    {
        foreach (var item in @this)
            action(item);
    }
}