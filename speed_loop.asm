section .text
	global _start ; info for linker

_start:  						;tell linker entry point
	mov	rcx, 1000000 	;initialize loop with 1000000 iterations
	mov rax, 0

l1:	
	add	rax, 2				;add 2 to rax
	loop 	l1					;loop again
	
	mov 	rax, 60			;system call for exit 
	xor	rdi, rdi			;return value - 0
	syscall 
