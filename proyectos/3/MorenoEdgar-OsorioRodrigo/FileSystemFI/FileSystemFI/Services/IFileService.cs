using System.Threading.Tasks;
using Avalonia.Platform.Storage;

namespace FileSystemFI.Services;

public interface IFileService
{
    public Task<IStorageFile?> OpenFileAsync();
}