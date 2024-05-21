def rr_preemptive(data, time_quantum):
    # Assuming `data` is a list of tuples (process_id, arrival_time, burst_time)
    from collections import deque

    processes = deque(sorted(data, key=lambda x: x[1]))  # Sort by arrival time
    time = 0
    schedule = []
    ready_queue = deque()
    remaining_burst = {}
    
    while processes or ready_queue:
        while processes and processes[0][1] <= time:
            pid, arrival, burst = processes.popleft()
            ready_queue.append(pid)
            remaining_burst[pid] = burst

        if ready_queue:
            current_pid = ready_queue.popleft()
            burst_time = remaining_burst[current_pid]
            execution_time = min(burst_time, time_quantum)
            start_time = time
            finish_time = time + execution_time
            time = finish_time
            remaining_burst[current_pid] -= execution_time
            
            if remaining_burst[current_pid] > 0:
                ready_queue.append(current_pid)
            else:
                schedule.append((current_pid, start_time, finish_time))
        else:
            time += 1

    return schedule
