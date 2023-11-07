import threading
import tkinter as tk
from tkinter import messagebox, simpledialog

# Parámetros del inventario
inventario = {'producto': 10}

# Condición para sincronizar el acceso al inventario
condition = threading.Condition()

class Aplicacion:
    def __init__(self, master):
        self.master = master
        master.title('Manejador de Inventario')

        self.label_inventario = tk.Label(master, text=f"Inventario: {inventario['producto']}")
        self.label_inventario.pack()

        self.boton_agregar = tk.Button(master, text="Agregar Stock", command=self.agregar_stock)
        self.boton_agregar.pack()

        self.boton_despachar = tk.Button(master, text="Despachar Stock", command=self.despachar_stock)
        self.boton_despachar.pack()

        self.boton_salir = tk.Button(master, text="Salir", command=self.salir)
        self.boton_salir.pack()

    def actualizar_inventario_label(self):
        self.label_inventario['text'] = f"Inventario: {inventario['producto']}"

    def agregar_stock(self):
        cantidad = simpledialog.askinteger("Agregar Stock", "Cantidad:", minvalue=1)
        if cantidad:
            with condition:
                inventario['producto'] += cantidad
                condition.notify_all()
            self.actualizar_inventario_label()

    def despachar_stock(self):
        cantidad = simpledialog.askinteger("Despachar Stock", "Cantidad:", minvalue=1)
        if cantidad:
            with condition:
                if inventario['producto'] < cantidad:
                    messagebox.showerror("Error", "No hay suficiente stock.")
                    return
                inventario['producto'] -= cantidad
            self.actualizar_inventario_label()

    def salir(self):
        if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres salir?"):
            self.master.destroy()

root = tk.Tk()
app = Aplicacion(root)
root.mainloop()
