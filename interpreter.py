# Instructions:
# 	pop ra
# 	push ra
# 	add ra, rb, rc		ra = rb + rc
# 	sub ra, rb, rc		ra = rb - rc
# 	xor ra, rb, rc		ra = rb xor rc
# 	or ra, rb, rc		ra = rb or rc
# 	and ra, rb, rc		ra = rb and rc
# 	not ra, rb			ra = not rb
# 	nop
# 	jmp ra 				jump to instruction ra
# 	jmpe ra, rb, rc		jump to instruction ra if rb == rc
# 	jmpl ra, rb, rc		jump to instruction ra if rb < rc
# 	jmpg ra, rb, rc		jump to instruction ra if rb < rc
# 	inc ra 				ra += 1
# 	dec ra 				ra -= 1
# 	mov ra, rb 			ra = rb; if either is in [] then treat as memory address
# 	print ra 			prints ascii value of ra
# 	read ra 			reads in single character or entire int
# 	halt				stops execution
# 	var name ra 		stores pointer with address ra
# 	label:				label style is "name:"

# Registers:
# 	r0-r15				regular registers
# 	rsp					stack pointer
# 	rbp					base pointer
# 	rax					return value for functions
# 	PC					Program Counter, points to next instruction

# Calling Convention:
# 	r10-r15 used as first 6 parameters, any others must be put on stack.
# 	Any other registers used in function must be backed up on stack.
# 	PC must always be backed up so function can return properly.			******it might be a good idea to implement call & ret instructions to handle PC******

# Memory:
# 	Main memory is 2^16 slots of python ints.
# 	Stack is 2^8 slots of python ints.