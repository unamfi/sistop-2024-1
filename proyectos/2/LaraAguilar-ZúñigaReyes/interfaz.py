import threading
from tkinter import *

# Variables globales
pasajeros_dentro = 0
puertas_abiertas = False

# Funciones de simulación
def abrir_puertas():
    global puertas_abiertas
    puertas_abiertas = True
    actualizar_interfaz()

def cerrar_puertas():
    global puertas_abiertas
    puertas_abiertas = False
    actualizar_interfaz()

def subir_pasajero():
    global pasajeros_dentro
    pasajeros_dentro += 1
    actualizar_interfaz()

def bajar_pasajero():
    global pasajeros_dentro
    pasajeros_dentro -= 1
    actualizar_interfaz()

def actualizar_interfaz():
    pasajeros_label.config(text=f"Pasajeros dentro: {pasajeros_dentro}")
    puertas_label.config(text=f"Puertas abiertas: {puertas_abiertas}")

def simular():
    abrir_puertas()
    subir_pasajero()
    bajar_pasajero()
    cerrar_puertas()

# Funciones de botones
def iniciar_simulacion():
    threading.Thread(target=simular).start()

# Configuración de la interfaz
root = Tk()
root.title("Simulador de Metro")

# Etiquetas para mostrar el estado del metro
pasajeros_label = Label(root, text="Pasajeros dentro: 0")
pasajeros_label.pack()

puertas_label = Label(root, text="Puertas abiertas: False")
puertas_label.pack()

# Botón para iniciar la simulación
iniciar_button = Button(root, text="Iniciar Simulación", command=iniciar_simulacion)
iniciar_button.pack()

# Ejecutar interfaz gráfica
root.mainloop()
