from defines import *


# Proces debugowany (potomek)
def debugee(progname):
    # Zezwalaj na debugowanie tego procesu
    # ptrace(PTRACE_TRACEME, 0, 0, 0)

    # Uruchom program o nazwie progname
    execv(progname, (progname, str(0)))
#

# Funkcja obsugujaca debugger. Czeka na sygnaly / zdarzenia
def debugger(pid):
    # Przechwytywanie procesu o okreslonym PID
    ptrace(PTRACE_ATTACH, pid, 0, None)

    # Funkcja zwraca tuple zawierajaca ID procesu oraz
    # 2-bajtowy status
    status = waitpid(pid, 0)

    # Petla debuggera - oczekujemy na dalsze zdarzenia
    while WIFSTOPPED(status[1]):
        print("Child started, setting permissions")
        x = int(input("addr: "), 16)
        mem_bp(x)

        # kontynuuj wykonanie sledzonego procesu, zaczekaj az dotrze to wyjatku
        ptrace(PTRACE_CONT, pid, 0, 0)

        # Petla debuggera - oczekujemy na dalsze zdarzenia
        status = wait()
        if (WIFSTOPPED(status[1])):
            print("Potomek otrzymal sygnal: ", WSTOPSIG(status[1]))
#

def mem_bp(instr_addr):
    print("addr: ", hex(get_page_start_addr(instr_addr)))
    if mprotect(0x556d32db9000, PAGESIZE, PROT_WRITE):
        raise RuntimeError("Failed to set page permissions")
    else:
        print("Permissions set")

# Get start address
def get_page_start_addr(addr):
    return addr & ~(PAGESIZE-1)

if __name__ == "__main__":
    pid = fork()

    # Debugger jako rodzic
    if pid:
        debugger(pid)
    else:
        # Debuggowany potomek
        debugee(argv[1])
#
