using FileSystemFI.Models;

namespace FileSystemFI.Tests;

public class WriteFileSystemTests
{
    private const string FileName = "./fiunamfs.img";

    [SetUp]
    public void Setup()
    {
    }

    [Test]
    public void SaveNewFileTest()
    {
        var fsm = new FiFileSystemMgr();
        fsm.OpenFileSystem(FileName);
        Assert.That(fsm.IsInitialized, Is.True);
        var files = fsm.GetAllDirectories();
        Assert.That(files, Is.Not.Empty);

        var file = fsm.CopyFromComputer("/home/ayame/Desktop/arch_logo.png");
        Assert.That(file, Is.Not.Null);
    }
}