#!/usr/bin/env bash

STRACE_TT_OUTPUT=${1}  # file resulted out of `strace =tt /path/to/binary 2>/strace_outfile
SYSCALL_NAMES_FILE=${2}
SYSCALL_TIMESTAMPS_FILE=${3}

echo ${SYSCALL_TIMESTAMPS_FILE} ${SYSCALL_NAMES_FILE} > log.err

cat ${STRACE_TT_OUTPUT} | cut -d' ' -f1 > ${SYSCALL_TIMESTAMPS_FILE}
cat ${STRACE_TT_OUTPUT} | cut -d' ' -f2 | cut -d'(' -f1 > ${SYSCALL_NAMES_FILE}

