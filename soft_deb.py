from defines import *

regs = RegsStruct()

# Funkcja obsugujaca debugger. Czeka na sygnaly / zdarzenia
def debugger(pid):
    breakpoint1_addr = 0x0000000000401d05# 0x0000000000001169 #0x40102c
    status = wait()

    while WIFSTOPPED(status[1]):
        soft_bp(pid, breakpoint1_addr)
        ptrace(PTRACE_SINGLESTEP, pid, 0, 0)
        status = wait()

def soft_bp(pid, instr_addr):
    # Pobierz aktualny stan RIP
    ptrace(PTRACE_GETREGS, pid, 0, byref(regs))
    print("\nPotomek zostal zatrzymany na adresie RIP = 0x%x" % (regs.rip))

    # Odczyt instrukcji ze wskazanej komorki pamieci
    org_instr = ptrace(PTRACE_PEEKTEXT, pid, c_ulonglong(instr_addr), 0)
    print("Oryginalna zawartosc pamieci z 0x%x:  0x%x" % (instr_addr, org_instr))

    # Zapis specjalnej instrukcji int3 pod wskazany adres
    instr_trap = (org_instr & 0xFFFFFFFFFFFFFF00) | 0xCC
    ptrace(PTRACE_POKETEXT, pid, instr_addr, instr_trap)
    zm_instr = ptrace(PTRACE_PEEKTEXT, pid, instr_addr, 0)
    print("Zmieniona zawartosc pamieci z 0x%x:  0x%x" % (instr_addr, zm_instr))

    # kontynuuj wykonanie potomka, zaczekaj az dotrze do wyjatku
    ptrace(PTRACE_CONT, pid, 0, 0)

    # Petla debuggera - oczekujemy na dalsze zdarzenia
    status = wait()
    if (WIFSTOPPED(status[1])):
        print("Potomek otrzymal sygnal: ", WSTOPSIG(status[1]))

    # Pobierz aktualny stan RIP
    ptrace(PTRACE_GETREGS, pid, 0, byref(regs))
    print("Potomek zostal zatrzymany na adresie RIP = 0x%x" % (regs.rip))

    # Przywroc oryginalna instrukcje, cofnij wskaznik instrukcji (RIP)
    ptrace(PTRACE_POKETEXT, pid, instr_addr, org_instr)
    regs.rip -= 1
    ptrace(PTRACE_SETREGS, pid, 0, byref(regs))

    input()
#

# Proces debugowany (potomek)
def debugee(progname):
    # Zezwalaj na debugowanie tego procesu
    ptrace(PTRACE_TRACEME, 0, 0, 0)

    # Uruchom program o nazwie progname
    execv(progname, (progname, str(0)))
#

if __name__ == "__main__":
    pid = fork()

    # Debugger jako rodzic
    if pid:
        debugger(pid)
    else:
        # Debuggowany potomek
        debugee(argv[1])
#