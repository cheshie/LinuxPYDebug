section .text
	global _start ; info for linker

_start:  ; tell linker entry point
	mov	rcx, 10 	;initialize loop with 10 iterations
	mov	rax, '0'	;first value to print

l1:
	mov	[num], rax	;move contents of rax to address of num variable
	mov	rax, 1		;system call for write
	mov	rdi, 1		;file handle 1 => stdout
	mov	rsi, num	;move address of num to rsi to prepare it to print
	mov 	rdx, 1		;size of printed message in bytes
	push	rcx		;save value of rcx - it gets cleared after syscall
	syscall
	
	mov	rax, [num]	;move back data from num address to rax
	sub	rax, '0'	;convert text to integer
	inc	rax		;increment integer
	add	rax, '0'	;convert integer to text
	pop	rcx		;restore RCX for loop control
	loop 	l1		;loop again

	mov 	rax, 60		; system call for exit 
	xor	rdi, rdi	; return value - 0
	syscall 

section .bss
	num resb 1
