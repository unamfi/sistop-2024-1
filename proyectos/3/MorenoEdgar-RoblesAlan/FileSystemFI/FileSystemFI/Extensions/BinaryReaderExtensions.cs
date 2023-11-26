using System;
using System.IO;
using System.Linq;

namespace FileSystemFI.Extensions;

public static class BinaryReaderExtensions
{
    /// <summary>
    /// Lee una cadena desde el buffer del archivo binario.
    /// </summary>
    /// <param name="br"><see cref="BinaryReader"/></param>
    /// <param name="charCount">Conteo de caracteres a leer.</param>
    /// <returns><see cref="string"/></returns>
    public static string ReadString(this BinaryReader br, int charCount) => new(br.ReadChars(charCount));

    /// <summary>
    /// Ontiene un entero de 32 bits desde el buffer del archivo binario,
    /// en formato Little Endian.
    /// </summary>
    /// <param name="br"><see cref="BinaryReader"/>></param>
    /// <returns><see cref="Int32"/></returns>
    public static int ReadInt32LitEnd(this BinaryReader br) =>
        BitConverter.ToInt32(br.ReadBytes(4).Reverse().ToArray(), 0);
}