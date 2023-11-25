---
title: 'PROYECTO 03: (MICRO) SISTEMA DE ARCHIVOS'
created: '2023-11-16T05:43:06.092Z'
modified: '2023-11-25T08:41:06.801Z'
---

# PROYECTO 03: (MICRO) SISTEMA DE ARCHIVOS

### Descripción General:

¡Este es el Proyecto 3 del curso de Sistemas Operativos! Y por ende, el último.

Este proyecto es el resultado de un arduo trabajo y representa tanto la culminación de mejoras significativas como la implementación de diversas funcionalidades para un gestor de archivos interactivo con el sistema de archivos 'FIUNAMFS'.

### Características Destacadas:

- Listado de contenido del sistema de archivos.
- Copia de archivos desde 'FIUNAMFS' a la computadora y viceversa.
- Eliminación de archivos del sistema 'FIUNAMFS'.
- Verificación de información general del sistema de archivos.

### Miembros del Equipo:

- Hernández Ortiz Jonathan
- Pérez Avin Paola Celina de Jesús

### Novedades y Mejoras:

A lo largo de esta versión, se han realizado:

- Correcciones de errores.
- Optimización del código para mejor rendimiento.
- Implementación de nuevas funciones para una experiencia más completa.

¡Estamos sumamente emocionados por presentar la versión final de nuestro (micro) sistemas de archivos, la V5, llena de mejoras y funcionalidades! Nos llevó bastante investigación, prueba y error elaborar este proyecto así que. ¡Gracias por ser parte de esta experiencia! Heh.

## OBJETIVOS

Objetivos a considerar para el proyecto.

Desarrollar es un programa que pueda obtener, crear y modificar información en el micro-sistema-de-archivos de la Facultad de Ingeniería, FiUnamFS.

- Listar los contenidos del directorio dentro de FiUnamFS.
- Copiar un archivo desde FiUnamFS hacia el sistema local.
- Copiar un archivo desde el sistema local hacia FiUnamFS.
- Eliminar archivos específicos almacenados en FiUnamFS.

Implementar un programa para desfragmentar FiUnamFS, realizando la reorganización de datos dentro del sistema de archivos existente, con el fin de mitigar la fragmentación externa. Asegurarse de realizar la desfragmentación sin crear un nuevo sistema de archivos ni copiar hacia uno nuevo.

## ESTRATEGIA

### Comprensión de la especificación:
- Analizar detalladamente la especificación proporcionada para comprender los requisitos funcionales y no funcionales del sistema de archivos FiUnamFS.
- Identificar los casos de uso y las operaciones requeridas para el sistema de archivos.

### Planificación y diseño:
- Establecer un plan de trabajo detallado que incluya las etapas de desarrollo, pruebas y documentación.
- Diseñar una arquitectura de software que cumpla con los requisitos de FiUnamFS.
- Definir la estructura de datos y algoritmos necesarios para implementar las operaciones requeridas (listar, copiar, eliminar archivos, desfragmentación).

### Implementación:
- Desarrollar el código del sistema de archivos FiUnamFS siguiendo las especificaciones.
- Implementar las funciones para listar contenidos, copiar archivos dentro y fuera del sistema, eliminar archivos y realizar la desfragmentación interna del sistema.

### Pruebas:
- Realizar pruebas exhaustivas para cada función y operación implementada.
- Verificar la integridad y el correcto funcionamiento del sistema mediante pruebas de unidad, integración y sistema.

### Optimización y control de calidad:
- Optimizar el sistema para mejorar su rendimiento y eficiencia.
- Realizar revisiones de código y asegurarse de cumplir con los estándares de calidad.

## REQUISITOS DE USO

### Funcionalidades del programa:
- Listar archivos en FiUnamFS.
- Copiar archivos desde y hacia FiUnamFS.
- Eliminar archivos de FiUnamFS.

### Requisitos del entorno:
- Acceso al archivo de imagen "fiunamfs.img".
- Operaciones seguras y correctas en FiUnamFS.

### Recursos necesarios:
- Permisos de lectura/escritura en "fiunamfs.img".
- Precaución al manipular el sistema de archivos para evitar corrupción.

### Documentación:
- Guía de usuario para el programa.
- Explicación de funcionalidades, limitaciones y riesgos.

### Mejoras potenciales:
- Garantizar integridad en manipulación de archivos.
- Mejor manejo de errores.
- Comentarios en el código para facilitar comprensión.

## ENTORNO DE DESARROLLO

### Sistemas Operativos Compatibles:
- Linux.
- macOS.
- Windows (a través de Git Bash, WSL u otros emuladores de terminal Unix).

### Requisitos de Hardware:
- No se necesitan especificaciones especiales.
- Se recomienda al menos 2 GB de RAM para un rendimiento óptimo.

### Software Requerido:
- Python 3.x y sus librerías estándar son necesarios para la ejecución del programa.

## LENGUAJE DE PROGRAMACIÓN Y VERSIÓN

### Python:
- Lenguaje de programación utilizado: Python.
- Versión recomendada: Python 3.x (por ejemplo, 3.7, 3.8, 3.9, etc.).

### Descarga de Python:
- Se puede descargar Python desde [python.org](https://www.python.org/downloads/).

### Herramientas o frameworks asociados:
- No se utilizan frameworks específicos en el código, solo librerías estándar de Python como os, time, struct, entre otras.

## ¡DESCARGA EL ARCHIVO!

Descarga ahora mismo el archivo:

   ```
   microsistema_final.py
   ```

## EJECUCIÓN

1. **Descarga**: Puedes obtener el código de dos maneras copiando y pegando el código en un archivo de Python con extensión `.py`, o descargando el archivo `microsistema_final.py` que se adjunta.

2. **Ejecución en la terminal**: Para ejecutar el programa, abre una terminal o línea de comandos en tu computadora. Luego, navega al directorio donde se encuentra el archivo de código.

3. **Iniciar el programa**: Utiliza alguna de las siguientes opciones para iniciar la ejecución del programa.

Escribe simplemente el nombre del programa y teclea `enter`:

   ```
   microsistema_final.py
   ```

Escribe `py`, el nombre del programa y teclea `enter`:

 ```
py microsistema_final.py
 ```
Escribe `python`, el nombre del programa y teclea `enter`:

 ```
python microsistema_final.py
 ```
   ---
> Realizado por:
> - Hernández Ortiz Jonathan Emmanuel.
> - Pérez Avin Paola Celina de Jesús.
