import random
import queue

class Proceso:
    def __init__(self, letra, tiempo, tiempoinicial):
        self.letra = letra
        self.tiempo = tiempo
        self.tiempoinicial = tiempoinicial

def fifo(processes):
    T, E, P = 0, 0, 0
    result = ""

    for process in processes:
        result += process.letra * process.tiempo
        T += process.tiempo
        E += T - process.tiempo

    T1 = T / len(processes)
    E1 = E / len(processes)
    P1 = T / T  # P = T / T in FIFO

    return result, T1, E1, P1

def rr(processes):
    T, E, P = 0, 0, 0
    result = ""
    quantum = 3 

    process_queue = queue.Queue()
    for process in processes:
        process_queue.put(process)

    while not process_queue.empty():
        process = process_queue.get()
        if process.tiempo > quantum:
            result += process.letra * quantum
            process.tiempo -= quantum
            process_queue.put(process)  
        else:
            result += process.letra * process.tiempo
            T += process.tiempo
            E += T - process.tiempo

    T1 = T / len(processes)
    E1 = E / len(processes)
    P1 = T / T  # P = T / T in RR

    return result, T1, E1, P1

def spn(processes):
    T, E, P = 0, 0, 0
    result = ""

    processes.sort(key=lambda p: (p.tiempoinicial, p.tiempo))

    for process in processes:
        result += process.letra * process.tiempo
        T += process.tiempo
        E += T - process.tiempo

    T1 = T / len(processes)
    E1 = E / len(processes)
    P1 = T / T  # P = T / T in SPN

    return result, T1, E1, P1

if __name__ == "__main__":
    num_procesos = ['A', 'B', 'C', 'D', 'E']
    processes = [Proceso(letra, random.randint(1, 10), random.randint(0, 9)) for letra in num_procesos]

    fifo_result, fifo_T, fifo_E, fifo_P = fifo(processes)
    rr_result, rr_T, rr_E, rr_P = rr(processes)
    spn_result, spn_T, spn_E, spn_P = spn(processes)

    print("FCFS")
    print(fifo_result)
    print("T =", fifo_T, " E =", fifo_E, "P =", fifo_P)

    print("RR1")
    print(rr_result)
    print("T =", rr_T, " E =", rr_E, "P =", rr_P)

    print("SPN")
    print(spn_result)
    print("T =", spn_T, " E =", spn_E, "P =", spn_P)
