from defines import *

# Funkcja obsugujaca debugger. Czeka na sygnaly / zdarzenia
def debugger(pid):
    # Liczba wykonanych instrukcji
    icounter = 0

    # Przechwytywanie procesu o okreslonym PID
    ptrace(PTRACE_ATTACH, pid, 0, None)

    # Funkcja zwraca tuple zawierajaca ID procesu oraz
    # 2-bajtowy status
    status = waitpid(pid, 0)

    # Sprawdz czy udalo sie przechwycic wykonywanie procesu
    # (proces otrzymal sygnal SIGSTOP)
    if WIFSTOPPED(status[1]):
        if WSTOPSIG(status[1]) == list(signals.keys())[list(signals.values()).index('SIGSTOP')]:
            # Dopoki sledzony proces nie zakonczyl pracy
            while (WIFSTOPPED(status[1])):
                icounter += 1
                print(f"Proces jak dotad {icounter} instrukcji")
                # Nakaz potomkowi wykonac kolejna instrukcje
                ptrace(PTRACE_SINGLESTEP, pid, 0, 0)
                status = waitpid(pid, 0)
        else:
            print("Otrzymano inny sygnal o nr.: ", WSTOPSIG(status[1]))
            exit(2)
#

if __name__ == "__main__":
    if len(argv[1:]):
        debugger(int(argv[1]))
#