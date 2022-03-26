#!/usr/bin/env python3

import matplotlib.pyplot as plt
from datetime import datetime
import sys
import re
import threading

class Counter:
    def __init__(self, start = 0, total = 100):
        self.lock = threading.Lock()
        self.value = start
        self.next_fraction = int(total / 100)
        self.one_percent = int(total/ 100)
        self.next_percentage = 1

    def increment(self):
        self.lock.acquire()
        try:
            self.value = self.value + 1

            print(self.value, self.next_fraction)
            if self.value == self.next_fraction:
                print("Done: " + self.next_percentage + "%")
                self.next_percentage += 1
                self.next_fraction += self.one_percent

        finally:
            self.lock.release()

def thread_func(left, right, delta_timestamps, syscall_names, counter):
    for dot in range(left, right):
        plt.scatter(delta_timestamps[dot], syscall_names[dot], c = "blue")

        counter.increment()

# sys.argv[1] - strace output file from `strace -tt path/to/binary 2>strace_outfile`
# sys.argv[2] - command delay
# sys.argv[3] - number of threads to be used

if __name__ == "__main__":
    strace_outfile = sys.argv[1]
    cmd_delay = float(sys.argv[2])
    threads_count = int(sys.argv[3])

    with open(strace_outfile) as f:
        strace_results = f.read()

    rgx = re.compile(\
        r"^[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6} [a-z]*",\
        re.MULTILINE)

    syscall_names = []
    syscall_timestamps = []
    for match in rgx.findall(strace_results):
        syscall_timestamp, syscall_name = match.split(' ')

        syscall_timestamps.append(syscall_timestamp)
        syscall_names.append(syscall_name)

    fmt = "%H:%M:%S.%f"
    last_timestamp = datetime.strptime(syscall_timestamps[-1], fmt)

    delta_timestamps = []
    for t in syscall_timestamps:
        delta_timestamps.append(float((str((last_timestamp - datetime.strptime(t, fmt)).total_seconds()))))

    delta_timestamps = list(reversed(delta_timestamps))

    for dot in range(len(delta_timestamps)):
        if delta_timestamps[dot] <= cmd_delay:
            plt.scatter(delta_timestamps[dot], syscall_names[dot], c = "magenta")
        else:
            benchmark_timestamp_dot = dot
            break

    size_to_compute = len(delta_timestamps) - benchmark_timestamp_dot
    size_to_compute_per_thread = int(size_to_compute / threads_count)

    threads = []
    counter = Counter(benchmark_timestamp_dot, len(delta_timestamps))
    for t in range(threads_count - 1):
        left = benchmark_timestamp_dot + t * size_to_compute_per_thread
        right = benchmark_timestamp_dot + (t + 1) * size_to_compute_per_thread
        threads.append(threading.Thread(target = thread_func, \
                        args = (left, right, delta_timestamps, syscall_names, counter,)))

    left = benchmark_timestamp_dot + (threads_count - 1) * size_to_compute_per_thread
    right = len(delta_timestamps)
    threads.append(threading.Thread(target = thread_func, \
                        args = (left, right, delta_timestamps, syscall_names, counter,)))

    for t in threads:
        t.start()
	
    for t in threads:
        t.join()
	
    plt.show()
