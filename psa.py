def psa_non_preemptive(data):
    # Assuming `data` is a list of tuples (process_id, arrival_time, burst_time, priority)
    processes = sorted(data, key=lambda x: (x[1], x[3]))  # Sort by arrival time and priority
    start_time = 0
    schedule = []
    waiting_list = []

    while processes or waiting_list:
        while processes and processes[0][1] <= start_time:
            waiting_list.append(processes.pop(0))
        waiting_list.sort(key=lambda x: x[3])  # Sort by priority
        if waiting_list:
            pid, arrival, burst, priority = waiting_list.pop(0)
            start_time = max(start_time, arrival)
            finish_time = start_time + burst
            schedule.append((pid, start_time, finish_time))
            start_time = finish_time
        else:
            start_time += 1

    return schedule

def psa_preemptive(data):
    # Assuming `data` is a list of tuples (process_id, arrival_time, burst_time, priority)
    from queue import PriorityQueue

    processes = sorted(data, key=lambda x: (x[1], x[3]))  # Sort by arrival time and priority
    time = 0
    schedule = []
    waiting_queue = PriorityQueue()
    remaining_burst_times = {pid: burst for pid, arrival, burst, priority in data}
    last_process = None

    while processes or not waiting_queue.empty() or last_process is not None:
        while processes and processes[0][1] <= time:
            pid, arrival, burst, priority = processes.pop(0)
            waiting_queue.put((priority, burst, arrival, pid))

        if last_process:
            pid, start_time, _, _ = last_process
            if remaining_burst_times[pid] == 0:
                finish_time = time
                schedule.append((pid, start_time, finish_time))
                last_process = None
            elif not waiting_queue.empty() and waiting_queue.queue[0][0] < remaining_burst_times[pid]:
                waiting_queue.put((priority, remaining_burst_times[pid], start_time, pid))
                last_process = None

        if not last_process and not waiting_queue.empty():
            priority, remaining_burst, arrival, pid = waiting_queue.get()
            if remaining_burst_times[pid] == remaining_burst:
                start_time = time
            else:
                start_time = time - (remaining_burst - remaining_burst_times[pid])
            last_process = (pid, start_time, remaining_burst, priority)
            remaining_burst_times[pid] -= 1
        time += 1

    return schedule
