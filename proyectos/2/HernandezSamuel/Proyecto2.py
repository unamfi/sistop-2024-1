import threading
import time
import tkinter as tk
import queue
import tkinter.font as tkFont

# Variables globales
message_queue = queue.Queue()
comensales_llegados = 0
max_comensales = 30
meseros = []
mesas = threading.Semaphore(5)
cocineros = threading.Semaphore(5)

# Clase para la interfaz gráfica
class RestaurantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Restaurante")
        self.root.geometry("600x600")  # Establece un tamaño inicial (puede ajustarse)
        self.center_window()  # Centra la ventana en la pantalla
        self.status_label = tk.Label(root, text="Estado del restaurante:", font=tkFont.Font(size=12))
        self.status_label.pack()
        self.status_text = tk.Text(root, font=tkFont.Font(size=12))  # Ajusta el tamaño de fuente
        self.status_text.pack(fill=tk.BOTH, expand=True)  # Hace que el cuadro de texto ocupe todo el espacio
        
    def center_window(self):
        # Obtiene el tamaño de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calcula las coordenadas para centrar la ventana
        x = (screen_width - self.root.winfo_reqwidth()) // 2
        y = (screen_height - self.root.winfo_reqheight()) // 2
        
        # Establece las coordenadas para centrar la ventana
        self.root.geometry("+{}+{}".format(x, y))

def log_status(message):
    app.status_text.insert(tk.END, message + "\n" + "\n")
    app.status_text.see(tk.END)

def process_messages():
    while True:
        try:
            message = message_queue.get(block=False)
            log_status(message)
        except queue.Empty:
            break
    if comensales_llegados >= max_comensales:
        log_status("¡Se atendieron a todos es hora de cerrar! :)")
    else:
        root.after(100, process_messages)

# Definición de funciones para actores
def comensal(nombre):
    global comensales_llegados
    mesa = mesas.acquire()
    message_queue.put(f'Comensal {nombre} ha llegado al restaurante y se ha sentado en la mesa {mesa + 1}.')
    mesero = meseros[mesa]
    message_queue.put(f'Comensal {nombre} ha hecho su pedido a Mesero {mesero.nombre}.')
    mesero.tomar_pedido(nombre, mesa)
    cocinero = cocineros.acquire()
    message_queue.put(f'El Cocinero está preparando el pedido de Comensal {nombre}.')
    time.sleep(3)  # Tiempo para cocinar el plato
    message_queue.put(f'El Cocinero ha terminado el pedido de Comensal {nombre}.')
    cocineros.release(cocinero)
    mesero.entregar_pedido(nombre, mesa)
    time.sleep(2)  # Tiempo para comer
    message_queue.put(f'Comensal {nombre} ha terminado de comer en la mesa {mesa + 1} y paga.')
    mesas.release(mesa)
    comensales_llegados += 1

class Mesero:
    def __init__(self, nombre):
        self.nombre = nombre
    def tomar_pedido(self, comensal, mesa):
        message_queue.put(f'Mesero {self.nombre} ha tomado el pedido de Comensal {comensal} en la mesa {mesa + 1}.')
    def entregar_pedido(self, comensal, mesa):
        message_queue.put(f'Mesero {self.nombre} ha entregado el pedido de Comensal {comensal} en la mesa {mesa + 1}.')

def personal_limpieza(nombre):
    mesa = mesas.acquire()
    message_queue.put(f'Personal de limpieza {nombre} está limpiando la mesa {mesa + 1}.')
    time.sleep(4)  # Tiempo para limpiar la mesa
    message_queue.put(f'Personal de limpieza {nombre} ha terminado de limpiar la mesa {mesa + 1}.')
    mesas.release(mesa)

# Creación de hilos para los actores
meseros = [Mesero(i) for i in range(5)]
comensales = [threading.Thread(target=comensal, args=(i,)) for i in range(max_comensales)]
personal_limpieza_threads = [threading.Thread(target=personal_limpieza, args=(i,)) for i in range(5)]

# Inicio de los hilos
for comensal in comensales:
    comensal.start()
for personal_limpieza_thread in personal_limpieza_threads:
    personal_limpieza_thread.start()

root = tk.Tk()
app = RestaurantApp(root)
root.after(100, process_messages)
root.mainloop()

# Esperar a que todos los hilos terminen
for comensal in comensales:
    comensal.join()
for personal_limpieza_thread in personal_limpieza_threads:
    personal_limpieza_thread.join()

print('La simulación ha terminado.')
