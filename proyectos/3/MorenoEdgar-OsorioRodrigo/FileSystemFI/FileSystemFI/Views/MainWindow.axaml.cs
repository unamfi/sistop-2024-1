using System;
using System.Threading.Tasks;
using Avalonia.Controls;
using Avalonia.Input;
using Avalonia.Interactivity;
using FileSystemFI.ViewModels;

namespace FileSystemFI.Views;

public partial class MainWindow : Window
{
    private MainWindowViewModel context = new MainWindowViewModel();
    public MainWindow()
    {
        DataContext = context;
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
        context.CloseFile();
        base.OnClosing(e);
    }
}