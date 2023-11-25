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
        public async Task CopyFileToFileSystemTest()
        {
            var fsm = new FiFileSystemMgr();
            try
            {
                fsm.OpenFileSystem(DestinationFileName);
                Assert.That(fsm.IsInitialized, Is.True);

                var file = await fsm.CopyFromComputer("./arch_logo.png");

                var files = fsm.GetAllFiles();
                Assert.That(files, Is.Not.Empty);
                Assert.That(files.Where(f => f.FileName == "arch_logo.png"), Is.Not.EqualTo(null));
            }
            catch (Exception e)
            {
                fsm.Dispose();
                Console.WriteLine(e);
                throw;
            }
        }
    }
}