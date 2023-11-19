using System;
using System.Collections.ObjectModel;
using System.IO;
using System.Linq;
using System.Security.Principal;
using System.Text;
using System.Threading.Tasks;
using Avalonia.Controls;
using Avalonia.Controls.Models.TreeDataGrid;
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
    public HierarchicalTreeDataGridSource<FiFile>? Source { get; set; }

    public MainWindowViewModel()
    {
        this.WhenAnyValue(f => f.SelectedFile)
            .Subscribe(f =>
            {
                if (Fsm is null || !Fsm.IsInitialized) return;
                if (SelectedFile is null) return;
                FileContent = Encoding.ASCII.GetString(Fsm.ReadFile(SelectedFile).ToArray());
            });
        // this.WhenAnyValue(f => f.Files)
        //     .Subscribe(x =>
        //     {
        //         Source = new HierarchicalTreeDataGridSource<FiFile>(Files)
        //         {
        //             Columns =
        //             {
        //                 new HierarchicalExpanderColumn<FiFile>(
        //                     new TextColumn<FiFile, string>("Nombre del archivo", x => x.FileName),
        //                     x => x.Children
        //                 ),
        //                 new TextColumn<FiFile,string>("File Size", x => $"{x.MbSize:0.00} MB"),
        //                 // new TextColumn<FiFile,string>("Creation", x => x.CreatedDate.ToString("MM/dd/yyyy hh:mm:ss"))
        //             }
        //         };
        //     });
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

    [RelayCommand]
    public void ReadFile()
    {
        if (Fsm is null || !Fsm.IsInitialized) return;
        if (SelectedFile is null) return;
        FileContent = Encoding.ASCII.GetString(Fsm.ReadFile(SelectedFile).ToArray());
    }

    private bool ReadFileSystem()
    {
        if (FileName is null) return false;
        Fsm = new FiFileSystemMgr();
        Fsm.OpenFileSystem(FileName);
        if (!Fsm.IsInitialized) return false;
        InfoString = $"Sistema de archivos: {Fsm.Identifier} {Fsm.Version} " +
                     $"| Tamaño de cluster: {Fsm.ClusterSize} bytes.";
        EnabledManagementButtons = true;
        InfoPanelEnabled = true;
        return true;
    }
}