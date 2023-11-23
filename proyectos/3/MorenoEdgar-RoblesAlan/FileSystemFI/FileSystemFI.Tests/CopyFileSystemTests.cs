using System.IO;
using FileSystemFI.Models;
using NUnit.Framework;

namespace FileSystemFI.Tests
{
    public class CopyFileSystemTests
    {
        private const string SourceFileName = "./source_file.txt";
        private const string DestinationFileName = "./fiunamfs.img";

        [SetUp]
        public void Setup()
        {
        }

        [Test]
        public void CopyFileToFileSystemTest()
        {
            var fsm = new FiFileSystemMgr();
            
            fsm.OpenFileSystem(DestinationFileName);

            Assert.That(fsm.IsInitialized, Is.True);

            File.WriteAllText(SourceFileName, "Contenido de prueba.");

            var success = fsm.CopyFileToFileSystem(SourceFileName, "/copied_file.txt");

            Assert.That(success, Is.True);

            fsm.Dispose();
        }
    }
}