import tkinter as tk
import threading
import time
import random

# Datos de muestra para las habitaciones del hotel
habitaciones_disponibles = {
    "101": "Disponible",
    "102": "Disponible",
    "103": "Disponible",
    "104": "Disponible",
    "105": "Disponible",
    "106": "Disponible",
    "107": "Disponible",
    "108": "Disponible",
    "109": "Disponible",
    "110": "Disponible",
# Agregar más habitaciones según sea necesario
}

# Mutex para proteger las operaciones en habitaciones_disponibles
mutex = threading.Lock()

# Función para hacer el check-in
def hacer_check_in(habitacion, nombre_cliente, lista_habitaciones, mensaje_label, ocupadas_text):
    with mutex:
        if habitacion in habitaciones_disponibles:
            if habitaciones_disponibles[habitacion] == "Disponible":
                habitaciones_disponibles[habitacion] = nombre_cliente
                notificar(mensaje_label, f"{nombre_cliente} ha realizado el check-in en la habitación {habitacion}")
            else:
                notificar(mensaje_label, f"La habitación {habitacion} está ocupada, escoge una distinta.")
        else:
            notificar(mensaje_label, f"La habitación {habitacion} no existe.")

        verificar_disponibilidad(lista_habitaciones)

        if ocupadas_text is not None:
            actualizar_habitaciones_ocupadas(ocupadas_text)

# Función para hacer el check-out
def hacer_check_out(habitacion, nombre_cliente, lista_habitaciones, mensaje_label, ocupadas_text):
    with mutex:
        if habitacion in habitaciones_disponibles and habitaciones_disponibles[habitacion] == nombre_cliente:
            habitaciones_disponibles[habitacion] = "Disponible"
            notificar(mensaje_label, f"{nombre_cliente} ha realizado el check-out de la habitación {habitacion}")
        else:
            notificar(mensaje_label, f"{nombre_cliente} no puede realizar el check-out de la habitación {habitacion}")

        verificar_disponibilidad(lista_habitaciones)

        if ocupadas_text is not None:
            actualizar_habitaciones_ocupadas(ocupadas_text)

# Función para notificar mensajes en la parte inferior
def notificar(mensaje_label, mensaje):
    mensaje_label.config(text=mensaje)

# Función para verificar la disponibilidad de habitaciones
def verificar_disponibilidad(lista_habitaciones):
    lista_habitaciones.delete(0, tk.END)
    for habitacion, estado in habitaciones_disponibles.items():
        if estado == "Disponible":
            lista_habitaciones.insert(tk.END, f"Habitación {habitacion}")

# Función para actualizar el widget de habitaciones ocupadas
def actualizar_habitaciones_ocupadas(ocupadas_text):
    ocupadas_text.delete(1.0, tk.END)
    for habitacion, estado in habitaciones_disponibles.items():
        if estado != "Disponible":
            ocupadas_text.insert(tk.END, f"Habitación {habitacion} - Ocupada por {estado}\n")

def simular_reservas(lista_habitaciones, mensaje_label, ocupadas_text):
    while True:
        # Simular un cliente aleatorio y una habitación aleatoria
        cliente = "Cliente" + str(random.randint(1, 10))
        habitacion = random.choice(list(habitaciones_disponibles.keys()))

        if habitaciones_disponibles[habitacion] == "Disponible":
            hacer_check_in(habitacion, cliente, lista_habitaciones, mensaje_label, ocupadas_text)
        else:
            # Realizar un check-out aleatorio de una habitación ocupada
            habitacion_ocupada = random.choice([h for h, estado in habitaciones_disponibles.items() if estado != "Disponible"])
            hacer_check_out(habitacion_ocupada, habitaciones_disponibles[habitacion_ocupada], lista_habitaciones, mensaje_label, ocupadas_text)
        
        # Esperar un tiempo antes de la siguiente simulación
        time.sleep(1)

# Función para crear la interfaz de usuario
def crear_interfaz():
    app = tk.Tk()
    app.title("Habitaciones Disponibles")  # Título de la ventana

    # Campos de entrada
    nombre_label = tk.Label(app, text="Nombre del Cliente:")
    nombre_label.pack()

    # Campos de entrada
    nombre_entry = tk.Entry(app)
    nombre_entry.pack()

    habitacion_label = tk.Label(app, text="Número de Habitación:")
    habitacion_label.pack()

    habitacion_entry = tk.Entry(app)
    habitacion_entry.pack()

    check_in_button = tk.Button(app, text="Check-In", command=lambda: hacer_check_in(habitacion_entry.get(), nombre_entry.get(), lista_habitaciones, mensaje_label, ocupadas_text))
    check_in_button.pack()

    check_out_button = tk.Button(app, text="Check-Out", command=lambda: hacer_check_out(habitacion_entry.get(), nombre_entry.get(), lista_habitaciones, mensaje_label, ocupadas_text))
    check_out_button.pack()

    # Botón para simular reservas
    simular_button = tk.Button(app, text="Simular reserva", command=lambda: threading.Thread(target=simular_reservas, args=(lista_habitaciones, mensaje_label, ocupadas_text)).start())
    simular_button.pack()

    # Listbox para mostrar las habitaciones disponibles
    lista_habitaciones = tk.Listbox(app, selectbackground="#A18262", selectforeground="white")
    lista_habitaciones.pack()

    # Agregar habitaciones disponibles a la lista
    for habitacion, estado in habitaciones_disponibles.items():
        if estado == "Disponible":
            lista_habitaciones.insert(tk.END, f"Habitación {habitacion}")

    # Label para mostrar el mensaje de notificación
    mensaje_label = tk.Label(app, text="", fg="red")
    mensaje_label.pack()

    # Text widget para mostrar habitaciones ocupadas
    ocupadas_text = tk.Text(app, height=5, width=40)
    ocupadas_text.pack()

    # Iniciar la ventana de la aplicación
    app.mainloop()

# Crear un proceso para ejecutar la aplicación
if __name__ == "__main__":
    crear_interfaz()
