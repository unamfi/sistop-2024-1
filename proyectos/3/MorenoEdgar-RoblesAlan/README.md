# Proyecto 3: (Micro) sistema de archivos

- Moreno Chalico Edgar Ulises
- Robles Reyes Alan

## Problema a resolver
## Entorno y dependencias

El programa está desarrollado en C# (.NET 7).
Para la interfaz de usuario se utilizó [Avalonia](https://avaloniaui.net), un framework de interfaz de usuario que al igual que .NET, es de código abierto, el cual permite desarrollar aplicaciones de escritorio multiplataforma que se ejecutan en Windows, Linux, MacOS, Android, iOS, web y en dispositivos embebidos. Este está basado en el patrón _model-view-viewmodel_ (MVVM).

Para agilizar el desarrollo con este patrón, se utilizó además la biblioteca [CommunityToolkit.Mvvm](https://github.com/CommunityToolkit/dotnet), y como tema para la aplicación se utilizó [Material.Avalonia](https://github.com/AvaloniaCommunity/Material.Avalonia).

Adicionalmente, se agregaron pruebas unitarias con [NUnit](https://nunit.org/), estas se utilizaron para ir probando los cambios en el programa de una manera más rápida sin depender de la GUI, así como para comprobar que todo se mantenga funcionando correctamente.

## Uso del programa