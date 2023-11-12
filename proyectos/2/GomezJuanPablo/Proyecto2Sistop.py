import threading
import time

# Variables globales para representar el estado de las habitaciones
habitaciones = {
    "habitacion1": "disponible",
    "habitacion2": "disponible",
    # Agrega más habitaciones según sea necesario
}

# Mutex para garantizar la exclusión mutua al reservar habitaciones
mutex_reserva = threading.Lock()

# Semáforo para controlar el acceso concurrente a la información de disponibilidad
sem_disponibilidad = threading.Semaphore(value=1)

def realizar_reserva(habitacion):
    global habitaciones

    # Verificar disponibilidad adquiriendo el semáforo
    sem_disponibilidad.acquire()

    if habitaciones[habitacion] == "disponible":
        # Bloquear el mutex antes de reservar
        with mutex_reserva:
            print(f"Reservando {habitacion}")
            # Simular proceso de reserva
            time.sleep(2)
            habitaciones[habitacion] = "reservada"
            print(f"Reserva de {habitacion} completada.")
    else:
        print(f"{habitacion} no está disponible para reserva.")

    # Liberar el semáforo después de la verificación de disponibilidad
    sem_disponibilidad.release()

def main():
    # Crear hilos para simular múltiples clientes que reservan habitaciones
    hilos_reserva = []
    for habitacion in habitaciones:
        hilo = threading.Thread(target=realizar_reserva, args=(habitacion,))
        hilos_reserva.append(hilo)
        hilo.start()

    # Esperar a que todos los hilos terminen
    for hilo in hilos_reserva:
        hilo.join()

if __name__ == "__main__":
    main()