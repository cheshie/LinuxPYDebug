from collections import namedtuple
from os import execv, wait, WIFSTOPPED, fork, waitpid, WSTOPSIG, system
from sys import argv, exit
from ctypes import c_ulonglong, byref, cast, CDLL, c_uint64, c_void_p, Structure, c_int, c_size_t
from struct import pack
from binascii import hexlify
from mmap import PAGESIZE
from os import getcwd

# get stdlib from ctypes => is it called stdlib??
libc = CDLL('libc.so.6')
# TODO: WHAT ARE THESE FOR?
libc.ptrace.argtypes = [c_uint64, c_uint64, c_uint64, c_void_p]
# libc.ptrace.argtypes = [c_uint64, c_uint64, c_void_p, c_void_p]
libc.ptrace.restype = c_uint64

# Memory protection (mprotect)
mprotect = libc.mprotect
mprotect.restype  = c_uint64
mprotect.argtypes = [c_uint64, c_uint64, c_uint64]
PROT_NONE = 0x0
PROT_READ = 0x1
PROT_WRITE = 0x2
PROT_EXEC = 0x04

# Ptrace calls
ptrace = libc.ptrace
PTRACE_TRACEME    = 0
PTRACE_SINGLESTEP = 9
PTRACE_ATTACH     = 16
PTRACE_DETACH     = 17
PTRACE_SYSCALL    = 24

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
# Defined in user.h
# source: https://code.woboq.org/userspace/glibc/sysdeps/unix/sysv/linux/x86/sys/user.h.html
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
# Most common signals used in examples
signals = {
    2  : 'SIGINT',
    5  : 'SIGTRAP',
    11 : 'SIGSEGV',
    15 : 'SIGTERM',
    18 : 'SIGCONT',
    19 : 'SIGSTOP',
}


# Load maps for specific process
maps = namedtuple('mapping', ['addr_start', 'addr_end', 'permissions', 'offset', 'device_id', 'inode', 'map_name'])
def load_maps(pid):
    with open('/proc/{}/maps'.format(pid), 'r') as h_maps:
        for line in h_maps.readlines():
            parts    = line.split()
            map_line = maps(
                *map(lambda x: int(x, 16), parts[0].split('-')),
                parts[1],
                int(parts[2], 16),
                parts[3],
                parts[4],
                parts[5] if len(parts) > 5 else ''
            )
            yield map_line
#

