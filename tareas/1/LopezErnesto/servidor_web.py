import threading
import time
import random

"""
    Problema del servidor WEB: Al inicializar el servidor WEB, el jefe manda k hilos trabajadores 
    (los trabajadores que no tienen nada que hacer se van a dormir).

    El proceso jefe recibe una conexión de red, y elige a cualquiera de los trabajadores para que lo atienda
    (se le asigna a un trabajador y lo despierta).

    El jefe siempre busca tener k hilos disponibles para atender las solicitudes.

    ¿Cómo implementarías lo necesario para mantener la información de contabilidad?

        - Cada hilo debe de notificar antes de terminar su ejecución (puede ser cualquier tipo de información)
"""

# Variables necesarias

k_trabajadores = 5
mutex_trabajador = threading.Semaphore(0)
mutex_conexion = threading.Semaphore(1)
serial_id_trabajador = 0
conexiones = [] # Aquí se tendrá un arreglo compartido de conexiones para que los hilos puedan responder la cnexión correspondiente
# Tenemos a dos elementos esenciales: jefe y trabajadores

def iniciarServidor():
    global serial_id_trabajador, contador_trabajador
    serial_id_trabajador += 5
    for i in range(k_trabajadores):
        threading.Thread(target=trabajador,args=[i]).start()

def jefe(conexion): # Preguntar si el jefe será un hilo o podemos manejarlo únicamente de esta manera
    """
        El jefe debe de recibir conexiones de red y mandar a cada trabajador a resolver la petición:
            - Siempre tiene que volver a sacar otro hilo que esté disponible para responder a las conexiones
            - Tiene que asignar la petición a cualquiera de los trabajadores
    """
    global serial_id_trabajador
    conexiones.append(conexion)
    # Llega una conexión -> El jefe debe de mandar dicha tarea a uno de los hilos disponibles y agregar un nuevo hilo en espera
    mutex_trabajador.release()
    threading.Thread(target=trabajador,args=[serial_id_trabajador]).start()
    serial_id_trabajador += 1

def trabajador(x):
    """
        Los trabajadores se encargarán de responder las peticiones que son lanzadas por el jefe:
            - Estos siguen una carrera hasta el final, es decir, no vuelven con el jefe
            - Tiene que mandar información (notificar al jefe)
    """
    # En este punto, los hilos trabajadores están en espera de las distribuciones del jefe
    global conexiones
    mutex_trabajador.acquire()
    mutex_conexion.acquire()
    print(f"Trabajador {x} va a responder la petición {conexiones[0]}")
    conexiones.pop(0)
    # Cuando el jefe libera al trabajador, este procede a realizar la petición de conexión. Para el problema
    # consideraremos el tiempo de respuesta como la información de contabilidad. Para esto, se simulará un tiempo
    # aleatorio:
    tiempo_respuesta = random.random() + 0.5
    mutex_conexion.release()
    # El tiempo de respuesta lo mandamos a un sleep
    time.sleep(tiempo_respuesta)
    print(f"Trabajador {x} terminó de responder la petición en: {tiempo_respuesta} segundos")

iniciarServidor()
for i in range(50):
    time.sleep(1.5 * random.random())
    jefe(f"Conexión {i}")