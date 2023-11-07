import tkinter as tk
from proyecto2 import Metro, pasajero, metro
import threading

class InterfazMetro(Metro):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.label = tk.Label(root)
        self.label.pack()
        self.canvas = tk.Canvas(root, width=400, height=200)
        self.canvas.pack()
        self.metro = self.canvas.create_rectangle(50, 50, 350, 150, fill="blue")
        self.puertas = [self.canvas.create_rectangle(150, 50, 200, 150, fill="yellow"),
                        self.canvas.create_rectangle(200, 50, 250, 150, fill="yellow")]
        self.pasajeros = [self.canvas.create_oval(100+i*20, 30, 120+i*20, 50, fill="red") for i in range(10)]

    def actualizar_interfaz(self, mensaje, color):
        self.label.config(text=mensaje)
        for puerta in self.puertas:
            self.canvas.itemconfig(puerta, fill=color)
        for i in range(10):
            if i < self.pasajeros_dentro:
                self.canvas.coords(self.pasajeros[i], 100+i*20, 70, 120+i*20, 90)
            else:
                self.canvas.coords(self.pasajeros[i], 100+i*20, 30, 120+i*20, 50)
        self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    metro_obj = InterfazMetro(root)
    for i in range(10):
        threading.Thread(target=pasajero, args=(metro_obj,)).start()
    threading.Thread(target=metro, args=(metro_obj,)).start()
    root.mainloop()
