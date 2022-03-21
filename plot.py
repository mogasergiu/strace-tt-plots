#!/usr/bin/env python3

import matplotlib.pyplot as plt
from datetime import datetime
import sys
import os

# sys.argv[1] - strace output file from `strace -tt path/to/binary 2>strace_outfile`
# sys.argv[2] - syscall names file
# sys.argv[3] - syscall timestamps file
# sys.argv[4] - command delay

setup_script = sys.argv[1]
strace_outfile = sys.argv[2]
syscall_names = sys.argv[3]
syscall_timestamps = sys.argv[4]
cmd_delay = sys.argv[5]

os.system(setup_script + " " + \
          strace_outfile + " " + \
          syscall_names + " " + \
          syscall_timestamps)

with open(syscall_names) as f:
    syscalls = f.read().splitlines()

with open(syscall_timestamps) as f:
    timestamps = f.read().splitlines()

fmt = "%H:%M:%S.%f"
last_timestamp = datetime.strptime(timestamps[-1], fmt)

delta_timestamps = []
for t in timestamps:
    delta_timestamps.append(float((str((last_timestamp - datetime.strptime(t, fmt)).total_seconds()))))

delta_timestamps = list(reversed(delta_timestamps))

for dot in range(len(delta_timestamps)):
    if delta_timestamps[dot] <= float(cmd_delay):
        plt.scatter(delta_timestamps[dot], syscalls[dot], c = "magenta")
    else:
        plt.scatter(delta_timestamps[dot], syscalls[dot], c = "blue")

plt.show()
