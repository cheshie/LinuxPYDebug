from defines import *

regs = RegsStruct()

# Funkcja obsugujaca debugger. Czeka na sygnaly / zdarzenia

def debugger(pid):
    breakpoint_dict = {'addr': 0x401042, 'org_instr' : ''}
    status = wait()

    while WIFSTOPPED(status[1]):
        set_bp(pid, breakpoint_dict)
        obsluga_zdarzenia(pid)
        unset_bp(pid, breakpoint_dict)
        status = wait()

def obsluga_zdarzenia(pid):
    # Wyswietl aktualny stan rejestrow oraz kontekst procesu
    ptrace(PTRACE_GETREGS, pid, 0, byref(regs))
    print("=================== DUMP =========================")
    print("RIP = 0x%x" % (regs.rip))
    print("RAX = 0x%x" % (regs.rax))
    print("RBX = 0x%x" % (regs.rbx))
    print("RCX = 0x%x" % (regs.rcx))
    print("RDX = 0x%x" % (regs.rdx))
    print("RSI = 0x%x" % (regs.rsi))
    print("RDI = 0x%x" % (regs.rdi))
    print("RSP = 0x%x" % (regs.rsp))
    print("RBP = 0x%x" % (regs.rbp))
    print("EFLAGS = 0x%x" % (regs.eflags))
    print("=================== DUMP =========================")
    print()


def unset_bp(pid, bp_dict):
    # Przywroc oryginalna instrukcje, cofnij wskaznik instrukcji (RIP)
    ptrace(PTRACE_POKETEXT, pid, bp_dict['addr'], bp_dict['org_instr'])
    regs.rip -= 1
    ptrace(PTRACE_SETREGS, pid, 0, byref(regs))

    input()
    ptrace(PTRACE_SINGLESTEP, pid, 0, 0)

def set_bp(pid, bp_dict):
    # Odczyt instrukcji ze wskazanej komorki pamieci
    org_instr = ptrace(PTRACE_PEEKTEXT, pid, c_ulonglong(bp_dict['addr']), 0)
    bp_dict['org_instr'] = org_instr

    # Zapis specjalnej instrukcji int3 pod wskazany adres
    instr_trap = (org_instr & 0xFFFFFFFFFFFFFF00) | 0xCC
    ptrace(PTRACE_POKETEXT, pid, bp_dict['addr'], instr_trap)

    # kontynuuj wykonanie potomka, zaczekaj az dotrze do wyjatku
    ptrace(PTRACE_CONT, pid, 0, 0)

    # Petla debuggera - oczekujemy na dalsze zdarzenia
    status = wait()
    if (WIFSTOPPED(status[1])):
        print("\nPotomek otrzymal sygnal: ", signals[WSTOPSIG(status[1])])
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