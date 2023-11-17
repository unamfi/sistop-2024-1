using System;

namespace FileSystemFI.Models;

internal enum FileType
{
    Directory = 0x2d,
    Empty = 0x0f
}

public class FiFile
{
    public char Type { get; set; }
    public string? FileName { get; set; }
    public int Size { get; set; }
    public int FirstCluster { get; set; }
    public DateTime CreatedDate { get; set; }
    public DateTime LastModifiedDate { get; set; }
    public int UnusedSpace { get; set; }
}