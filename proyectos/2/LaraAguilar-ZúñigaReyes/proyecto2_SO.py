#Proyecto 2
# Lara Aguilar Christian Abraham
# Zúñiga Reyes Lissett

# Importamos las bibliotecas necesarias para la ejecución correcta
import tkinter as tk # Biblioteca para la interfaz gráfica
import threading # Biblioteca para los hilos
import time # Biblioteca para el tiempo
import random # Biblioteca para generar números aleatorios

# Clase que representa el metro y sus acciones (abrir puertas, cerrar puertas, bajar pasajero, subir pasajero)
class Metro:
    def __init__(self, root):
        self.pasajeros_dentro = random.randint(0, 15) # Se genera un número aleatorio de pasajeros dentro del metro
        self.pasajeros_esperando = random.randint(0, 10) # Se genera un número aleatorio de pasajeros esperando
        self.puertas_abiertas = False # Se inicializa el estado de las puertas
        self.mutex = threading.Lock() # Se inicializa el mutex
        self.cond = threading.Condition(self.mutex) # Se inicializa la condición
        self.root = root
        self.label = tk.Label(root)
        self.label.pack()
        self.canvas = tk.Canvas(root, width=400, height=200) # Se inicializa el canvas
        self.canvas.pack()
        self.metro = self.canvas.create_rectangle(50, 50, 350, 150, fill="blue") # Se crea el rectángulo que representa el metro en el canvas y se le da color azul
        self.puertas = [self.canvas.create_rectangle(150, 50, 200, 150, fill="yellow"), # Se crean los rectángulos que representan las puertas en el canvas y se les da color amarillo
                        self.canvas.create_rectangle(200, 50, 250, 150, fill="yellow")]
        self.pasajeros = [self.canvas.create_oval(100+i*20, 30, 120+i*20, 50, fill="red") for i in range(10)] # Se crean los círculos que representan a los pasajeros en el canvas y se les da color rojo

    def abrir_puertas(self): # Método para abrir las puertas
        with self.mutex:
            if self.pasajeros_esperando > 0: # Si hay pasajeros esperando, se abren las puertas
                self.puertas_abiertas = True
                self.actualizar_interfaz("Metro: Puertas abiertas.", "yellow") # Se actualiza la interfaz
                self.cond.notify_all() # Se notifica a los hilos que están esperando
            else:
                self.actualizar_interfaz("No hay pasajeros esperando.", "yellow")
                self.cond.notify_all()

    def cerrar_puertas(self): # Método para cerrar las puertas
        with self.mutex:
            self.puertas_abiertas = False # Se cierran las puertas
            self.actualizar_interfaz("Metro: Puertas cerradas.", "blue") # Se actualiza la interfaz
            self.cond.notify_all() # Se notifica a los hilos que están esperando

    def bajar_pasajero(self): # Método para bajar pasajeros
        with self.mutex: # Se usa el mutex para evitar que se modifiquen los datos al mismo tiempo
            while not self.puertas_abiertas or self.pasajeros_dentro == 0: # Mientras las puertas estén cerradas o no haya pasajeros dentro, se espera
                self.cond.wait()    # Se espera a que se abran las puertas y haya pasajeros dentro
            if self.pasajeros_dentro > 0: # Si hay pasajeros dentro, se bajan
                self.actualizar_interfaz("Pasajero: Bajando del metro.", "red")
                time.sleep(random.randint(1, 3))
                self.pasajeros_dentro -= 1 # Se actualiza el número de pasajeros dentro
                self.pasajeros_esperando += random.randint(0, 3) # Se actualiza el número de pasajeros esperando
                self.cond.notify_all()

    def subir_pasajero(self): # Método para subir pasajeros
        with self.mutex:
            while not self.puertas_abiertas or self.pasajeros_dentro >= 10 or self.pasajeros_esperando == 0: # Mientras las puertas estén cerradas, haya 10 pasajeros dentro o no haya pasajeros esperando, se espera
                self.cond.wait()
            if self.pasajeros_dentro < 10: # Si hay menos de 10 pasajeros dentro, se suben
                self.actualizar_interfaz("Pasajero: Subiendo al metro.", "green")
                time.sleep(random.randint(1, 3)) # Se simula el tiempo que tarda en subir un pasajero
                self.pasajeros_dentro += 1  # Se simula el tiempo que tarda en bajar un pasajero
                self.pasajeros_esperando -= 1
                self.cond.notify_all()


    def actualizar_interfaz(self, mensaje, color_puertas): # Método para actualizar la interfaz
        for puerta in self.puertas: # Se actualiza el color de las puertas
            self.canvas.itemconfig(puerta, fill=color_puertas) # Se actualiza el color de las puertas
            # Se actualiza el texto de la interfaz
        self.label.config(text=f"{mensaje}\nPasajeros a bordo: {self.pasajeros_dentro}\nUsuarios esperando: {self.pasajeros_esperando}\nEstado de las puertas: {'Abierto' if self.puertas_abiertas else 'Cerrado'}")
        self.root.update()

root = tk.Tk() # Se crea la ventana
metro = Metro(root) # Se crea el metro
for _ in range(10): # Se crean los hilos
    threading.Thread(target=metro.bajar_pasajero).start() # Se crean los hilos para bajar pasajeros
for _ in range(10): # Se crean los hilos para subir pasajeros
    threading.Thread(target=metro.subir_pasajero).start() 
metro.abrir_puertas() # Se abren las puertas
root.mainloop() # Se ejecuta la ventana
