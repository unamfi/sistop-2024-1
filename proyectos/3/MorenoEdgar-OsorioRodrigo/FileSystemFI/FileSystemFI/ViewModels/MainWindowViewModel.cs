using System;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using FileSystemFI.Services;
using Microsoft.Extensions.DependencyInjection;
using FileSystemFI.Extensions;

namespace FileSystemFI.ViewModels;

public partial class MainWindowViewModel : ObservableObject
{
    [ObservableProperty] private string? _fileName;
    [ObservableProperty] private string? _infoString = "No hay un sistema de archivos montado.";
    [ObservableProperty] private bool _enabledManagementButtons = false;
    [ObservableProperty] private FileSystemManager? _fsm = null;

    [RelayCommand]
    private async Task OpenFile()
    {
        var filesService = App.Current?.Services?.GetService<IFileService>();
        if (filesService is null)
            throw new NullReferenceException("File Service does not exists.");

        var file = await filesService.OpenFileAsync();
        if (file is null) return;
        FileName = file.Path.AbsolutePath;
        await ReadFile();
    }

    private async Task ReadFile()
    {
        if (FileName is null) return;
        Fsm = new FileSystemManager();
        await Fsm.OpenFileSystem(FileName);
        if (!Fsm.IsInitialized) return;
        InfoString = $"Sistema de archivos: {Fsm.Identifier} " +
                     $"Versión {Fsm.Version} | Tamaño de cluster: {Fsm.ClusterSize} bytes.";
    }
}