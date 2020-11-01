section .text
	global _start ; must be for GCC???

_start:  ; tell linker entry point
	mov	rcx, 10 	;initialize loop with 10 iterations
	mov	rax, '0'	;first value to print

l1:
	mov	[num], rax	;move contents of rax to address of num variable
	mov	rax, 1		;
	mov	rdi, 1		;
	mov	rsi, num	;
	mov 	rdx, 1
	push	rcx
	syscall
	
	mov	rax, [num]
	sub	rax, '0'
	inc	rax
	add	rax, '0'
	pop	rcx
	loop 	l1

	mov 	rax,60	; system call nr (sys_exit)
	xor	rdi,rdi	; call kernel
	syscall 

section .bss
	num resb 1
