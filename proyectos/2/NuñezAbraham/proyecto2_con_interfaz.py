import tkinter as tk
import threading
import queue
import time
import random

# Simulación de una cocina de restaurante
class Restaurante:
    def __init__(self, num_chefs, num_meseros, gui_ref=None):
        self.num_chefs = num_chefs  # Guarda num_chefs como variable de instancia
        self.num_meseros = num_meseros 
        self.pedidos = queue.Queue()
        self.lock_equipamiento = threading.Lock()
        self.sem_meseros = threading.Semaphore(num_meseros)
        self.cond_plato_listo = threading.Condition()
        self.cond_mesero = threading.Condition()  # Nueva variable de condición para coordinar con los meseros
        self.todos_pedidos_servidos = False
        self.gui_ref = gui_ref  # Referencia a la GUI para actualizaciones

    def chef(self, id_chef):
        while True:
            pedido = self.pedidos.get()
            if pedido is None:  # Si se recibe None, es la señal para detenerse
                self.pedidos.task_done()
                break
            with self.lock_equipamiento:
                self.actualizar_gui(f"Chef {id_chef} está preparando el pedido {pedido}")
                time.sleep(random.uniform(0.5, 2))
            with self.cond_plato_listo:
                self.actualizar_gui(f"Chef {id_chef} ha terminado el pedido {pedido}")
                self.cond_plato_listo.notify_all()
            self.pedidos.task_done()

    def mesero(self, id_mesero):
        while True:
            with self.cond_plato_listo:
                self.cond_plato_listo.wait()
                if self.todos_pedidos_servidos:  # Verificar si ya se sirvieron todos los pedidos
                    break
                with self.sem_meseros:
                    self.actualizar_gui(f"Mesero {id_mesero} está sirviendo un plato.")
                    time.sleep(random.uniform(0.5, 1))
                with self.cond_mesero:
                    self.cond_mesero.notify()  # Notificar al chef que el plato ha sido servido

    def actualizar_gui(self, mensaje):
        if self.gui_ref:  # Si se ha proporcionado una referencia a la GUI, usarla
            self.gui_ref.actualizar_log(mensaje)
        else:
            print(mensaje)  # De lo contrario, imprimir en consola

    def nuevo_pedido(self, id_pedido):
        self.actualizar_gui(f"Recibido nuevo pedido: {id_pedido}")
        self.pedidos.put(id_pedido)

    
    def finalizar_servicio(self):
        # Asegurarse de que todos los pedidos han sido procesados
        while not self.pedidos.empty():
            time.sleep(1)
        # Colocar None en la cola para cada chef como señal de parada
        for i in range(self.num_chefs):
            self.pedidos.put(None)
        with self.cond_plato_listo:
            self.todos_pedidos_servidos = True
            self.cond_plato_listo.notify_all()
        self.actualizar_gui("Todos los pedidos han sido preparados y servidos.")

    def programar_pedidos(self, total_pedidos, pedido_actual):
        if pedido_actual < total_pedidos:
            self.nuevo_pedido(pedido_actual)
            # Programa el próximo pedido para después de un tiempo aleatorio
            delay = int(random.uniform(100, 300))  # milisegundos
            self.gui_ref.master.after(delay, lambda: self.programar_pedidos(total_pedidos, pedido_actual + 1))
        else:
            # Una vez programados todos los pedidos, esperar un poco antes de detener los chefs
            self.gui_ref.master.after(1000, self.finalizar_servicio)

    def iniciar_servicio(self, num_pedidos):
        # Iniciar hilos de chefs
        for i in range(self.num_chefs):
            threading.Thread(target=self.chef, args=(i,)).start()

        # Iniciar hilos de meseros
        for i in range(self.num_meseros):
            threading.Thread(target=self.mesero, args=(i,)).start()

        # Programar la llegada de pedidos
        self.programar_pedidos(num_pedidos, 0)

        # Colocar None en la cola para cada chef como señal de parada
        for i in range(self.num_chefs):
            self.pedidos.put(None)

        # Esperar a que todos los pedidos sean procesados
        self.pedidos.join()
        with self.cond_plato_listo:
            self.todos_pedidos_servidos = True
            self.cond_plato_listo.notify_all()
        self.actualizar_gui("Todos los pedidos han sido preparados y servidos.")
    

class RestauranteGUI:
    def __init__(self, master, restaurante):
        self.master = master
        self.restaurante = restaurante
        master.title("Simulación de Restaurante")

        # Área de log
        self.log = tk.Text(master, state='disabled', height=10)
        self.log.pack(padx=10, pady=10)

        # Botón de inicio
        self.start_button = tk.Button(master, text="Iniciar Servicio", command=self.iniciar_servicio)
        self.start_button.pack(pady=5)

        # Estado de chefs y meseros
        self.estado_chefs = tk.Label(master, text="Chefs: Esperando")
        self.estado_chefs.pack(pady=5)

        self.estado_meseros = tk.Label(master, text="Meseros: Esperando")
        self.estado_meseros.pack(pady=5)

    def actualizar_log(self, mensaje):
        # Esta función se asegura de que la actualización de la GUI se ejecute en el hilo principal.
        def log_update():
            self.log.config(state='normal')
            self.log.insert('end', mensaje + "\n")
            self.log.config(state='disabled')
            self.log.see('end')
        self.master.after(0, log_update) 
    
    def iniciar_servicio(self):
        self.start_button.config(state='disabled')
        self.actualizar_log("Iniciando servicio...")
        # Iniciar la simulación en un hilo separado para no bloquear la GUI
        threading.Thread(target=self.simulacion).start()

    def simulacion(self):
        # Esta función se ejecuta en un hilo separado para manejar la simulación.
        # Llama a la función de inicio de servicio del restaurante.
        self.restaurante.iniciar_servicio(10)

# Crear la instancia de Restaurante
restaurante = Restaurante(3, 2, None)

# Crear la instancia de Tkinter
root = tk.Tk()
app = RestauranteGUI(root, restaurante)  # Pasar la instancia de Restaurante a RestauranteGUI
restaurante.gui_ref = app  # Establecer la referencia de la GUI en la instancia de Restaurante

root.mainloop()
