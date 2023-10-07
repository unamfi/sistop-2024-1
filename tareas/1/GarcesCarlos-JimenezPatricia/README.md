# Tarea 1. Ejercicio de Sincronizaciòn

## Problema a resolver
### El servidor Web

Planteamiento

Al presentar los modelos de programación con hilos se presntó al Jefe-trabajador.
Así operan muchos servidores de red, como el servidor Apache.

Reglas:
- Al inicializar, el proceso jefe lanza k hilos trabajadores
   - Los trabajadores que no tienen nada que hacer se van a dormir
- El proceso jefe recibe una conexión de red, y elige a cualquiera de los trabajadores para que la atienda
   - Se la asigna a un trabajador y lo despierta
- El jefe va a buscar mantener siempre a k hilos disponibles y listos para atender las solicitudes que van llegando


## Lenguaje y entrono de desarrollo

	Python 3.0.12
	GCC 11.4.0

## Estrategia de sincronizaciòn

Se utilizaron Objetos de Semàforos
y Patrón de sincronizacion: Multiplex