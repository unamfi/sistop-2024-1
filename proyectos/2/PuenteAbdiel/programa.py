import threading
import time
import tkinter as tk

class FabricaAutomoviles:
    def __init__(self):
        self.motor_listo = threading.Event()
        self.carroceria_listo = threading.Event()
        self.neumaticos_listo = threading.Event()
        self.mutex = threading.Lock()  # Mutex para proteger el ensamblaje del automóvil

    def ensamblar_motor(self):
        self.mostrar_espera(motor_label)
        time.sleep(5)  # Simulamos un tiempo de ensamblaje
        motor_label.config(text="Motor ensamblado.")
        self.motor_listo.set()

    def ensamblar_carroceria(self):
        self.mostrar_espera(carroceria_label)
        time.sleep(4)  # Simulamos un tiempo de ensamblaje
        carroceria_label.config(text="Carrocería ensamblada.")
        self.carroceria_listo.set()

    def ensamblar_neumaticos(self):
        self.mostrar_espera(neumaticos_label)
        time.sleep(3)  # Simulamos un tiempo de ensamblaje
        neumaticos_label.config(text="Neumáticos ensamblados.")
        self.neumaticos_listo.set()

    def mostrar_espera(self, label):
        label.config(text="Esperando inicio del ensamblaje...")
        label.update()  # Actualiza la interfaz gráfica

    def ensamblar_automovil(self):
        with self.mutex:
            self.motor_listo.wait()
            self.carroceria_listo.wait()
            self.neumaticos_listo.wait()
            return "Automóvil ensamblado con éxito!"
    
    def mostrar_hilos_activos(self):
        for thread in threading.enumerate():
            print(f"Hilo activo: {thread.name}")

def mostrar_hilos_activos():
    fabrica.mostrar_hilos_activos()

# Función para imprimir información sobre los hilos
def mostrar_hilos_activos():
    for thread in threading.enumerate():
        print(f"Hilo activo: {thread.name}")
    

# Función para iniciar el proceso de ensamblaje
def ensamblar_automovil():
    resultado = fabrica.ensamblar_automovil()
    resultado_label.config(text=resultado)

# Función para reiniciar el programa
def reiniciar_programa():
    motor_label.config(text="")
    carroceria_label.config(text="")
    neumaticos_label.config(text="")
    resultado_label.config(text="")
    fabrica.__init__()

# Función para salir del programa
def salir_del_programa():
    root.destroy()

# Crear una instancia de la fábrica
fabrica = FabricaAutomoviles()

# Configurar la ventana de Tkinter
root = tk.Tk()
root.title("Fábrica de Automóviles")

# Crear etiquetas para mostrar el progreso de ensamblaje
motor_label = tk.Label(root, text="", font=("Helvetica", 12))
motor_label.pack()

carroceria_label = tk.Label(root, text="", font=("Helvetica", 12))
carroceria_label.pack()

neumaticos_label = tk.Label(root, text="", font=("Helvetica", 12))
neumaticos_label.pack()

# Crear botones para iniciar el ensamblaje
motor_button = tk.Button(root, text="Ensamblar Motor", command=fabrica.ensamblar_motor)
motor_button.pack()

carroceria_button = tk.Button(root, text="Ensamblar Carrocería", command=fabrica.ensamblar_carroceria)
carroceria_button.pack()

neumaticos_button = tk.Button(root, text="Ensamblar Neumáticos", command=fabrica.ensamblar_neumaticos)
neumaticos_button.pack()

ensamblar_button = tk.Button(root, text="Ensamblar Automóvil", command=ensamblar_automovil)
ensamblar_button.pack()

# Crear botones para reiniciar y salir
reiniciar_button = tk.Button(root, text="Reiniciar Programa", command=reiniciar_programa)
reiniciar_button.pack()

salir_button = tk.Button(root, text="Salir del Programa", command=salir_del_programa)
salir_button.pack()

resultado_label = tk.Label(root, text="", font=("Helvetica", 14))
resultado_label.pack()

# Botón para mostrar hilos activos
mostrar_hilos_button = tk.Button(root, text="Mostrar Hilos Activos", command=mostrar_hilos_activos)
mostrar_hilos_button.pack()

root.mainloop()
