using System;
using System.Threading.Tasks;
using Avalonia.Controls;
using Avalonia.Input;
using Avalonia.Interactivity;
using FileSystemFI.ViewModels;

namespace FileSystemFI.Views;

public partial class MainWindow : Window
{
    private readonly MainWindowViewModel _context = new();
    public MainWindow()
    {
        DataContext = _context;
        InitializeComponent();
    }

    private async void OnAboutClick(object? sender, RoutedEventArgs e)
    {
        var dialog = new AboutWindow();
        await dialog.ShowDialog(this);
    }

    private void OnCloseClick(object? sender, RoutedEventArgs e) => Close();

    protected override void OnClosing(WindowClosingEventArgs e)
    {
        _context.CloseFileSystem();
        base.OnClosing(e);
    }
}