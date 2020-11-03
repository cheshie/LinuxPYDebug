from os import execv, wait, WIFSTOPPED, fork, waitpid, WSTOPSIG
from sys import argv, exit
from ctypes import c_ulonglong, byref, cast, CDLL, c_uint64, c_void_p, Structure

# get stdlib from ctypes => is it called stdlib??
libc = CDLL('libc.so.6')
# TODO: WHAT ARE THESE FOR?
libc.ptrace.argtypes = [c_uint64, c_uint64, c_void_p, c_void_p]
libc.ptrace.restype = c_uint64



ptrace = libc.ptrace
PTRACE_TRACEME    = 0
PTRACE_SINGLESTEP = 9
PTRACE_ATTACH     = 16
PTRACE_DETACH     = 17

# Breakpoints --------
# Search memory
PTRACE_PEEKTEXT   = 1
# Insert into memory
PTRACE_POKETEXT   = 4
# Continue execution
PTRACE_CONT       = 7


# Context actions - get registers etc ---
PTRACE_GETREGS    = 12
PTRACE_SETREGS    = 13

# Registers -----------
class RegsStruct(Structure):
    _fields_ = [
        ("r15", c_ulonglong),
        ("r14", c_ulonglong),
        ("r13", c_ulonglong),
        ("r12", c_ulonglong),
        ("rbp", c_ulonglong),
        ("rbx", c_ulonglong),
        ("r11", c_ulonglong),
        ("r10", c_ulonglong),
        ("r9", c_ulonglong),
        ("r8", c_ulonglong),
        ("rax", c_ulonglong),
        ("rcx", c_ulonglong),
        ("rdx", c_ulonglong),
        ("rsi", c_ulonglong),
        ("rdi", c_ulonglong),
        ("orig_rax", c_ulonglong),
        ("rip", c_ulonglong),
        ("cs", c_ulonglong),
        ("eflags", c_ulonglong),
        ("rsp", c_ulonglong),
        ("ss", c_ulonglong),
        ("fs_base", c_ulonglong),
        ("gs_base", c_ulonglong),
        ("ds", c_ulonglong),
        ("es", c_ulonglong),
        ("fs", c_ulonglong),
        ("gs", c_ulonglong),
    ]

# Signals
SIGSTOP = 19