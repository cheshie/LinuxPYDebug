from defines import *

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
            input()
            ptrace(PTRACE_CONT, pid, 0, 0)
            
#

def mem_bp(pid):
    # Pobierz aktualny stan RIP
    ptrace(PTRACE_GETREGS, pid, 0, byref(regs))
    print("\nPotomek zostal zatrzymany na adresie RIP = 0x%x" % (regs.rip))

    # Zachowaj aktualna instrukcje oraz stan rejestrow
    backup_regs = RegsStruct()
    regs = RegsStruct()
    ptrace(PTRACE_GETREGS, pid, 0, byref(backup_regs))
    ptrace(PTRACE_GETREGS, pid, 0, byref(regs))
    org_instr = ptrace(PTRACE_PEEKDATA, pid, c_ulonglong(regs.rip), 0)
    print("Oryginalna zawartosc pamieci z 0x%x:  0x%x" % (regs.rip, org_instr))

    # zmien instrukcje na syscall, przygotuj rejestry do mprotect
    regs.rax = 10 # mprotect - system call nr
    regs.rdi = get_page_start_addr(int(argv[1], 16)) + 0x1000 # adres startu
    print("BP ustawiony na:", hex(get_page_start_addr(int(argv[1], 16)) + 0x1000))
    regs.rsi = 1024# dlugosc
    regs.rdx = PROT_NONE # protection
    
    ptrace(PTRACE_SETREGS, pid, 0, byref(regs))
    ptrace(PTRACE_POKEDATA, pid, c_ulonglong(regs.rip), 0x050f)
    ptrace(PTRACE_SINGLESTEP, pid, 0, 0)
    
    ptrace(PTRACE_GETREGS, pid, 0, byref(regs))
    print("Memprotect result: ", regs.rax)

    # Przywroc oryginalne instrukcje oraz stan rejestrow
    ptrace(PTRACE_SETREGS, pid, 0, byref(backup_regs))
    ptrace(PTRACE_POKEDATA, pid, c_ulonglong(backup_regs.rip), org_instr)
    # kontynuuj wykonanie
    ptrace(PTRACE_CONT, pid, 0, 0)

# Get start address
def get_page_start_addr(addr):
    return addr & -PAGESIZE

if __name__ == "__main__":
    debugger(int(argv[2]))

