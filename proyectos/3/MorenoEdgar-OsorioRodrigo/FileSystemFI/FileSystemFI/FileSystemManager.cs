using System;
using System.IO;
using System.Threading.Tasks;
using FileSystemFI.Extensions;

namespace FileSystemFI;

public class FileSystemManager : IDisposable
{
    private FileStream? _fs;
    private BinaryReader? _br;
    private BinaryWriter? _bw;

    public async Task OpenFileSystem(string filePath)
    {
        _fs = new FileStream(filePath, FileMode.Open, FileAccess.ReadWrite);
        _br = new BinaryReader(_fs);
        _bw = new BinaryWriter(_fs);
        try
        {
            Identifier = _br.ReadString(8);
            _br.ReadBytes(2);
            Version = _br.ReadString(4);
            _br.ReadBytes(6);
            Volume = _br.ReadString(19);
            ClusterSize = _br.ReadInt32LitEnd();
            DirClusterSize = _br.ReadInt32LitEnd();
            FullClusterSize = _br.ReadInt32LitEnd();

            IsInitialized = true;
        }
        catch (Exception)
        {
            IsInitialized = false;
            Dispose();
        }
    }

    public string? Identifier { get; private set; }
    public string? Version { get; private set; }
    public string? Volume { get; private set; }
    public int ClusterSize { get; private set; }
    public int DirClusterSize { get; private set; }
    public int FullClusterSize { get; private set; }
    public bool IsInitialized { get; private set; } = false;

    public void Dispose()
    {
        _fs.Dispose();
        _br.Dispose();
        _bw.Dispose();
        GC.SuppressFinalize(this);
    }
}