# Instructions:
# 	pop a 				a = stack[rsp]; decrementing rsp is up to program
# 	push a 				stack[rsp+1] = a; incrementing rsp is up to program
# 	add a, b, c			a = b + c
# 	sub a, b, c			a = b - c
# 	xor a, b, c			a = b xor c
# 	or a, b, c			a = b or c
# 	and a, b, c			a = b and c
# 	not a, b			a = not b
# 	nop
# 	jmp a 				jump to instruction a
# 	jmpe a, b, c		jump to instruction a if b == c
# 	jmpl a, b, c		jump to instruction a if b < c
# 	jmpg a, b, c		jump to instruction a if b < c
# 	inc a 				a += 1
# 	dec a 				a -= 1
# 	mov a, b 			a = b
# 	print a 			prints ascii value of a
# 	read a 				reads in single character or entire int
# 	halt				stops execution
# 	var name a 			stores pointer with address a, name can only be letters and cannot be the same as a register name
# 	label:				label style is "name:"
#*** if an argument is in [] then it is treated as a pointer to main memory
#*** otherwise if it is a name of a register it will be treated as such
#*** constants are 0d for decimal, 0x for hex, and 0b for binary
#*** trying to store something in a constant is not allowed

# Registers:
# 	r0-r15				regular registers
# 	rsp					stack pointer, supposed to point at top USED slot of stack
# 	rbp					base pointer
# 	rax					return value for functions
# 	PC					Program Counter, points to next instruction, that is what will be executed next

# Calling Convention:
# 	r10-r15 used as first 6 parameters, any others must be put on stack.
# 	Any other registers used in function must be backed up on stack.
# 	PC must always be backed up so function can return properly.			******it might be a good idea to implement call & ret instructions to handle PC******

# Memory:
# 	Main memory is 2^16 slots of python ints.
# 	Stack is 2^8 slots of python ints.

## first need to create variables used in all functions

# lists to hold memories
mem = [0] * (2**16)
stack = [0] * (2**8)

# dict of registers
reg = {"r0": 0,
		"r1": 0,
		"r2": 0,
		"r3": 0,
		"r4": 0,
		"r5": 0,
		"r6": 0,
		"r7": 0,
		"r8": 0,
		"r9": 0,
		"r10": 0,
		"r11": 0,
		"r12": 0,
		"r13": 0,
		"r14": 0,
		"r15": 0,
		"rsp": 0,
		"rbp": 0,
		"rax": 0,
		"PC": 0}

# variables is a dict that holds any var: address that are created
variables = {}

# program holds all the instructions of the program
program = []


## now define functions for all the instructions
# arguments are strings

def pop(a):
	if (a[0] == "["):
		global mem
		mem[int(a[1:-1])] = stack[reg["rsp"]]
	elif ((a[0] == "r" and isNum(a[1])) or a == "rsp" or a == "rbp" or a == "rax" or a == "PC"):
		global reg
		reg[a] = stack[reg["rsp"]]
	elif (a in variables):
		global mem
		mem[int(variables[a])] = stack[reg["rsp"]]
	else:
		print("Error when trying to pop into", a)
		errorTraceback()

def push(a):
	if (a[0] == "["):
		global stack
		stack[reg["rsp"] + 1] = mem[int(a[1:-1])]
	elif ((a[0] == "r" and isNum(a[1])) or a == "rsp" or a == "rbp" or a == "rax" or a == "PC"):
		global stack
		stack[reg["rsp"] + 1] = reg[a]
	elif (a in variables):
		global stack
		stack[reg["rsp"] + 1] = mem[int(variables[a])]
	else:
		print("Error when trying to push from", a)
		errorTraceback()

def add(a, b, c):
	b = getValue(b)
	c = getValue(c)

	if (a[0] == "["):
	elif ((a[0] == "r" and isNum(a[1])) or a == "rsp" or a == "rbp" or a == "rax" or a == "PC"):
	elif (a in variables):
	else:
		print("Error when trying to add", b, "and", c, "and stor in", a)
		errorTraceback()

def sub(a, b, c):


def xor(a, b, c):


def langOr(a, b, c):


def langAnd(a, b, c):


def langNot(a, b):


def no():


def jmp(a):


def jmpe(a, b, c):


def jmpl(a, b, c):


def jmpg(a, b, c):


def inc(a):


def dec(a):


def mov(a, b):


def langPrint(a):


def read(a):


def halt():


def var(name, a):


## helper functions

def isNum(n):
	try:
		int(n)
		return True
	except ValueError:
		return False

def errorTraceback():
	for key in reg:
		print(key, "has value", reg[key])
	quit()

def getValue(b):
	if (b[0] == "["):
		return mem[int(b[1:-1])]
	elif ((b[0] == "r" and isNum(b[1])) or b == "rsp" or b == "rbp" or b == "rax" or b == "PC"):
		return reg[b]
	elif (b in variables):
		return mem[int(variables[c])]
	else:
		print("Error when trying to get value of", b)
		errorTraceback()

def assignValue(location, value):
	if (location[0] == "["):
		global mem
		mem[int(location[1:-1])] = value
	elif ((location[0] == "r" and isNum(location[1])) or location == "rsp" or location == "rbp" or location == "rax" or location == "PC"):
		global reg
		reg[location] = value
	elif (location in variables):
		variables[location] = value
	else:
		print("Error when trying to assign" value, "to", location)
		errorTraceback()