from random import randint
from defines import *

regs = RegsStruct()

# Funkcja obsugujaca debugger. Czeka na sygnaly / zdarzenia
def debugger(pid):
    # Przechwytywanie procesu o okreslonym PID
    ptrace(PTRACE_ATTACH, pid, 0, None)

    # Obliczanie adresu przerwania
    instr_offset = 0x11a9 - 0x1000

    maps = load_maps(pid)

    text_segment = list(filter(
        lambda x: x.map_name == f"{getcwd()}/hello_loop" and x.permissions == 'r-xp',
        maps
    ))[0]

    instr_addr = text_segment.addr_start + instr_offset

    # Funkcja zwraca tuple zawierajaca ID procesu oraz
    # 2-bajtowy status
    status = waitpid(pid, 0)

    while WIFSTOPPED(status[1]):
        modify(pid, instr_addr)
        ptrace(PTRACE_SINGLESTEP, pid, 0, 0)
        status = wait()
#

def modify(pid, instr_addr):
    # Odczyt instrukcji ze wskazanej komorki pamieci
    org_instr = ptrace(PTRACE_PEEKTEXT, pid, c_ulonglong(instr_addr), 0)

    # Zapis specjalnej instrukcji int3 pod wskazany adres
    instr_trap = (org_instr & 0xFFFFFFFFFFFFFF00) | 0xCC
    ptrace(PTRACE_POKETEXT, pid, instr_addr, instr_trap)
    zm_instr = ptrace(PTRACE_PEEKTEXT, pid, instr_addr, 0)

    # kontynuuj wykonanie potomka, zaczekaj az dotrze do wyjatku
    ptrace(PTRACE_CONT, pid, 0, 0)

    # Petla debuggera - oczekujemy na dalsze zdarzenia
    status = wait()
    if (WIFSTOPPED(status[1])):
        print("Proces otrzymal sygnal: ", signals[WSTOPSIG(status[1])])

    # Pobierz aktualny stan RIP
    ptrace(PTRACE_GETREGS, pid, 0, byref(regs))
    print("RIP = 0x%x" % (regs.rip))
    print("Orig. RDI = 0x%x : %d" % (regs.rdi, regs.rdi))

    # Przywroc oryginalna instrukcje, cofnij wskaznik instrukcji (RIP)
    ptrace(PTRACE_POKETEXT, pid, instr_addr, org_instr)
    regs.rip -= 1
    regs.rdi = randint(0, 100)
    ptrace(PTRACE_SETREGS, pid, 0, byref(regs))
    print()
#



if __name__ == "__main__":
    if len(argv[1:]):
        debugger(int(argv[1]))
#