using System.Threading.Tasks;
using Avalonia.Controls;
using Avalonia.Platform.Storage;

namespace FileSystemFI.Services;

public class FileService : IFileService
{
    private readonly Window _target;

    public static FilePickerFileType Img { get; } = new("All img files")
    {
        Patterns = new[] { "*.img" }
    };

    public FileService(Window target)
    {
        _target = target;
    }

    public async Task<IStorageFile?> OpenFileAsync()
    {
        var files = await _target.StorageProvider.OpenFilePickerAsync(new FilePickerOpenOptions()
        {
            Title = "Selecciona el archivo de imagen",
            AllowMultiple = false,
            FileTypeFilter = new[] { Img }
        });

        return files.Count >= 1 ? files[0] : null;
    }

    public async Task<IStorageFile?> SaveFileAsync()
    {
        var file = await _target.StorageProvider.SaveFilePickerAsync(new FilePickerSaveOptions()
        {
            Title = "Exportar archivo"
        });
        return file;
    }

    public async Task<IStorageFile?> SaveFileAsync(string fileName)
    {
        var file = await _target.StorageProvider.SaveFilePickerAsync(new FilePickerSaveOptions()
        {
            Title = "Exportar archivo",
            SuggestedFileName = fileName
        });
        return file;
    }
}