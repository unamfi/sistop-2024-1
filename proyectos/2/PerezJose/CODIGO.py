import threading
import time
import random
import os
import queue

#---------------------------------------------------------------------------
#Varibles nombradas de acuerdo a su funcion
personas_en_espera = queue.Queue()
copias_vendidas_total = 0
print_lock = threading.Lock() 

#---------------------------------------------------------------------------

# Clase ReadWriteLock para manejar bloqueos de lectura y escritura.
# Permite que varios hilos lean un recurso compartido simultáneamente,
# pero asegura que un hilo que escriba tenga acceso exclusivo.
class ReadWriteLock:
    def __init__(self):
        self._readers = 0  # Contador de lectores activos
        self._readers_lock = threading.Lock()  # Lock para modificar el contador de lectores
        self._writers_lock = threading.Lock()  # Lock exclusivo para escritores
    
    # Adquiere el lock para lectura.
    # Si es el primer lector, adquiere el lock de escritores para bloquear escritores.
    def acquire_read(self):
        with self._readers_lock:
            self._readers += 1
            if self._readers == 1:
                self._writers_lock.acquire()
    
    # Libera el lock de lectura.
    # Si no hay más lectores, libera el lock de escritores para permitir la escritura.
    def release_read(self):
        with self._readers_lock:
            self._readers -= 1
            if self._readers == 0:
                self._writers_lock.release()
    
    # Adquiere el lock para escritura, bloqueando a otros escritores y lectores.
    def acquire_write(self):
        self._writers_lock.acquire()
    
    # Libera el lock de escritura, permitiendo a otros escritores o lectores proceder.
    def release_write(self):
        self._writers_lock.release()

# Instancia del Read-Write Lock
rw_lock = ReadWriteLock()

#---------------------------------------------------------------------------

# Función que muestra arte ASCII en la pantalla 
def mostrar_arte_ascii4():
    os.system('clear') #limpia la pantalla para solo mostrar el arte ascii
    arte_ascii = """
        
        _    ___    _    ___   ___ ___    _   __  __  ___  ___ 
       | |  / _ \  | |  / _ \ / __| _ \  /_\ |  \/  |/ _ \/ __|
       | |_| (_) | | |_| (_) | (_ |   / / _ \| |\/| | (_) \__ \
    \n        |____\___/  |____\___/ \___|_|_\/_/ \_\_|  |_|\___/|___/
                          
                                      ¶¶¶¶¶¶¶¶¶
                                    ¶¶          ¶¶
                      ¶¶¶¶¶       ¶¶              ¶¶
                     ¶     ¶    ¶¶     ¶¶    ¶¶     ¶¶
                     ¶     ¶   ¶¶      ¶¶    ¶¶       ¶¶
                     ¶    ¶  ¶¶        ¶¶    ¶¶        ¶¶
                      ¶   ¶   ¶                         ¶¶
                    ¶¶¶¶¶¶¶¶¶¶¶¶                        ¶¶
                   ¶´´´´´´´´´´´´¶ ¶¶             ¶¶     ¶¶
                  ¶¶            ¶  ¶¶            ¶¶     ¶¶
                 ¶¶   ¶¶¶¶¶¶¶¶¶¶¶    ¶¶        ¶¶       ¶¶
                 ¶               ¶     ¶¶¶¶¶¶¶         ¶¶
                 ¶¶              ¶                    ¶¶
                  ¶   ¶¶¶¶¶¶¶¶¶¶¶¶                   ¶¶
                  ¶¶           ¶  ¶¶                ¶¶
                   ¶¶¶¶¶¶¶¶¶¶¶¶     ¶¶            ¶¶
                                      ¶¶¶¶¶¶¶¶¶¶¶¶
                                                                             

    """
    print(arte_ascii)
    time.sleep(3)  # Mostrar durante 3 segundos
#---------------------------------------------------------------------------

def mostrar_arte_ascii5():
    os.system('clear') 
    arte_ascii = """
          _  _  ___    _    ___    _    ___   ___ ___    _   __  __  ___  ___ 
         | \| |/ _ \  | |  / _ \  | |  / _ \ / __| _ \  /_\ |  \/  |/ _ \/ __|
         | .` | (_) | | |_| (_) | | |_| (_) | (_ |   / / _ \| |\/| | (_) \__ \
    \n         |_|\_|\___/  |____\___/  |____\___/ \___|_|_\/_/ \_\_|  |_|\___/|___/
    
                              ███████▄▄███████████
                            ▓▓▓▓▓▓█░░░░░░░░░░░░░░█
                            ▓▓▓▓▓▓█░░░░░░░░░░░░░░█
                            ▓▓▓▓▓▓█░░░░░░░░░░░░░░█
                            ▓▓▓▓▓▓█░░░░░░░░░░░░░░█
                            ▓▓▓▓▓▓█░░░░░░░░░░░░░░█
                            ▓▓▓▓▓▓███░░░░░░░░░░░░█
                            ██████▀  █░░░░██████▀
                                     █░░░░█
                                      █░░░█
                                       █░░█
                                       █░░█
                                        ▀▀

    """
    print(arte_ascii)
    time.sleep(3)  
#---------------------------------------------------------------------------

def mostrar_arte_ascii():
    os.system('clear')
    arte_ascii = """
        ════════════════════════════════════════════════════════════════════════
    
                ████████ ███████ ████████ ██████  ██ ███████     ██████  
                   ██    ██         ██    ██   ██ ██ ██               ██ 
                   ██    █████      ██    ██████  ██ ███████      █████  
                   ██    ██         ██    ██   ██ ██      ██     ██      
                   ██    ███████    ██    ██   ██ ██ ███████     ███████ 
                                                                         
                        
        ════════════════════════════════════════════════════════════════════════
    """
    print(arte_ascii)
    time.sleep(3) 

#---------------------------------------------------------------------------

def mostrar_arte_ascii2():
    os.system('clear')  
    arte_ascii = """
         _____ ___  _____ _   _ _____ _      _       ___   _____  
        |_   _/ _ \|  _  | | | |_   _| |    | |     / _ \ /  ___| 
          | |/ /_\ \ | | | | | | | | | |    | |    / /_\ \\ `--.  
          | ||  _  | | | | | | | | | | |    | |    |  _  | `--. \ 
          | || | | \ \/' / |_| |_| |_| |____| |____| | | |/\__/ / 
          \_/\_|_|_/\_/\_\\___/_\___/\_____/\_____/\_|_|_/\____/  
         / _ \ | ___ \_   _|  ___| ___ \_   _/ _ \ /  ___|        
        / /_\ \| |_/ / | | | |__ | |_/ / | |/ /_\ \\ `--.         
        |  _  || ___ \ | | |  __||    /  | ||  _  | `--. \        
        | | | || |_/ /_| |_| |___| |\ \  | || | | |/\__/ /        
        \_| |_/\____/ \___/\____/\_| \_| \_/\_| |_/\____/         

    """
    print(arte_ascii)
    time.sleep(2)  
    
#---------------------------------------------------------------------------

def mostrar_arte_ascii3():
    os.system('clear') 
    arte_ascii = """
      
          _______       ____  _    _ _____ _      _                _____  
         |__   __|/\   / __ \| |  | |_   _| |    | |        /\    / ____| 
            | |  /  \ | |  | | |  | | | | | |    | |       /  \  | (___   
            | | / /\ \| |  | | |  | | | | | |    | |      / /\ \  \___ \  
            | |/ ____ \ |__| | |__| |_| |_| |____| |____ / ____ \ ____) | 
           _|_/_/____\_\___\_\\____/|_____|______|______/_/    \_\_____/  
          / ____|  ____|  __ \|  __ \     /\   |  __ \   /\    / ____|    
         | |    | |__  | |__) | |__) |   /  \  | |  | | /  \  | (___      
         | |    |  __| |  _  /|  _  /   / /\ \ | |  | |/ /\ \  \___ \     
         | |____| |____| | \ \| | \ \  / ____ \| |__| / ____ \ ____) |    
          \_____|______|_|  \_\_|  \_\/_/    \_\_____/_/    \_\_____/     

    """
    print(arte_ascii)
    time.sleep(2)  
    
#---------------------------------------------------------------------------
# Función que simula la apertura de las taquillas
def abrir_taquillas():
    personas_atendidas = 0
    while not personas_en_espera.empty() and personas_atendidas < 5:
        taquilla_id = personas_en_espera.get()  # Obtenemos una persona de la cola (bloqueante)
        synchronized_print(f"║ Taquilla {taquilla_id + 1} está procesando una compra.")
        
        personas_en_espera.task_done()  # Indicamos que la taquilla ha terminado de procesar la compra
        with rw_lock._writers_lock:
            global copias_vendidas_total
            copias_vendidas_total += 1  # Actualizamos el total de copias vendidas
        personas_atendidas += 1
#---------------------------------------------------------------------------
# Función que simula la venta de copias en una taquilla
def vender_copias(taquilla_id):
    personas_en_espera.put(taquilla_id)  # Añadimos una persona a la cola
    print(f"║ Una persona se forma en la taquilla {taquilla_id + 1}.")

# Función para la llegada de personas
def llegada_personas():
    n = random.randint(1, 10)
    print(f"║  {n} personas llegan para comprar una copia del juego     ")
    for i in range(n):
        threading.Thread(vender_copias(i % 3)).start()
        
# Función que maneja la impresión sincronizada
def synchronized_print(*args, **kwargs):
    with print_lock:
        print(*args, **kwargs)
#---------------------------------------------------------------------------
mostrar_arte_ascii()
print("""
        ╔═══════════════════════════════════════════════════════════════════════╗ 
        ║     Ayuda a los desarrolladores a mantener las ventanillas abiertas   ║ 
        ║     para poder vender el stock de alrededor de 150 copias.            ║ 
        ║      El gran juego TETRIS 2 busca la venta de al menos 50 copias      ║ 
        ║     para poder recuperar la inversion del juego.                      ║ 
        ╚═══════════════════════════════════════════════════════════════════════╝ 
""")
time.sleep(8)
mostrar_arte_ascii2()

#---------------------------------------------------------------------------
def mostrar_estado():
    with print_lock:
        os.system('clear')  # Limpiar la pantalla
        print("""
        ╔═══════════════════════════════╗
        ║        VENTA DE COPIAS        ║
        ╚═══════════════════════════════╝
        """)
        print("╔══════════════════════════════════════════════════════════════════════════╗")
        print(f"║ Personas en espera: {personas_en_espera.qsize()}")
        print("╚══════════════════════════════════════════════════════════════════════════╝")
#---------------------------------------------------------------------------
def procesar_compras():
    while not personas_en_espera.empty():
        taquilla_id = personas_en_espera.get()
        with print_lock:
            print(f"║ Taquilla {taquilla_id + 1} está procesando una compra.")
        
        personas_en_espera.task_done()
#---------------------------------------------------------------------------
# Lógica para ejecutar el programa y manejar la entrada del usuario

#si se venden las 150 copias se termina de vender hasta ese ciclo y se termina el programa
while True:
    if copias_vendidas_total >= 150:
        os.system('clear')
        print("\n\n ╔══════════════════════════════╗    ")
        print(f" ║ Total de copias vendidas: {copias_vendidas_total} ")
        print(" ╚══════════════════════════════╝     ")
        print("""
        ╔═══════════════════════════════╗
        ║        VENTA EXITOSA!!!       ║
        ╚═══════════════════════════════╝
        """)
        time.sleep(5)
        mostrar_arte_ascii4()
        time.sleep(3)
        mostrar_arte_ascii3()
        time.sleep(3)
        exit()
        
#MENU de usuario
    mostrar_estado()  # Mostrar el estado actual
    # Simula la llegada de personas
    llegada_personas()

    # Iniciamos las taquillas en hilos separados si hay personas en espera
    if not personas_en_espera.empty():
        threading.Thread(abrir_taquillas()).start()

    # Muestra el estado actual después de la llegada de personas y la apertura de las taquillas
    
    with print_lock:
        print(f"║ Personas en espera después de 10 min  en taquillas: {personas_en_espera.qsize()} ")
        print("╚══════════════════════════════════════════════════════════════════════════╝")
        user_input = input("Presiona Enter para continuar vendiendo o escribe 'cerrar' para cerrar las taquillas: ")
    
    if user_input.lower() == 'cerrar':
        print(" ╔══════════════════════════════╗    ")
        print(f"║ Total de copias vendidas: {copias_vendidas_total} ")
        print(" ╚══════════════════════════════╝     ")
        time.sleep(2)
        if copias_vendidas_total >= 50:
            mostrar_arte_ascii4()
            time.sleep(2)
        else:
            mostrar_arte_ascii5()
            time.sleep(2)
        mostrar_arte_ascii3()
        break
