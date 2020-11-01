import ctypes

# get stdlib from ctypes => is it called stdlib??
libc = ctypes.CDLL('libc.so.6')
ptrace = libc.ptrace
PTRACE_TRACEME    = 0
PTRACE_SINGLESTEP = 9
PTRACE_ATTACH     = 16
PTRACE_DETACH     = 17


# Signals
SIGSTOP = 19