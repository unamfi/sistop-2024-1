print("✦--- TAREA 1 | EL ELEVADOR ---✦\n")

print ("︙Implementación de una estrategia de sincronización utilizando hilos en Python.")
print ("︙Con la finalidad de simular eficazmente la operación del sistema de un ascensor.")
print ("︙Aquí una simulación de la solución propuesta:\n")

import threading
import time
import random

# Definimos la capacidad del elevador y el número de pisos.

cap_elevador = 5
num_pisos = 5

# Variables para el estado del elevador y la lista de personas esperando en cada piso.

estado_elevador = {
    'piso_actual': 1,
    'personas_dentro': [],
    'direccion': 1,  
    # Para dirigirse hacia arriba: 1.
    # Para dirigirse hacia abajo: -1.
}

personas_esperando = [[] for _ in range(num_pisos)]

# Mutex para controlar el acceso al estado compartido.

mutex = threading.Lock()

# Función para simular el movimiento del elevador.

def mover_elevador():
    global estado_elevador 
    # Declaracion de variable global para el estado del elevador.

    while True:
        with mutex:
            # Determinar el próximo piso a visitar.
            proximo_piso = estado_elevador['piso_actual'] + estado_elevador['direccion']

            # Verificar si alguien quiere bajar en el próximo piso.
            personas_bajando = personas_esperando[proximo_piso - 1]

            for persona in estado_elevador['personas_dentro'][:]:
                if persona['destino'] == proximo_piso:
                    personas_bajando.append(persona)
                    estado_elevador['personas_dentro'].remove(persona)

            # Si el elevador está vacío, buscar a personas que quieran subir.
            if not estado_elevador['personas_dentro']:
                for persona in personas_esperando[proximo_piso - 1][:]:
                    if persona['direccion'] == estado_elevador['direccion'] and len(estado_elevador['personas_dentro']) < cap_elevador:
                        estado_elevador['personas_dentro'].append(persona)
                        personas_esperando[proximo_piso - 1].remove(persona)

            # Cambiar de dirección si es necesario cuando llegamos al limite del elevador.
            if proximo_piso == num_pisos:
                # Hacia abajo.
                estado_elevador['direccion'] = -1
            elif proximo_piso == 1:
                # Hacia arriba.
                estado_elevador['direccion'] = 1

            # Actualizar el piso actual.
            estado_elevador['piso_actual'] = proximo_piso

            print(f"Elevador en piso {estado_elevador['piso_actual']}, {len(estado_elevador['personas_dentro'])} personas dentro.")

        time.sleep(2)  # Simulación de tiempo de viaje.

# Función para simular el comportamiento de las personas.

def persona(id_persona):
    global estado_elevador

    while True:
        origen = random.randint(1, num_pisos)
        destino = random.randint(1, num_pisos)
        while origen == destino:
            destino = random.randint(1, num_pisos)
        
        # Indicamos la dirección. 
        direccion = 1 if destino > origen else -1

        with mutex:
            if len(estado_elevador['personas_dentro']) < cap_elevador and estado_elevador['direccion'] == direccion:
                estado_elevador['personas_dentro'].append({'id': id_persona, 'destino': destino})
                print(f"Persona {id_persona} sube al elevador, en piso {origen} con destino a piso {destino}.")
            else:
                personas_esperando[origen - 1].append({'id': id_persona, 'direccion': direccion, 'destino': destino})
                print(f"Persona {id_persona}, espera en piso {origen} para ir al piso {destino}.")

        time.sleep(random.uniform(0.5, 2))  # Tiempo de espera antes de intentar de nuevo.

# Creamos un thread para el elevador y varios threads para las personas.

elevador_thread = threading.Thread(target=mover_elevador)
elevador_thread.start()

personas_threads = []
for i in range(10):  # Cambiar el número de personas según sea necesario.
    persona_thread = threading.Thread(target=persona, args=(i,))
    personas_threads.append(persona_thread)
    persona_thread.start()

# Esperar a que todos los threads terminen (esto no se detendrá ya que es una simulación infinita).

elevador_thread.join()
for persona_thread in personas_threads:
    persona_thread.join()