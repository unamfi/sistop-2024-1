import random

def fcfs(processes):
    total_time = 0
    turnaround_time = 0
    waiting_time = 0
    for process in processes:
        total_time += process[1]
        turnaround_time += total_time
        waiting_time += turnaround_time - process[0] - process[1]
    return total_time, turnaround_time / len(processes), waiting_time / len(processes)

def rr(processes, quantum):
    total_time = 0
    turnaround_time = 0
    waiting_time = 0
    queue = processes.copy()
    while queue:
        process = queue.pop(0)
        if process[1] > quantum:
            total_time += quantum
            queue.append((process[0], process[1] - quantum))
        else:
            total_time += process[1]
            turnaround_time += total_time
            waiting_time += turnaround_time - process[0] - process[1]
    return total_time, turnaround_time / len(processes), waiting_time / len(processes)

def spn(processes):
    total_time = 0
    turnaround_time = 0
    waiting_time = 0
    remaining_processes = processes.copy()
    remaining_processes.sort(key=lambda x: x[1])
    for process in remaining_processes:
        total_time += process[1]
        turnaround_time += total_time
        waiting_time += turnaround_time - process[0] - process[1]
    return total_time, turnaround_time / len(processes), waiting_time / len(processes)

def run_simulation():
    for i in range(5):
        print(f"Ejecución {i + 1}:")
        processes = []
        for process_id in range(5):
            arrival_time = random.randint(0, 10)
            burst_time = random.randint(2, 7)
            processes.append([process_id, arrival_time, burst_time])
            print(f"{process_id}: {arrival_time}, t={burst_time}", end='; ')

        total_fcfs, avg_turnaround_fcfs, avg_waiting_fcfs = fcfs(processes)
        print(f"\nFCFS: T={total_fcfs}, E={avg_turnaround_fcfs}, P={avg_waiting_fcfs}")

        quantum = 1
        total_rr, avg_turnaround_rr, avg_waiting_rr = rr(processes, quantum)
        print(f"RR{quantum}: T={total_rr}, E={avg_turnaround_rr}, P={avg_waiting_rr}")

        total_spn, avg_turnaround_spn, avg_waiting_spn = spn(processes)
        print(f"SPN: T={total_spn}, E={avg_turnaround_spn}, P={avg_waiting_spn}")
        print()

if __name__ == "__main__":
    run_simulation()