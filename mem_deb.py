from defines import *

regs = RegsStruct()

# Funkcja obsugujaca debugger. Czeka na sygnaly / zdarzenia
def debugger(pid):
    # Przechwytywanie procesu o okreslonym PID
    ptrace(PTRACE_ATTACH, pid, 0, None)

    # Funkcja zwraca tuple zawierajaca ID procesu oraz
    # 2-bajtowy status
    status = waitpid(pid, 0)

    mem_bp(pid)

    # Petla debuggera - oczekujemy na dalsze zdarzenia
    while WIFSTOPPED(status[1]):
        # Petla debuggera - oczekujemy na dalsze zdarzenia
        status = wait()
        if (WIFSTOPPED(status[1])):
            print("Potomek otrzymal sygnal: ", signals[WSTOPSIG(status[1])])
#

def mem_bp(pid):
    # 1. Znalezc segment z kodem programu
    # instr_offset = 0x141e - 0x1000
    # maps = load_maps(pid)
    #
    # text_segment = list(filter(
    #     lambda x: x.map_name == f"{getcwd()}/memory" and x.permissions == 'r-xp',
    #     maps
    # ))[0]
    #
    # instr_addr = text_segment.addr_start + instr_offset

    # Pobierz aktualny stan RIP
    ptrace(PTRACE_GETREGS, pid, 0, byref(regs))
    print("\nPotomek zostal zatrzymany na adresie RIP = 0x%x" % (regs.rip))

    instr_addr = regs.rip

    # Zachowaj aktualna instrukcje oraz stan rejestrow
    backup_regs = RegsStruct()
    ptrace(PTRACE_GETREGS, pid, 0, byref(backup_regs))
    org_instr = ptrace(PTRACE_PEEKTEXT, pid, c_ulonglong(instr_addr), 0)
    print("Oryginalna zawartosc pamieci z 0x%x:  0x%x" % (instr_addr, org_instr))

    # zmien instrukcje na syscall, przygotuj rejestry do mprotect
    ptrace(PTRACE_POKETEXT, pid, c_ulonglong(instr_addr), 0x0000000000000f05)
    regs.rax = 0x10 # mprotect - system call nr
    regs.rdi = get_page_start_addr(int(argv[2], 16)) # adres startu
    regs.rsi = 0x1 * PAGESIZE # dlugosc - 1 strona pamieci
    regs.rdx = PROT_NONE # protection
    nowa_instr = ptrace(PTRACE_PEEKTEXT, pid, c_ulonglong(instr_addr), 0)
    print("Nowa zawartosc pamieci z 0x%x:  0x%x" % (instr_addr, nowa_instr))

    # wykonaj syscall
    ptrace(PTRACE_SYSCALL, pid, 0, 0)

    # Przywroc oryginalne instrukcje oraz stan rejestrow
    ptrace(PTRACE_SETREGS, pid, 0, byref(backup_regs))
    ptrace(PTRACE_POKETEXT, pid, c_ulonglong(instr_addr), org_instr)

    # kontynuuj wykonanie
    ptrace(PTRACE_CONT, pid, 0, 0)

# Get start address
def get_page_start_addr(addr):
    return addr & ~(PAGESIZE-1)

if __name__ == "__main__":
    debugger(int(argv[1]))

