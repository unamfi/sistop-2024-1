using System;
using System.Collections.ObjectModel;
using System.IO;
using System.Linq;
using System.Security.Principal;
using System.Text;
using System.Threading.Tasks;
using Avalonia.Controls;
using Avalonia.Controls.Models.TreeDataGrid;
using Avalonia.Media.Imaging;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using FileSystemFI.Services;
using Microsoft.Extensions.DependencyInjection;
using FileSystemFI.Extensions;
using FileSystemFI.Models;
using ReactiveUI;

namespace FileSystemFI.ViewModels;

public partial class MainWindowViewModel : ObservableObject
{
    [ObservableProperty] private string? _fileName = "No hay ningún archivo abierto";
    [ObservableProperty] private string? _infoString = "No hay un sistema de archivos montado.";
    [ObservableProperty] private bool _enabledManagementButtons = false;
    [ObservableProperty] private FiFileSystemMgr? _fsm = null;
    [ObservableProperty] private ObservableCollection<FiFile> _files = new();
    [ObservableProperty] private FiFile? _selectedFile = new();
    [ObservableProperty] private string? _fileInfo = string.Empty;
    [ObservableProperty] private bool _infoPanelEnabled = false;
    [ObservableProperty] private string _fileContent = string.Empty;
    [ObservableProperty] private Image _selectedImage = new Image();

    [ObservableProperty] private Bitmap? _imageSource;

    // Para estos hay maneras mucho mejor de hacerlo, pero no queda mucho tiempo :(
    [ObservableProperty] private bool _imageMode = false;
    [ObservableProperty] private bool _textMode = true;

    public MainWindowViewModel()
    {
        this.WhenAnyValue(f => f.SelectedFile)
            .Subscribe(f =>
            {
                if (Fsm is null || !Fsm.IsInitialized) return;
                if (SelectedFile is null) return;
                if (SelectedFile.FileName!.EndsWith("png") || SelectedFile.FileName!.EndsWith("jpg"))
                {
                    ImageSource = ReadImage();
                    ImageMode = true;
                    TextMode = false;
                }
                else
                {
                    FileContent = ReadFile();
                    ImageMode = false;
                    TextMode = true;
                }
            });
    }

    [RelayCommand]
    private async Task SaveFile()
    {
        if (Fsm is null || !Fsm.IsInitialized) return;
        if (SelectedFile is null) return;

        var filesService = App.Current?.Services?.GetService<IFileService>();
        if (filesService is null)
            throw new NullReferenceException("File Service does not exists.");

        var file = await filesService.SaveFileAsync(SelectedFile.FileName!);
        if (file is null) return;
        await using var fs = new FileStream(file.Path.AbsolutePath, FileMode.CreateNew, FileAccess.Write);
        await using var sw = new BinaryWriter(fs);
        sw.Write(Fsm.ReadFile(SelectedFile).ToArray());
    }

    [RelayCommand]
    private async Task OpenFile()
    {
        if (Fsm is not null && Fsm.IsInitialized)
            Fsm.Dispose();

        var filesService = App.Current?.Services?.GetService<IFileService>();
        if (filesService is null)
            throw new NullReferenceException("File Service does not exists.");

        var file = await filesService.OpenFileAsync();
        if (file is null) return;
        FileName = file.Path.AbsolutePath;
        if (ReadFileSystem())
        {
            var files = Fsm?.GetAllDirectories();
            if (files is null) return;
            Files = new ObservableCollection<FiFile>(files);
        }
    }

    [RelayCommand]
    public void CloseFile()
    {
        if (Fsm is null || !Fsm.IsInitialized) return;
        Fsm.Dispose();
        FileName = "";
        InfoString = "No hay un sistema de archivos montado.";
        Files.Clear();
        SelectedFile = new FiFile();
        EnabledManagementButtons = false;
        InfoPanelEnabled = false;
    }

    public string ReadFile()
    {
        if (Fsm is null || !Fsm.IsInitialized) return string.Empty;
        if (SelectedFile is null) return string.Empty;
        return Encoding.ASCII.GetString(Fsm.ReadFile(SelectedFile).ToArray());
    }

    private Bitmap? ReadImage()
    {
        if (Fsm is null || !Fsm.IsInitialized) return null;
        if (SelectedFile is null) return null;
        var imageBytes = Fsm.ReadFile(SelectedFile).ToArray();
        using var ms = new MemoryStream(imageBytes);
        return new Bitmap(ms);
    }

    private bool ReadFileSystem()
    {
        if (FileName is null) return false;
        Fsm = new FiFileSystemMgr();
        Fsm.OpenFileSystem(FileName);
        if (!Fsm.IsInitialized) return false;
        InfoString = $"Sistema de archivos: {Fsm.Identifier} {Fsm.Version} " +
                     $"| Etiqueta del volumen: {Fsm.Volume}" +
                     $"| Tamaño de cluster: {Fsm.ClusterSize} bytes.";
        EnabledManagementButtons = true;
        InfoPanelEnabled = true;
        return true;
    }
}