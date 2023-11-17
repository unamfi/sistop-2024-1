using System;
using System.IO;
using System.Linq;

namespace FileSystemFI.Extensions;

public static class BinaryReaderExtensions
{
    public static string ReadString(this BinaryReader br, int charCount) => new string(br.ReadChars(charCount));

    public static int ReadInt32LitEnd(this BinaryReader br) =>
        BitConverter.ToInt32(br.ReadBytes(4).Reverse().ToArray(), 0);
}