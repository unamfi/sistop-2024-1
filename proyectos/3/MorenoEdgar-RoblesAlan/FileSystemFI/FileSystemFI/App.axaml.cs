using System;
using Avalonia;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Markup.Xaml;
using FileSystemFI.Services;
using FileSystemFI.ViewModels;
using FileSystemFI.Views;
using HotAvalonia;
using Microsoft.Extensions.DependencyInjection;

namespace FileSystemFI;

public partial class App : Application
{
    public override void Initialize()
    {
        this.EnableHotReload();
        AvaloniaXamlLoader.Load(this);
    }

    public override void OnFrameworkInitializationCompleted()
    {
        if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
        {
            desktop.MainWindow = new MainWindow
            {
                DataContext = new MainWindowViewModel(),
            };

            var services = new ServiceCollection();

            services.AddSingleton<IFileService, FileService>(_ => new FileService(desktop.MainWindow));

            Services = services.BuildServiceProvider();
        }

        base.OnFrameworkInitializationCompleted();
    }

    public new static App? Current => Application.Current as App;
    public IServiceProvider? Services { get; private set; }
}