import threading
#programa sencillo de semaforos para imprimir 4 digitos
sem1= threading.Semaphore(0)
sem2 = threading.Semaphore(0)

def fun_1():
    print(1)
    sem1.release()
    sem2.acquire()
    print(3)
    sem1.release()


def fun_2():
    sem1.acquire()
    print(2)
    sem2.release()
    sem1.acquire()
    print(4)

threading.Thread(target=fun_1).start()
threading.Thread(target=fun_2).start()
    

