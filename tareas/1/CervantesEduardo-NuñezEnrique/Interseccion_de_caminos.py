import threading
import random
import time

''' Hago uso del patron con semáforos multiplex para tener contemplada la situación en la que puede haber 4 carros en cada una de las diferentes secciones de la intersección 
sin chocar, y de esa manera no bloquear toda la intersección para un carro. Además, permite un mejor flujo del tráfico'''
multiplex = threading.Semaphore(4) 
'''Este semáforo tradicional controla la variable carril que es compartida por los hilos, de esta manera no se pierde la información del carril
o se generan cambios inesperados de carril'''
sem_carril = threading.Semaphore(1) # 
#Cada uno de estos semáforos controla una de las partes de la sección crítica en las que puede haber solo un carro
sem_interseccion1 = threading.Semaphore(1)
sem_interseccion2 = threading.Semaphore(1)
sem_interseccion3  = threading.Semaphore(1)
sem_interseccion4 = threading.Semaphore(1)

'''Las intersecciones o el espacio compartido por los carros esta representado por arreglos que registran los carros que han pasado en ellas, guardando el número de auto, estas
variables son las que pueden generar una condición de carrera entre los hilos'''
interseccion1 = []
interseccion2 = []
interseccion3 = []
interseccion4 = []

'''En esta función dependiendo del carril en el que va un carro y su destino, decide la intersección a la que cruza . Todas las intersecciones son protegidas por su propio semaforo 
de esta manera puede haber 4 carros en toda la intersección sin que existan choques o problemas en la escritura de los arreglos de intersección'''
def intersection_change(a, carril):
        if carril == 1:
            sem_interseccion1.acquire()
            global interseccion1
            interseccion1.append("Auto: %d" % a)
            print('ENTRADA - el auto: %d, llego a la intersección %d' % (a, carril))
            time.sleep(random.random()) #Se agregó un sleep para que se observe de mejor manera la concurrrencia
            print('SALIDA - el auto: %d, salio de la intersección %d' % (a, carril))
            sem_interseccion1.release()
        elif carril == 2:
            sem_interseccion2.acquire()
            global interseccion2
            interseccion2.append("Auto: %d" % a)
            print('ENTRADA - el auto: %d, llego a la intersección %d' % (a, carril))
            time.sleep(random.random())
            print('SALIDA - el auto: %d, salio de la intersección %d' % (a, carril))
            sem_interseccion2.release()
        elif carril == 3:
            sem_interseccion3.acquire()
            global interseccion3
            interseccion3.append("Auto: %d" % a)
            print('ENTRADA - el auto: %d, llego a la intersección %d' % (a, carril))
            time.sleep(random.random())
            print('SALIDA - el auto: %d, salio de la intersección %d' % (a, carril))
            sem_interseccion3.release()
        elif carril == 4:
            sem_interseccion4.acquire()
            global interseccion4
            interseccion4.append("Auto: %d" % a)
            print('ENTRADA - el auto: %d, llego a la intersección %d' % (a, carril))
            time.sleep(random.random())
            print('SALIDA - el auto: %d, salio de la intersección %d' % (a, carril))
            sem_interseccion4.release()

'''Esta función indica  al cambio de intersecciones como debe cruzar un carro, de donde viene y aonde va, por tanto por que partes de la intersección pasará, de esta manera
los semáforos pueden sincronizar y evitar perdidas de información.'''
def chokezone(a, carril, y):
        intersection_change(a, carril)
        intersection_change(a,y)
        print('FINAL - El auto: %d continua su camino libre de choques' % a)

'''Esta función se encarga de crear el tráfico, mete autos en los carriles, permitiendo meter varios y a su vez los lleva a la gestión de la intersección o sección critica,
impidienndo choques'''
def transit(a):
    '''Multiplex esta aquí para que varios hilos puedan pasar pero solo una pueda obtener y entrar a la zona crítica con su carril antes de que otro cambie el valor 
    de carril, de esta forma pueden entrar varios autos a la zona critica, haber mejor flujo y de evitar los choques se encargan los otros semaforos'''
    multiplex.acquire() 
    sem_carril.acquire()#protejo carril para que no se cambie ningun carro de carril sin querer, tomando en cuenta la concurrencia
    carril = random.randint(1,4)
    print('INICIO - El auto: %d, va por el carril %d' % (a, carril))

    '''El multiplex va arriba por lo mencionado, pero identifico esta como la sección crítica'''
    if carril == 1:
        '''Dejo carriles para que los otros autos puedan tomar uno y haya un buen flujo, no me afecta después desproteger la variable porque interpreto que
        los carriles se vuelven locales en la función para cada hilo, así como algunas otras variables manejadas solo en las funciones'''
        sem_carril.release() 
        chokezone(a, carril, 4)
        multiplex.release() #Todos los condicionales llevan realese, para cuando acabe de pasar cada auto totalmente al otro lado, deje tomar la ejecución a otro.
    elif carril == 2:
        sem_carril.release()
        chokezone(a, carril, 3)
        multiplex.release()
    elif carril == 3:
        sem_carril.release()
        chokezone(a, carril, 1)
        multiplex.release()
    elif carril == 4:
        sem_carril.release()
        chokezone(a, carril, 2)
        multiplex.release()

def main():
    for i in range(5): #Modificar el rango para probar con mayores tráficos
        threading.Thread(target=transit, args=[i]).start()

main()