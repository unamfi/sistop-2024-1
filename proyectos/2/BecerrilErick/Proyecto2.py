import threading
import time
import random
import tkinter as tk
from queue import Queue

# Definición del teatro con 50 asientos
num_asientos = 50
asientos_disponibles = list(range(1, num_asientos + 1))
bloqueo = threading.Lock()
cola_reservas = Queue()
reservas_clientes = {}  # Diccionario para almacenar las reservas de los clientes

# Función para que un cliente reserve un asiento
def reserva_asiento(cliente, asiento_seleccionado):
    global asientos_disponibles
    with bloqueo:
        if asiento_seleccionado in asientos_disponibles:
            asientos_disponibles.remove(asiento_seleccionado)
            cola_reservas.put(asiento_seleccionado)
            reservas_clientes[asiento_seleccionado] = cliente
            return True
        else:
            return False

# Función para mostrar el estado actual de las reservas
def estado_reservas():
    reservas_frame.config(text="Reservas existentes:\n")
    for asiento, cliente in reservas_clientes.items():
        reservas_frame.config(text=reservas_frame.cget("text") + f"Asiento {asiento} está reservado por {cliente}.\n")

# Función para actualizar la lista de asientos disponibles en la interfaz gráfica
def actualizar_lista_asientos():
    lista_asientos.config(text=", ".join(map(str, asientos_disponibles)))

# Función para manejar la reserva cuando el cliente presiona el botón "Reservar"
def reservar_asiento():
    asiento_seleccionado = int(entry_asiento.get())
    if reserva_asiento(cliente_nombre.get(), asiento_seleccionado):
        actualizar_lista_asientos()
        entry_asiento.delete(0, tk.END)
        estado_reservas()  # Actualizar la visualización de las reservas

# Crear ventana de la interfaz gráfica
ventana = tk.Tk()
ventana.title("Reserva de Asientos")

# Etiqueta para el nombre del cliente
cliente_nombre = tk.StringVar()
etiqueta_nombre = tk.Label(ventana, text="Nombre del Cliente:")
etiqueta_nombre.pack()
entry_nombre = tk.Entry(ventana, textvariable=cliente_nombre)
entry_nombre.pack()

# Etiqueta para la selección de asiento
etiqueta_asiento = tk.Label(ventana, text="Selecciona un Asiento (1-50):")
etiqueta_asiento.pack()
entry_asiento = tk.Entry(ventana)
entry_asiento.pack()

# Botón para reservar un asiento
boton_reservar = tk.Button(ventana, text="Reservar", command=reservar_asiento)
boton_reservar.pack()

# Etiqueta para mostrar la lista de asientos disponibles
lista_asientos = tk.Label(ventana, text=", ".join(map(str, asientos_disponibles)))
lista_asientos.pack()

# Etiqueta para mostrar las reservas existentes
reservas_frame = tk.Label(ventana, text="Reservas existentes:\n")
reservas_frame.pack()

# Crear clientes (hilos) que intentarán reservar asientos
clientes = []
for i in range(10):  # 10 clientes
    cliente = threading.Thread(target=reserva_asiento, args=(i,))
    clientes.append(cliente)
    cliente.start()

# Esperar a que todos los clientes terminen de reservar
for cliente in clientes:
    cliente.join()

# Mostrar el estado final de las reservas
estado_reservas()

# Iniciar la interfaz gráfica
ventana.mainloop()
