import threading
import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, Label, Button, Entry

# Inventario inicial
inventario = {}

# Condición para sincronizar el acceso al inventario
condition = threading.Condition()

class Aplicacion:
    def __init__(self, master):
        self.master = master
        master.title('Manejador de Inventario')

        self.label_inventario = tk.Label(master, text="Inventario:")
        self.label_inventario.pack()

        self.frame_inventario = tk.Frame(master)
        self.frame_inventario.pack()

        self.actualizar_inventario_label()

        self.boton_agregar_producto = tk.Button(master, text="Agregar Producto", command=self.agregar_producto)
        self.boton_agregar_producto.pack()

        self.boton_modificar_stock = tk.Button(master, text="Modificar Stock", command=self.modificar_stock)
        self.boton_modificar_stock.pack()

        self.boton_salir = tk.Button(master, text="Salir", command=self.salir)
        self.boton_salir.pack()

    def actualizar_inventario_label(self):
        for widget in self.frame_inventario.winfo_children():
            widget.destroy()
        for producto, cantidad in inventario.items():
            Label(self.frame_inventario, text=f"{producto}: {cantidad}").pack()

    def agregar_producto(self):
        producto = simpledialog.askstring("Agregar Producto", "Nombre del Producto:")
        if producto:
            with condition:
                if producto in inventario:
                    messagebox.showinfo("Información", "El producto ya existe.")
                else:
                    inventario[producto] = 0
                    condition.notify_all()
            self.actualizar_inventario_label()

    def modificar_stock(self):
        self.top = Toplevel(self.master)
        self.top.title("Modificar Stock")

        self.label_producto = Label(self.top, text="Producto:")
        self.label_producto.pack()

        self.entry_producto = Entry(self.top)
        self.entry_producto.pack()

        self.label_cantidad = Label(self.top, text="Cantidad:")
        self.label_cantidad.pack()

        self.entry_cantidad = Entry(self.top)
        self.entry_cantidad.pack()

        self.boton_agregar_stock = Button(self.top, text="Agregar Stock", command=self.agregar_stock)
        self.boton_agregar_stock.pack()

        self.boton_despachar_stock = Button(self.top, text="Despachar Stock", command=self.despachar_stock)
        self.boton_despachar_stock.pack()

    def agregar_stock(self):
        producto = self.entry_producto.get()
        try:
            cantidad = int(self.entry_cantidad.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido.")
            return

        with condition:
            if producto in inventario:
                inventario[producto] += cantidad
                condition.notify_all()
            else:
                messagebox.showerror("Error", "El producto no existe.")
                return
        self.actualizar_inventario_label()
        self.top.destroy()

    def despachar_stock(self):
        producto = self.entry_producto.get()
        try:
            cantidad = int(self.entry_cantidad.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido.")
            return

        with condition:
            if producto in inventario and inventario[producto] >= cantidad:
                inventario[producto] -= cantidad
                condition.notify_all()
            else:
                messagebox.showerror("Error", "Stock insuficiente o el producto no existe.")
                return
        self.actualizar_inventario_label()
        self.top.destroy()

    def salir(self):
        if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres salir?"):
            self.master.destroy()

root = tk.Tk()
app = Aplicacion(root)
root.mainloop()
