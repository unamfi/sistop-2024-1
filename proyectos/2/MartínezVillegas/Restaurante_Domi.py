# -*- coding: utf-8 -*-

# Importación de bibliotecas necesarias
import threading
import tkinter as tk
from tkinter import ttk
from queue import Queue
import random
import time

# Clase Restaurante que maneja los pedidos
class Restaurante:
    def __init__(self):
        self.pedidos = Queue()  # Cola para los pedidos
        self.pedidos_listos = Queue()  # Cola para los pedidos listos

    # Función para recibir un pedido
    def recibir_pedido(self, nombre, apellido, pedido, direccion):
        if self.es_pedido_valido(pedido):
            self.pedidos.put((nombre, apellido, pedido, direccion))  # Agregar pedido a la cola de pendientes
            print(f"Pedido recibido de {nombre} {apellido}: {pedido}\n")
            self.preparar_comida()  # Llamar a la función de preparar comida
        else:
            print("No hay pedido por preparar\n")  # Mensaje si el pedido no es válido

    # Función para preparar comida
    def preparar_comida(self):
        if not self.pedidos.empty():
            pedido = self.pedidos.get()  # Obtener pedido de la cola de pendientes
            print(f"Preparando comida para pedido de {pedido[0]} {pedido[1]}\n")
            self.pedidos_listos.put(pedido)  # Agregar pedido a la cola de listos
            self.actualizar_gui()  # Llamar a la función de actualizar la GUI
            print(f"Pedido de {pedido[0]} {pedido[1]} listo\n")

    # Función para asignar pedidos a repartidores
    def asignar_pedidos_a_repartidores(self):
        while True:
            if not self.pedidos_listos.empty():
                pedido = self.pedidos_listos.get()  # Obtener pedido de la cola de listos
                repartidor = random.randint(1, 3)  # Asignar repartidor de manera aleatoria
                print(f"Pedido de {pedido[0]} {pedido[1]} asignado al repartidor {repartidor} para entrega en {pedido[3]}\n")
                time.sleep(2)  # Simular tiempo de entrega
                print(f"Pedido de {pedido[0]} {pedido[1]} entregado por repartidor {repartidor}\n")

    # Función para actualizar la GUI con los pedidos pendientes
    def actualizar_gui(self):
        pedidos_label.config(text=", ".join([f"Pedido de {pedido[0]} {pedido[1]}: {pedido[2]}\n" for pedido in self.pedidos.queue]))

    # Función para verificar si un pedido es válido
    def es_pedido_valido(self, pedido):
        return pedido.strip().lower() != "nada" and pedido.strip() != ""

# Función para iniciar la simulación
def iniciar_simulacion():
    rest = Restaurante()

    # Función para que el mesero tome pedidos, descartada
    def mesero():
        while True:
            pedido_info = mesero_queue.get()
            if pedido_info[0].lower() == 'q':
                break
            nombre, apellido, pedido, direccion = pedido_info
            rest.recibir_pedido(nombre, apellido, pedido, direccion)

    # Función para solicitar el nombre
    def solicitar_nombre():
        nombre = input("Ingrese su nombre: ")
        return nombre

    # Función para solicitar el apellido
    def solicitar_apellido():
        apellido = input("Ingrese su apellido: ")
        return apellido

    # Función para solicitar el pedido
    def solicitar_pedido():
        pedido = input("Ingrese su pedido: ")
        return pedido

    # Función para solicitar la dirección
    def solicitar_direccion():
        calle = input("Ingrese la calle: ")
        numero = input("Ingrese el número: ")
        colonia = input("Ingrese la colonia: ")
        return f"{calle} {numero}, {colonia}"

    # Función para que el cocinero prepare comida
    def cocinero():
        while True:
            rest.preparar_comida()

    # Función para que los repartidores entreguen pedidos
    def repartidor(num_repartidor):
        while True:
            rest.asignar_pedidos_a_repartidores()

    # Cola para los pedidos del mesero
    mesero_queue = Queue()

    # Iniciar hilos para meseros, cocineros y repartidores
    mesero_thread = threading.Thread(target=mesero)
    cocinero_thread = threading.Thread(target=cocinero)
    repartidor_thread_1 = threading.Thread(target=repartidor, args=(1,))
    repartidor_thread_2 = threading.Thread(target=repartidor, args=(2,))
    repartidor_thread_3 = threading.Thread(target=repartidor, args=(3,))

    mesero_thread.start()
    cocinero_thread.start()
    repartidor_thread_1.start()
    repartidor_thread_2.start()
    repartidor_thread_3.start()

    # Crear la interfaz gráfica
    root = tk.Tk()
    root.title("Sistema de Pedidos a Domicilio en Restaurante Pedro's")

    label_nombre = ttk.Label(root, text="Nombre:")
    label_nombre.pack()

    entry_nombre = ttk.Entry(root)
    entry_nombre.pack()

    label_apellido = ttk.Label(root, text="Apellido:")
    label_apellido.pack()

    entry_apellido = ttk.Entry(root)
    entry_apellido.pack()

    label_pedido = ttk.Label(root, text="Pedido:")
    label_pedido.pack()

    entry_pedido = ttk.Entry(root)
    entry_pedido.pack()

    label_calle = ttk.Label(root, text="Calle:")
    label_calle.pack()

    entry_calle = ttk.Entry(root)
    entry_calle.pack()

    label_numero = ttk.Label(root, text="Número de domicilio:")
    label_numero.pack()

    entry_numero = ttk.Entry(root)
    entry_numero.pack()

    label_colonia = ttk.Label(root, text="Colonia:")
    label_colonia.pack()

    entry_colonia = ttk.Entry(root)
    entry_colonia.pack()

    # Función para enviar el pedido desde la interfaz gráfica
    def enviar_pedido():
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        pedido = entry_pedido.get()
        calle = entry_calle.get()
        numero = entry_numero.get()
        colonia = entry_colonia.get()

        if not nombre or not apellido or not pedido or not calle or not numero or not colonia:
            advertencia_label.config(text="Favor de llenar todos los campos requeridos para su Pedido.")
            return

        advertencia_label.config(text="")  # Limpiar advertencia si todo está lleno

        entry_nombre.delete(0, tk.END)
        entry_apellido.delete(0, tk.END)
        entry_pedido.delete(0, tk.END)
        entry_calle.delete(0, tk.END)
        entry_numero.delete(0, tk.END)
        entry_colonia.delete(0, tk.END)
        mesero_queue.put((nombre, apellido, pedido, f"{calle} {numero}, {colonia}"))

    mesero_button = ttk.Button(root, text="Enviar Pedido", command=enviar_pedido)
    mesero_button.pack()

    global pedidos_label
    pedidos_label = ttk.Label(root, text="")
    pedidos_label.pack()

    global advertencia_label
    advertencia_label = ttk.Label(root, text="", foreground="red")
    advertencia_label.pack()

    root.mainloop()

# Iniciar la simulación
iniciar_simulacion()
