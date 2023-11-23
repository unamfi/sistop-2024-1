using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using FileSystemFI.Extensions;

namespace FileSystemFI.Models;

public class FiFileSystemMgr : IDisposable
{
    private FileStream _fs = null!;
    private BinaryReader _br = null!;
    private BinaryWriter _bw = null!;

    /// <summary>
    /// Abre el sistema de archivos y crea el lector y el escritor binario para
    /// leer/manipular el archivo.
    /// </summary>
    /// <param name="filePath">Ruta al archivo .img</param>
    public void OpenFileSystem(string filePath)
    {
        _fs = new FileStream(filePath, FileMode.Open, FileAccess.ReadWrite);
        _br = new BinaryReader(_fs);
        _bw = new BinaryWriter(_fs);
        try
        {
            Identifier = _br.ReadString(8);
            if (Identifier != "FiUnamFS")
                throw new Exception("El sistema de archivos no es válido (Debe ser FiUnamFS)");
            _br.ReadBytes(2);
            Version = _br.ReadString(4);
            _br.ReadBytes(6);
            Volume = _br.ReadString(19);
            ClusterSize = _br.ReadInt32LitEnd();
            DirClusterSize = _br.ReadInt32LitEnd();
            FullClusterSize = _br.ReadInt32LitEnd();

            IsInitialized = true;
        }
        catch (Exception e)
        {
            IsInitialized = false;
            Dispose();
            throw;
        }
    }

    public IEnumerable<byte> ReadFile(FiFile file)
    {
        var start = file.FirstCluster * ClusterSize;
        if (start >= _br.BaseStream.Length)
            throw new Exception("Posición de lectura inválida");
        _br.BaseStream.Position = start;
        return _br.ReadBytes(file.Size);
    }

    public List<FiFile> GetAllDirectories()
    {
        _br.BaseStream.Position = ClusterSize;

        while (_br.BaseStream.Position <= ClusterSize * 4)
        {
            var type = _br.ReadChar();
            var filename = _br.ReadString(14);
            var fileSize = _br.ReadInt32LitEnd();
            _br.ReadChars(1);
            var initCluster = _br.ReadInt32();
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

            Files.Add(file);
        }

        return Files;
    }


    public async Task<FiFile?> CreateNewFile(string path)
    {
        if (Files.Any(c => c.FileName == path))
            throw new Exception("El archivo ya existe");

        await using var fs = new FileStream(path, FileMode.Open, FileAccess.Read);
        using var br = new BinaryReader(fs);

        var fileSize = fs.Length;

        var infoLocation = GetNextAvaiableFileInfo();
        if (infoLocation == -1)
            throw new Exception("No hay espacio para registrar el archivo.");
        var dataLocation = GetNextAvaiableDataSpace(fileSize);
        if (dataLocation == -1)
            throw new Exception("No hay espacio para almacenar el archivo.");
        dataLocation /= ClusterSize;

        _br.BaseStream.Position = dataLocation * ClusterSize;
        Console.WriteLine(_br.ReadString(50000));

        return null;
    }

    private long GetNextAvaiableFileInfo()
    {
        _br.BaseStream.Position = ClusterSize;
        while (true)
        {
            var buffer = _br.ReadBytes(64);
            if (Encoding.ASCII.GetString(buffer[1..15]) == "..............")
                return _br.BaseStream.Position;
            if (_br.BaseStream.Position >= ClusterSize * 4)
                break;
        }

        return -1;
    }

    private long GetNextAvaiableDataSpace(long fileSize)
    {
        var remaining = fileSize;
        _br.BaseStream.Position = ClusterSize * 4;
        while (_br.ReadByte() is var c)
        {
            if (c == 0x00)
                remaining--;
            else
                remaining = fileSize;

            if (remaining == 0)
                return _br.BaseStream.Position - fileSize;
        }

        return -1;
    }

    public string? Identifier { get; private set; }
    public string? Version { get; private set; }
    public string? Volume { get; private set; }
    public int ClusterSize { get; private set; }
    public int DirClusterSize { get; private set; }
    public int FullClusterSize { get; private set; }
    public bool IsInitialized { get; private set; } = false;

    private List<FiFile> Files { get; set; } = new();

    public void Dispose()
    {
        IsInitialized = false;
        _fs.Dispose();
        _br.Dispose();
        _bw.Dispose();
        GC.SuppressFinalize(this);
    }
}