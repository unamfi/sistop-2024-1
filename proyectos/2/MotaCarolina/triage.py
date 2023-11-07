import threading
from colorama import Fore


color_texto = [Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.RED, Fore.BLACK]
triage_rojo=[]
triage_amarillo=[]
triage_verde=[]


color_doctor = Fore.WHITE
num_pacientes = int(input(color_doctor + "Número de sillas y/o camillas en el hospital: "))
contador = 0
mut_contador = threading.Semaphore(1)
num_emergencias_pacientes = []
energia_doctor= 1000
num_pacientes_urgencias = num_pacientes

for i in range(num_pacientes):
    num_emergencias_pacientes.append(1)

dudas = [threading.Semaphore(1) for i in range(num_pacientes)]


#Función que expresa el diálogo de los hilos
def digo(num, msg):
    mi_color = color_texto[num % len(color_texto)]
    print(mi_color + '%4d // %d: %s' % (contador, num, msg))

#Se adquiere con acquire
def revision_medica(quien):
    dudas[(quien + 1) % num_pacientes].acquire()

#Se cede el control con release
def atencion(quien):
    dudas[(quien + 1) % num_pacientes].release()
    clasificando_paciente(quien)

#Se clasifica a un hilo(paciente) aleatoriamente y se modifica el arreglo que contiene las prioridades
def clasificando_paciente(quien):
    global num_pacientes_urgencias
    num_emergencias_pacientes[quien] = num_emergencias_pacientes[quien]-1
    if num_emergencias_pacientes[quien] <= 0:
        if(num_pacientes_urgencias == 0):
            print("Todos los pacientes han sido clasificados.")


#Se expresan la clasificación de todos los pacientes actualmente

#Se adquiere el poder para ofrecerle atención de parte del doctor y posteriormente se libera.
def salaUrgencias(quien):
    global contador
    mut_contador.acquire()
    revision_medica(quien)
    contador += 1
    atencion(quien)
    if (contador==energia_doctor):
        exit()
    mut_contador.release()
    


def paciente(num):
    while num_emergencias_pacientes[num] > 0:
        salaUrgencias(num)
    

pacientes = [threading.Thread(target=paciente, args=[i]) for i in range(num_pacientes)]

for i in pacientes:
    i.start()