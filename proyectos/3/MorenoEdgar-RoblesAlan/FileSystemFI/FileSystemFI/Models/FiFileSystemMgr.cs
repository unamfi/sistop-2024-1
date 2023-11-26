using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Avalonia.Controls;
using FileSystemFI.Extensions;

// ReSharper disable PossibleLossOfFraction

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
            Files = GetAllFiles();
        }
        catch (Exception)
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

    public List<FiFile> GetAllFiles()
    {
        _br.BaseStream.Position = ClusterSize;
        Files.Clear();
        while (_br.BaseStream.Position < ClusterSize * 4)
        {
            var type = _br.ReadChar();
            var filename = _br.ReadString(14);
            var fileSize = _br.ReadInt32LitEnd();
            _br.ReadChars(1);
            var initCluster = _br.ReadInt32();
            var createDate = _br.ReadString(14);
            var modDate = _br.ReadString(14);
            _br.ReadChars(12);

            // if (filename == "..............") continue;
            if (type == '/') continue;

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


    public async Task<FiFile?> CopyFromComputer(string path)
    {
        await using var fs = new FileStream(path, FileMode.Open, FileAccess.Read);
        using var br = new BinaryReader(fs);

        var fileSize = fs.Length;

        var infoLocation = GetNextAvaiableFileInfo();
        if (infoLocation == -1)
            throw new Exception("No hay espacio para registrar el archivo.");
        var dataLocation = GetNextAvaiableDataSpace(fileSize);
        if (dataLocation == -1)
            throw new Exception("No hay espacio para almacenar el archivo.");

        var fileExt = Path.GetExtension(fs.Name);
        var fileName = Path.GetFileName(fs.Name).PadRight(14);
        if (fileName.Length > 14)
            fileName = fileName[..14];
        if (!fileName.Trim().EndsWith(fileExt))
            fileName = fileName[..^fileExt.Length] + fileExt;
        if (fileName.Length != 14)
            throw new Exception("Nombre del archivo inválido");
        if (Files.Any(c => c.FileName == path))
            throw new Exception("El archivo ya existe");

        var file = new FiFile
        {
            FileName = fileName,
            FirstCluster = (int)dataLocation / ClusterSize,
            Size = (int)fileSize,
            Type = '-',
            CreatedDate = File.GetCreationTime(path),
            LastModifiedDate = DateTime.Now
        };
        WriteFileData(file, infoLocation);

        _bw.BaseStream.Position = file.FirstCluster * ClusterSize;

        while (br.BaseStream.Position < br.BaseStream.Length)
            _bw.Write(br.ReadByte());

        return file;
    }

    public void DeleteFile(FiFile file)
    {
        // Eliminar los metadatos
        _br.BaseStream.Position = ClusterSize;
        var found = false;
        while (_br.BaseStream.Position < ClusterSize * 4)
        {
            var mdata = _br.ReadBytes(64);
            if (Encoding.ASCII.GetString(mdata[1..15]).Trim() != file.FileName) continue;
            found = true;
            break;
        }

        if (!found) throw new Exception("No se puede encontrar el archivo.");

        _bw.BaseStream.Position = _br.BaseStream.Position - 64;
        _bw.Write('/');
        _bw.Write(string.Join(string.Empty, Enumerable.Repeat('.', 14)));
        _bw.Write(Enumerable.Repeat((byte)0x0, 7).ToArray());
        _bw.Write(string.Join(string.Empty, Enumerable.Repeat(0, 28))); // Fechas en cero
        _bw.Write(Enumerable.Repeat((byte)0x0, 12).ToArray());

        // Eliminar los datos
        // ReSharper disable once PossibleLossOfFraction
        var usedClusters = (int)Math.Ceiling((double)(file.Size / ClusterSize)) - 1;
        _bw.BaseStream.Position = file.FirstCluster * ClusterSize;
        while (usedClusters > 0)
        {
            var prev = _bw.BaseStream.Position;
            _bw.Write(0x00);
            _bw.BaseStream.Position = prev + ClusterSize;
            usedClusters--;
        }

        Files = GetAllFiles();
    }

    public void Defrag()
    {
        Files = Files.OrderBy(f => f.FirstCluster).ToList(); // Ordenar los archivos por número de cluster
        var lastCluster = 0;
        for (var i = 0; i < Files.Count - 1; i++)
        {
            var file = Files[i];
            var usedClusters = (int)Math.Ceiling((double)(file.Size / ClusterSize)) - 1;

            if (i == 0)
            {
                lastCluster = usedClusters + 1;
                continue;
            }
            
            if (file.FirstCluster * ClusterSize == lastCluster) continue;

            var readPosition = (long) file.FirstCluster * ClusterSize;
            var writePosition = (long) ClusterSize * 4 + lastCluster;
            while (usedClusters > 0)
            {
                _br.BaseStream.Position = readPosition;
                var data = _br.ReadBytes(ClusterSize);
                readPosition = _br.BaseStream.Position;

                _bw.BaseStream.Position = writePosition;
                _bw.Write(data);
                writePosition = _bw.BaseStream.Position;
                
                usedClusters--;
            }

            Files[i].FirstCluster = lastCluster;
            lastCluster = usedClusters + 1;
        }
    }

    private void WriteFileData(FiFile file, long infoSpace)
    {
        _bw.BaseStream.Position = infoSpace;
        var buffer = new byte[64];
        var bufferIndex = 0;

        BitConverter.GetBytes(file.Type).CopyTo(buffer, bufferIndex);
        bufferIndex += 1;

        var fileNameBytes = Encoding.ASCII.GetBytes(file.FileName!);
        fileNameBytes.CopyTo(buffer, bufferIndex);
        bufferIndex += fileNameBytes.Length;

        BitConverter.GetBytes(file.Size).Reverse().ToArray().CopyTo(buffer, bufferIndex);
        bufferIndex += sizeof(int);

        // BitConverter.GetBytes((char)0).CopyTo(buffer, bufferIndex);
        buffer[bufferIndex] = 0x0;
        bufferIndex += 1;

        BitConverter.GetBytes(file.FirstCluster).CopyTo(buffer, bufferIndex);
        bufferIndex += sizeof(int);

        var createdDateBytes = file.CreatedDate.ToString("yyyyMMddHHmmss").ToCharArray().Select(c => (byte)c).ToArray();
        createdDateBytes.CopyTo(buffer, bufferIndex);
        bufferIndex += createdDateBytes.Length;

        var modDateBytes = file.LastModifiedDate.ToString("yyyyMMddHHmmss").ToCharArray().Select(c => (byte)c).ToArray();
        modDateBytes.CopyTo(buffer, bufferIndex);
        bufferIndex += modDateBytes.Length;

        if (bufferIndex > 0)
        {
            _bw.Write(buffer, 0, bufferIndex);
        }
    }

    private long GetNextAvaiableFileInfo()
    {
        _br.BaseStream.Position = ClusterSize;
        while (_br.BaseStream.Position < ClusterSize * 4)
        {
            var buffer = _br.ReadBytes(64);
            if (Encoding.ASCII.GetString(buffer[1..15]) == "..............")
                return _br.BaseStream.Position - 64;
        }

        return -1;
    }

    private long GetNextAvaiableDataSpace(long fileSize)
    {
        // ReSharper disable once PossibleLossOfFraction
        var requiredClusters = (int)Math.Ceiling((double)(fileSize / ClusterSize));
        if (requiredClusters == 0) requiredClusters = 1;
        if (requiredClusters > 720) return -1;
        var fileClusterCount = 0;
        var clusterCount = 0;
        long startPos = -1;
        _br.BaseStream.Position = ClusterSize * 4;
        while (_br.BaseStream.Position < _br.BaseStream.Length && fileClusterCount < requiredClusters && clusterCount < 720)
        {
            clusterCount++;
            if (startPos == -1)
                startPos = _br.BaseStream.Position;

            var cluster = _br.ReadBytes(ClusterSize);
            if (cluster[0] == 0x00)
            {
                fileClusterCount++;
            }
            else
            {
                startPos = -1;
                fileClusterCount = 0;
            }
        }

        return startPos;
    }

    public void ShowInitClustersContent()
    {
        _br.BaseStream.Position = ClusterSize * 4;
        while (_br.BaseStream.Position < _br.BaseStream.Length)
            Console.WriteLine((char)_br.ReadBytes(ClusterSize).First());
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