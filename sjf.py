def sjf_non_preemptive(data):
    # Assuming `data` is a list of tuples (process_id, arrival_time, burst_time)
    processes = sorted(data, key=lambda x: x[1])  # Sort by arrival time
    start_time = 0
    schedule = []
    waiting_list = []

    while processes or waiting_list:
        while processes and processes[0][1] <= start_time:
            waiting_list.append(processes.pop(0))
        waiting_list.sort(key=lambda x: x[2])  # Sort by burst time
        if waiting_list:
            pid, arrival, burst = waiting_list.pop(0)
            start_time = max(start_time, arrival)
            finish_time = start_time + burst
            schedule.append((pid, start_time, finish_time))
            start_time = finish_time
        else:
            start_time += 1

    return schedule


def sjf_preemptive(data):
    # Assuming `data` is a list of tuples (process_id, arrival_time, burst_time)
    from queue import PriorityQueue

    processes = sorted(data, key=lambda x: x[1])  # Sort by arrival time
    time = 0
    schedule = []
    waiting_queue = PriorityQueue()
    remaining_burst_times = {pid: burst for pid, arrival, burst in data}
    last_process = None

    while processes or not waiting_queue.empty() or last_process is not None:
        while processes and processes[0][1] <= time:
            pid, arrival, burst = processes.pop(0)
            waiting_queue.put((burst, arrival, pid))

        if last_process:
            pid, start_time, _ = last_process
            remaining_burst = remaining_burst_times[pid]
            if remaining_burst == 0:
                finish_time = time
                schedule.append((pid, start_time, finish_time))
                last_process = None
            elif not waiting_queue.empty() and waiting_queue.queue[0][0] < remaining_burst:
                waiting_queue.put((remaining_burst, start_time, pid))
                last_process = None

        if not last_process and not waiting_queue.empty():
            remaining_burst, arrival, pid = waiting_queue.get()
            if remaining_burst_times[pid] == remaining_burst:
                start_time = time
            else:
                start_time = time - (remaining_burst - remaining_burst_times[pid])
            last_process = (pid, start_time, remaining_burst)
            remaining_burst_times[pid] -= 1
        time += 1

    return schedule

