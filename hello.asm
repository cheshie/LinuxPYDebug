	global	_start
	
	section	.text
_start:	mov	rax, 1		;system call for write
	mov 	rdi, 1		; file handle 1 => stdout
	mov 	rsi, msg	; adress of string to output
	mov 	rdx, 14		; number of bytes in message
	syscall
	mov	rax, 60
	xor	rdi, rdi	; exit code 0
	syscall			; invoke operating system to exit

	section	.data
msg:	db	"Child: Hello!",10	; newline at the end
	
