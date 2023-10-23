import threading
from colorama import Fore
from random import seed
from random import randint

color_texto = [Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.RED, Fore.BLACK]


color_profesor = Fore.WHITE
num_alumnos = int(input(color_profesor + "Número de sillas: "))
contador = 0
mut_contador = threading.Semaphore(1)
num_dudas_alumnos = []
energia_profesor= 1000
num_alumnos_cubiculo = num_alumnos

for i in range(num_alumnos):
    num_dudas_alumnos.append(randint(10, 15))

dudas = [threading.Semaphore(1) for i in range(num_alumnos)]

def digo(num, msg):
    mi_color = color_texto[num % len(color_texto)]
    print(mi_color + '%4d // %d: %s' % (contador, num, msg))

def pregunto(quien):
    dudas[(quien + 1) % num_alumnos].acquire()
    digo(quien, 'Mi duda es [inserte duda existencial]\n')

def baja_mano(quien):
    dudas[(quien + 1) % num_alumnos].release()
    duda_resuelta(quien)


def duda_resuelta(quien):
    global num_alumnos_cubiculo
    num_dudas_alumnos[quien] = num_dudas_alumnos[quien]-1
    digo(quien,"Mi número de dudas es: " + str(num_dudas_alumnos[quien]))
    if num_dudas_alumnos[quien] <= 0:
        digo(quien, "No tengo más dudas. Me voy!")
        num_alumnos_cubiculo -= 1
        if(num_alumnos_cubiculo == 0):
            print(color_profesor + "Todos los alumnos han ido. ¡A dormir!")
            exit()

    
def piensa(quien):
    digo(quien, 'Pensando...')

def profesorApunta(quien):
    digo(quien, 'El profesor me cede la palabra')

def pregunta(quien):
    global contador
    digo(quien, 'Levanto la mano para ser escuchado')
    mut_contador.acquire()
    profesorApunta(quien)
    pregunto(quien)
    contador += 1
    digo(quien, 'El profesor respondió la duda')
    baja_mano(quien)
    if (contador==energia_profesor):
        print(color_profesor + "Muchas dudas por hoy. ¡A dormir!")
        exit()
    mut_contador.release()


def alumno(num):
    digo(num, 'Entrando al cubículo y sentándome')
    digo (num, "Mi número de dudas es: " + str(num_dudas_alumnos[num]))

    while num_dudas_alumnos[num] > 0:
        piensa(num)
        pregunta(num)
    

alumnos = [threading.Thread(target=alumno, args=[i]) for i in range(num_alumnos)]

print(color_profesor + "Soy el profesor y hoy es un gran día para resolver dudas.")
for i in alumnos:
    i.start()
