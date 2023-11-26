using System.IO;
using System.Linq;
using static System.BitConverter;

namespace FileSystemFI.Extensions;

public static class BinaryWriterExtensions
{
    public static void WriteInt32LitEnd(this BinaryWriter bw, int value)
    {
        var bytes = GetBytes(value).Reverse().ToArray();
        bw.Write(bytes);
    }
}