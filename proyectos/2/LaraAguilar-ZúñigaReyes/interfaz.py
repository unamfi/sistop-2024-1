import tkinter as tk
from proyecto2 import Metro
import random
from threading import Thread
import time

class InterfazMetro:
    def __init__(self, root, metro):
        self.metro = metro
        self.root = root
        self.label = tk.Label(root)
        self.label.pack()
        self.canvas = tk.Canvas(root, width=400, height=200)
        self.canvas.pack()
        self.metro_rect = self.canvas.create_rectangle(50, 50, 350, 150, fill="blue")
        self.puertas = [self.canvas.create_rectangle(150, 50, 200, 150, fill="yellow"),
                        self.canvas.create_rectangle(200, 50, 250, 150, fill="yellow")]
        self.pasajeros = [self.canvas.create_oval(100+i*20, 30, 120+i*20, 50, fill="red") for i in range(10)]
        self.pasajeros_label = tk.Label(root, text="Pasajeros a bordo: 0")
        self.pasajeros_label.pack()
        self.esperando_label = tk.Label(root, text="Pasajeros esperando: 0")
        self.esperando_label.pack()
        self.tiempo_puertas_label = tk.Label(root, text="Tiempo de puertas: Cerradas")
        self.tiempo_puertas_label.pack()
        self.actualizar_interfaz()

    def actualizar_interfaz(self):
        self.label.config(text="Estado actual del metro")
        for puerta in self.puertas:
            self.canvas.itemconfig(puerta, fill="yellow" if self.metro.get_estado_puertas() else "grey")
        for i in range(10):
            if i < self.metro.get_pasajeros_dentro():
                self.canvas.coords(self.pasajeros[i], 100+i*20, 70, 120+i*20, 90)
            else:
                self.canvas.coords(self.pasajeros[i], 100+i*20, 30, 120+i*20, 50)
        self.pasajeros_label.config(text="Pasajeros a bordo: " + str(self.metro.get_pasajeros_dentro()))
        self.esperando_label.config(text="Pasajeros esperando: " + str(self.metro.get_pasajeros_esperando()))
        self.tiempo_puertas_label.config(text="Tiempo de puertas: Abiertas" if self.metro.get_estado_puertas() else "Tiempo de puertas: Cerradas")
        self.root.after(1000, self.actualizar_interfaz)

def pasajero(metro):
    while True:
        time.sleep(random.randint(1, 5))
        metro.bajar_pasajero()
        time.sleep(random.randint(1, 5))
        metro.terminar_bajar()
        time.sleep(random.randint(1, 5))
        metro.subir_pasajero()
        time.sleep(random.randint(1, 5))
        metro.terminar_subir()

def metro(metro):
    while True:
        time.sleep(random.randint(1, 5))
        metro.abrir_puertas()
        time.sleep(random.randint(1, 5))
        metro.cerrar_puertas()

def agregar_pasajero_esperando(metro):
    while True:
        time.sleep(random.randint(1, 5))
        metro.agregar_pasajero_esperando()

def quitar_pasajero_esperando(metro):
    while True:
        time.sleep(random.randint(1, 5))
        if metro.get_pasajeros_esperando() > 0:
            metro.quitar_pasajero_esperando()

if __name__ == "__main__":
    root = tk.Tk()
    metro_obj = Metro()
    interfaz = InterfazMetro(root, metro_obj)
    for i in range(10):
        Thread(target=pasajero, args=(metro_obj,)).start()
    Thread(target=metro, args=(metro_obj,)).start()
    Thread(target=agregar_pasajero_esperando, args=(metro_obj,)).start()
    Thread(target=quitar_pasajero_esperando, args=(metro_obj,)).start()
    root.mainloop()
