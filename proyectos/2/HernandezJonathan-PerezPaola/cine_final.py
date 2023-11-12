################# PROYECTO 2 ############################
############# Sistemas Operativos ####################### 
############### Semestre 2024-1 #########################
################# Integrantes ###########################
######## Hernandez Ortiz Jonathan Emmanuel ##############
######## Pérez Avin Paola Celina de Jesús ###############


######### Código: Este programa en Python fue creado para implementar 
######### una solución de sincronización en una sala de cine. La sala 
######### tiene una capacidad de 10 personas, pero tenemos 100 clientes
######### que desean ingresar para ver una película específica. Para evitar
######### que más de 10 personas entren en la sala al mismo tiempo, utilizamos
######### hilos para controlar la entrada y salida de las personas, permitiendo
######### así que todos disfruten de la película sin problemas.

# Se importan las bibliotecas a ocupar en el programa.
import threading 
import os,time,random

# Se utiliza una biblioteca para agregar colores a los textos en la consola del terminal.
from colorama import Fore 

# Colores disponibles para asignar a cada cliente y aplicar en la terminal.
# Rojo      Blanco     Amarillo    Verde      Azul        Magenta     Cyan.
color =[Fore.RED,Fore.WHITE,Fore.YELLOW,Fore.GREEN,Fore.BLUE,Fore.MAGENTA,Fore.CYAN]
# Se crea un semáforo para controlar el acceso a los asientos de la sala del cine.
# Suponiendo, como ejemplo, que hay 10 asientos disponibles.
semaforo_cine = threading.Semaphore(10) 

# Función que simula el proceso de un espectador viendo una película.
def ver_pelicula(espectador_id):
    
    # Se aplica un pequeño retraso para evitar que la información se imprima de
    # forma inmediata, lo que dificultaría la apreciación de la asignación de asientos.
    time.sleep(5)
    
    # ¡Generamos un color de forma aleatoria para cada cliente!
    mi_color = color[random.randint(0, 6)]
    # Imprimimos su color asignado y todos comienzan en la fila para disfrutar.
    print(mi_color +  "\nEspectador %d está en la fila del cine." % espectador_id)
    # Aplicamos un retraso para una asignación más clara de asientos.
    time.sleep(5)
    
    # Intenta adquirir un asiento si hay disponibilidad.
    semaforo_cine.acquire()  
    print(mi_color + "\nEspectador %d ha ocupado un asiento y está viendo la película." %espectador_id)
    print("¡A disfrutar!")
    
    # Verifica si el espectador realizará un comportamiento específico.
    probabilidad_comportamiento = random.random()
    if probabilidad_comportamiento <= 0.1:  # Por ejemplo, 10% de probabilidad de comprar palomitas.
        print(mi_color + "\nEspectador %d fue a comprar palomitas." % espectador_id)
        time.sleep(5)
    elif probabilidad_comportamiento <= 0.2:  # Por ejemplo, 20% de probabilidad de ir al baño.
        print(mi_color + "\nEspectador %d fue al baño." % espectador_id)
        time.sleep(2)
    
     # Probabilidad de deserción durante la película.
    probabilidad_desercion = random.random()
    if probabilidad_desercion <= 0.05:  # Por ejemplo, 5% de probabilidad de deserción.
        print(Fore.YELLOW + "\nEspectador %d ha abandonado el cine durante la película." % espectador_id)

    # Simula el tiempo de duración de la película.
    time.sleep(7)
    
    # Libera el asiento para el siguiente cliente del hilo.
    semaforo_cine.release()  
    print(mi_color + "\nEspectador %d ha terminado de ver la película y ha dejado un asiento." % espectador_id)
    print("Muy bonita la pelicula... :)")
        
# Cantidad de personas que desean disfrutar de la película.
num_espectadores = 100

# Generamos hilos para los espectadores.
hilos = []
print()

# ¡Se imprime el mensaje de bienvenida!
print("Proyecto 2 Sistemas Operativos")
print("-------Bienvenidos al Cine UNAM-----------")

# Aplicamos un retraso de 3 segundos en los hilos.
threading.Event().wait(3)
os.system('cls')

# Variable asignada con un rango para mejorar la visualización del bucle FOR.
rango = range(1, num_espectadores + 1)

# Creamos un bucle FOR para enviar a los espectadores y visualizar los hilos.
for espectador_id in rango:
    # Aplicamos un retraso para dar tiempo a que los espectadores pasen.
    time.sleep(3)
    # Hilo para los espectadores que se les pasa como argumentos a la función 'ver_pelicula'.
    # La variable espectador_id.
    hilo = threading.Thread(target=ver_pelicula, args=(espectador_id,))
    # Se añade una lista los hilos.
    hilos.append(hilo)
    # Se inicializan los hilos.
    hilo.start()

# Limpiamos la pantalla para comenzar la simulación de entrada y salida de la sala de cine.
os.system('cls')

# Al igual que abrimos los hilos, debemos cerrarlos para optimizar los procesos.
# Y asimismo, no consumir recursos que ya no se ocupan.
for hilo in hilos:
    hilo.join()
    
# Aquí terminan los hilos, indicando que todos han disfrutado de la película. :D
print()
print(Fore.WHITE + "Simulación de espectadores viendo una película en el cine terminada.")
print()
print()
# Detenemos 5 segundos antes de finalizar el programa.
time.sleep(5)
# ¡Fin del programa! Gracias por ver. 