from defines import *

# Proces debugowany (potomek)
def debugee(progname):
    # Zezwalaj na debugowanie tego procesu
    ptrace(PTRACE_TRACEME, 0, 0, 0)

    # Uruchom program o nazwie progname
    execv(progname, (progname, str(0)))
#

# Proces debugger (rodzic). Czeka na sygnaly / zdarzenia
def debugger(pid):
    # Liczba wykonanych instrukcji
    icounter = 0
    # Oczekuj az potomek wykona pierwsza instrukcje
    status = wait()

    # Oczekuj na sygnaly od potomka do
    # momentu jego zatrzymania
    while (WIFSTOPPED(status[1])):
        icounter+=1
        # Nakaz potomkowi wykonac kolejna instrukcje
        ptrace(PTRACE_SINGLESTEP, pid, 0, 0)
        status = wait()

    print(f"Potomek wykonal {icounter} instrukcji")

if __name__ == "__main__":
    pid = fork()

    # Debugger jako rodzic
    if pid:
        debugger(pid)
    else:
        # Debuggowany potomek
        debugee(argv[1])
#