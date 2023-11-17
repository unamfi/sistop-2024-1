using FileSystemFI.Extensions;
using FileSystemFI.Models;

namespace FileSystemFI.Tests;

public class ReadBinTests
{
    private const string FileName = "./fiunamfs.img";

    [SetUp]
    public void Setup()
    {
    }

    [Test]
    public void FileManagerTest()
    {
        var fsm = new FiFileSystemMgr();
        fsm.OpenFileSystem(FileName);
        Assert.That(fsm.IsInitialized, Is.True);
        
        Console.WriteLine($"Sistema de archivos abierto: {fsm.Identifier} {fsm.Version}");
        Console.WriteLine($"Etiqueta: {fsm.Volume}");
        Console.WriteLine($"Tamaño de cluster: {fsm.ClusterSize} bytes.");
        Console.WriteLine($"Número de clusters que mide el directorio: {fsm.DirClusterSize} bytes.");
        Console.WriteLine($"Número de clusters que mide la unidad completa: {fsm.FullClusterSize}");

        var files = fsm.GetAllDirectories();
        files.ForEach(f => Console.WriteLine($"File: {f.FileName} | Created: {f.CreatedDate} | Size: {f.Size}"));
        Assert.True(files.Count > 0);
        
        fsm.Dispose();
    }
    
    [Test]
    public async Task ReadImgFile()
    {
        await using FileStream fs = new(FileName, FileMode.Open, FileAccess.Read);
        using BinaryReader br = new(fs);
        
        var fileSystem = new string(br.ReadChars(8));
        br.ReadChars(2);
        var version = new string(br.ReadChars(4));
        br.ReadChars(6);
        var volume = new string(br.ReadChars(19));
        var clusterSize = br.ReadInt32();
        var dirClusterSize = br.ReadInt32LitEnd();
        var totalCluster = br.ReadInt32LitEnd();

        Console.WriteLine($"File system: {fileSystem} {version}");
        Console.WriteLine($"Volume label: {volume}");
        Console.WriteLine($"Cluster size = {clusterSize}");
        Console.WriteLine($"Directory Cluster size = {dirClusterSize}");
        Console.WriteLine($"Full cluster size = {totalCluster}");
        
        Assert.That(fileSystem, Is.EqualTo("FiUnamFS"));
    }
}