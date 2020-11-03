from ctypes import c_void_p

from defines import *

# Funkcja obsugujaca debugger. Czeka na sygnaly / zdarzenia
def debugger(pid):
    instr_addr = c_uint64(0x40102c) #c_ulonglong(0x40102c) #
    print("what: ", instr_addr)
    # Odczyt instrukcji ze wskazanej komorki pamieci
    org_instr       = bytes(ptrace(PTRACE_PEEKTEXT, pid, cast(byref(instr_addr), c_void_p), 0))
    print(f"Oryginalna zawartosc pamieci z adresu {instr_addr}: ", org_instr)
    exit()

    # Zapis specjalnej instrukcji int3 pod wskazany adres
    instr_trap = c_ulonglong((org_instr & 0xFFFFFF00) | 0xCC)
    ptrace(PTRACE_POKETEXT, pid, cast(byref(instr_addr), c_void_p), cast(byref(instr_trap), c_void_p))

    zm_instr       = ptrace(PTRACE_PEEKTEXT, pid, cast(byref(instr_addr), c_void_p), 0)
    print(f"Zmieniona zawartosc pamieci z adresu {instr_addr}: ", zm_instr)

    # kontynuuj wykonanie potomka, zaczekaj az dotrze to wyjatku
    ptrace(PTRACE_CONT, pid, 0, 0)

    # Petla debuggera - oczekujemy na dalsze zdarzenia
    status = wait()
    if (WIFSTOPPED(status[1])):
        print("Potomek otrzymal sygnal: ", WSTOPSIG(status[1]))

    # Pobierz aktualny stan RIP
    regs = RegsStruct()
    ptrace(PTRACE_GETREGS, pid, 0, byref(regs))
    print("Potomek zostal zatrzymany na adresie RIP = 0x{:016X}".format(regs.rip))

    # Przywroc oryginalna instrukcje, cofnij wskaznik instrukcji (RIP)
    ptrace(PTRACE_POKETEXT, pid, cast(byref(instr_addr), c_void_p), cast(byref(org_instr), c_void_p))
    regs.rip -= 1
    ptrace(PTRACE_SETREGS, pid, 0, byref(regs))

    # Wznow dzialanie
    ptrace(PTRACE_CONT, pid, 0, 0)
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