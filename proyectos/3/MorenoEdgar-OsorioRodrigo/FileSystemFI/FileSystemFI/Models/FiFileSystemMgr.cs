using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using FileSystemFI.Extensions;

namespace FileSystemFI.Models;

public class FiFileSystemMgr : IDisposable
{
    private FileStream? _fs;
    private BinaryReader? _br;
    private BinaryWriter? _bw;

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
            var initCluster = _br.ReadInt32LitEnd();
            var createDate = _br.ReadString(14);
            var modDate = _br.ReadString(14);
            _br.ReadChars(12);

            if (filename == "..............") continue;

            var file = new FiFile
            {
                Type = type,
                FileName = filename,
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