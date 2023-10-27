import threading
import time
import random


capacidadMax =5 #capacidad del cubiculo
num_alumnos =  random.randint(1,20) #numero de alumnos que quieren una asesoria con el profesor

# Definimos semáforos y mutex
semprofesor = threading.Semaphore(1)  # Semáforo para controlar acceso al profesor
semalumnos = threading.Semaphore(capacidadMax-1)   # Semáforo para controlar número de alumnos en el cubiculo, se puede ver como las sillas disponibles
mutex = threading.Lock()                    

# Comportamiento del alumno
def alumno(id_alumno):
    global semprofesor
    global semalumnos
    global mutex
    global capacidadMax

    semalumnos.acquire() #un alumno toma el lugar disponible para entrar al cubiculo
    with mutex:
        print(f"Alumno {id_alumno} entra al cubiculo y espera su turno.")
        capacidadMax -=1
        
    

    semprofesor.release()  # Despierta al profesor
    #semprofesor.release()  # Despierta al profesor

    with mutex:
        print(f"Alumno {id_alumno} está hablando con el profesor.")
    
    # Simula el tiempo que el profesor necesita para responder la pregunta
    time.sleep(random.randint(1, 5))
    
    
    with mutex:
        print(f"Alumno {id_alumno} ha salido del aula.")
        
    semalumnos.release() #liberamos el semaforo de alumnos una vez que se muestre que ha salido del cubiculo
    with mutex:
        capacidadMax +=1
        

#Comportamiento del profesor
def profesor():
    while capacidadMax==5:
        semprofesor.acquire() #cuando no hay alumnos entrando al salon
        print("El profesor está durmiendo...")
        time.sleep(random.randint(1, 5)) #duerme un tiempo aleatorio
        



print(f"El dia de hoy hay {num_alumnos} alumnos queriendo ser atendidos")



#hilo del profesor
profesor_thread = threading.Thread(target=profesor).start()



# Se crean los hilos para alumnos, cada alumno sera un hilo
threads = []
for i in range(num_alumnos):
    thread = threading.Thread(target=alumno, args=(i+1,))
    threads.append(thread)
    thread.start()




# Esperamos a que todos los hilos terminen
for thread in threads:
    thread.join()

print('Se ha terminado la jornada laboral de hoy')





