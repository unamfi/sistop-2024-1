using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using FileSystemFI.Extensions;

namespace FileSystemFI.Models;

public class FiFileSystemMgr : IDisposable
{
    private FileStream _fs = null!;
    private BinaryReader _br = null!;
    private BinaryWriter _bw = null!;

    /// <summary>
    /// TODO: Esto debe quedar en el constructor de la clase.
    /// </summary>
    /// <param name="filePath"></param>
    public void OpenFileSystem(string filePath)
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

    public IEnumerable<byte> ReadFile(FiFile file)
    {
        var start = file.FirstCluster * ClusterSize;
        if (start >= _br.BaseStream.Length)
            throw new Exception("Posición de lectura inválida");
        _br.BaseStream.Position = start;

        var sb = new List<byte>();
        while (_br.ReadByte() is var c)
        {
            if (c == 0x00) break;
            sb.Add(c);
        }

        return sb;
    }

    public List<FiFile> GetAllDirectories()
    {
        _br.BaseStream.Position = ClusterSize;
        List<FiFile> files = new();

        while (_br.BaseStream.Position <= ClusterSize * 4)
        {
            var type = _br.ReadChar();
            var filename = _br.ReadString(14);
            var fileSize = _br.ReadInt32LitEnd();
            _br.ReadChars(1);
            // Mide 3 bytes, no 4
            var initCluster = _br.ReadInt32();
            // var initClusterTemp = _br.ReadBytes(3);
            // var initClusterBytes = new byte[initClusterTemp.Length + 1];
            // initClusterBytes[0] = 0x00;
            // Array.Copy(initClusterTemp, 0, initClusterBytes, 1, initClusterTemp.Length);
            // var initCluster = BitConverter.ToInt32(initClusterBytes); 

            // _br.ReadChar();
            var createDate = _br.ReadString(14);
            var modDate = _br.ReadString(14);
            _br.ReadChars(12);

            if (filename == "..............") continue;

            var file = new FiFile
            {
                Type = type,
                FileName = filename.Trim(),
                Size = fileSize,
                FirstCluster = initCluster,
                CreatedDate = DateTime.ParseExact(createDate, "yyyyMMddHHmmss", CultureInfo.InvariantCulture),
                LastModifiedDate = DateTime.ParseExact(modDate, "yyyyMMddHHmmss", CultureInfo.InvariantCulture)
            };

            files.Add(file);
        }

        return files;
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
        IsInitialized = false;
        _fs.Dispose();
        _br.Dispose();
        _bw.Dispose();
        GC.SuppressFinalize(this);
    }
}