## Proyecto3: Micro Sistemas de Archivos
*Autores: Cervantes Garcia Eduardo, Chagoya Gonzalez Leonardo*


*Especificaciones*
Generar un microsistema de archivos el cual tenga la capacidad de realizar las siguientes operaciones
Listar los contenidos del directorio
Copiar uno de los archivos de dentro del FiUnamFS hacia tu sistema
Copiar un archivo de tu computadora hacia tu FiUnamFS
Eliminar un archivo del FiUnamFS

*Entorno y dependencias*
El código fue realizado en el lenguaje de programación de Python en su versión 3.9.13, en el editor de código Visual Studio Code . Se utilizaron las bibliotecas datatime,os, threading  . Es por ello que para ejecutar el código es recomendable tener Python 3.
En cuanto al Sistema Operativo, el código fue creado y ejecutado en Windows.


*Metodo de desarrollo*
Se divide el desarrollo del programa en 4 archivos de python: Main,fileEntry,operation y superblock. Apoyandonos de la programacion orientada a objetos. Definimos objetos para el superbloque y para el archivo fiunamfs.img


*superblock.py*
Esta clase representa al superbloque solicitado. Su metodo contructor necesita la ruta del archivo, en nuestro caso basta con colocar el nombre del archivo fiunamfs.img.
Se recupera la informacion del archivo mediante los metodos readCharacters y readlittlendianNumbers. Moviendo el puntero hacia los siguientes espacios

0–8 (se guarda en el campo name)
Para identificación, el nombre del sistema de archivos.

10–14 (se guarda en el campo version)
Versión de la implementación. Estamos implementando la versión 24.1.

20–39 
Etiqueta del volumen (se guarda en el campo volumeLabel)

40–44 (se guarda en el campo clusterSize)
Tamaño del cluster en bytes

45–49 (se guarda en dirSize)
Número de clusters que mide el directorio

50–54 ( se guarda en cuSize)
Número de clusters que mide la unidad completa



*fileEntry.py*
Esto es un clase que representa un archivo del sistema. Tiene un metodo constructor el cual abarca los siguiente puntos
1)Nombre del archivo (fileName)
2)Tamaño del archivo ,esto en bytes (fileSize)
3)La fecha de creacion (crDate)
4)La fecha de modificacion (modDate)
5)Archivos existentes

Para la asignacion contigua nos apoyamos del metodo senitinitialCluster, el cual asigna un cluster deacuerdo al tamaño de este y al tamaño del archivo



*Main.py*
En este archivo se inicializa un objeto superblock llamado super_bloque. Asi como tambien se tiene la estructura de un menu