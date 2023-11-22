using System;
using System.Collections.ObjectModel;

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
    public double MbSize => (Size / 1024.0) / 1024.0;
    public int FirstCluster { get; set; }
    public DateTime CreatedDate { get; set; }
    public DateTime LastModifiedDate { get; set; }
    public int UnusedSpace { get; set; }
    public ObservableCollection<FiFile> Children { get; } = new();
}