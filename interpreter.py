# Instructions:
# 	pop a 				a = stack[rsp]; rsp -= 1
# 	push a 				stack[rsp+1] = a; rsp += 1
# 	add a, b, c			a = b + c
# 	sub a, b, c			a = b - c
# 	xor a, b, c			a = b xor c
# 	or a, b, c			a = b or c
# 	and a, b, c			a = b and c
# 	not a, b			a = not b
#	shiftr a, b, c 		a = b shifted c bits right
#	shiftl a, b, c 		a = b shifted c bits left
# 	nop
# 	jmp a 				jump to instruction a
# 	jmpe a, b, c		jump to instruction a if b == c
# 	jmpl a, b, c		jump to instruction a if b < c
# 	jmpg a, b, c		jump to instruction a if b < c
# 	inc a 				a += 1
# 	dec a 				a -= 1
# 	mov a, b 			a = b
# 	print a, b 			if b == 0, prints int value of a, else prints ascii value of a
# 	read a 				reads in single character or entire int
# 	halt				stops execution
#	call 				pushes PC onto the stack and jumps to label
#	ret 				pops top of stack and returns to that instruction, if function coded correctly will be PC
# 	var name a 			stores value a in memory, can get memory address with [name], name can only be letters and cannot be the same as a register name
#	debug				dumps memory and registers
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
varptr = len(mem) - 1

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

# labels held in dict
labels = {}

# program holds all the instructions of the program
program = []

# number of lines in program, used so halt is not required
loc = 0


## now define functions for all the instructions
# arguments are strings

def pop(a):
	global mem
	global stack
	global reg
	if (a[0] == "["):
		mem[int(a[1:-1])] = stack[reg["rsp"]]
	elif ((a[0] == "r" and isNum(a[1])) or a == "rsp" or a == "rbp" or a == "rax" or a == "PC"):
		reg[a] = stack[reg["rsp"]]
	elif (a in variables):
		mem[int(variables[a])] = stack[reg["rsp"]]
	else:
		print("Error when trying to pop into", a)
		errorTraceback()
	reg["rsp"] -= 1
	return

def push(a):
	global mem
	global stack
	global reg
	if (a[0] == "["):
		stack[reg["rsp"] + 1] = mem[int(a[1:-1])]
	elif ((a[0] == "r" and isNum(a[1])) or a == "rsp" or a == "rbp" or a == "rax" or a == "PC"):
		stack[reg["rsp"] + 1] = reg[a]
	elif (a in variables):
		stack[reg["rsp"] + 1] = mem[int(variables[a])]
	else:
		print("Error when trying to push from", a)
		errorTraceback()
	reg["rsp"] += 1
	return

def add(a, b, c):
	b = getValue(b)
	c = getValue(c)

	assignValue(a, b + c)
	return

def sub(a, b, c):
	b = getValue(b)
	c = getValue(c)

	assignValue(a, b - c)
	return

def xor(a, b, c):
	b = getValue(b)
	c = getValue(c)

	assignValue(a, b ^ c)
	return

def langOr(a, b, c):
	b = getValue(b)
	c = getValue(c)

	assignValue(a, b | c)
	return

def langAnd(a, b, c):
	b = getValue(b)
	c = getValue(c)

	assignValue(a, b & c)
	return

def langNot(a, b):
	b = getValue(b)

	assignValue(a, ~ b)
	return

def shiftr(a, b, c):
	b = getValue(b)
	c = getValue(c)

	assignValue(a, b >> c)
	return

def shiftl(a, b, c):
	b = getValue(b)
	c = getValue(c)

	assignValue(a, b << c)
	return

def nop():
	return

def jmp(a):
	a = getValue(a)
	global reg
	reg["PC"] = a
	return

def jmpe(a, b, c):
	if (getValue(b) == getValue(c)):
		jmp(a)
	return

def jmpl(a, b, c):
	if (getValue(b) < getValue(c)):
		jmp(a)
	return

def jmpg(a, b, c):
	if (getValue(b) > getValue(c)):
		jmp(a)
	return

def inc(a):
	t = getValue(a)

	assignValue(a, t + 1)
	return

def dec(a):
	t = getValue(a)

	assignValue(a, t - 1)
	return

def mov(a, b):
	assignValue(a, getValue(b))
	return

def langPrint(a, b):
	if (getValue(b) == 0):
		print(getValue(a), end="")
	else:
		print(chr(getValue(a)), end="")
	return

def read(a):
	r = input().split()[0]
	if (len(r) == 1):
		if (isNum(r)):
			assignValue(a, int(r))
		else:
			assignValue(a, ord(r))
	elif (r[0:2] == "0d" or r[0:2] == "0x" or r[0:2] == "0b"):
		assignValue(a, getValue(r))
	elif (isNum(r)):
		assignValue(a, int(r))
	return

def halt():
	print("\nExecution reached halt instruction")
	quit()

def call(a):
	push("PC")
	jmp(a)
	return

def ret():
	pop("PC")
	jmp("PC")
	return

def var(name, a):
	global variables
	global varptr
	global mem
	variables[name] = varptr
	mem[varptr] = getValue(a)
	varptr -= 1
	return

def debug():
	dumpMem()
	errorTraceback()
	return







## helper functions

def isNum(n):
	try:
		int(n)
		return True
	except ValueError:
		return False

def getBin(b):
	if (b[0] == "1"):
		x = flip(b[1:])
		x = -1 * int(x, 2)
	else:
		x = int(b[1:], 2)
	return x

def flip(s):
	t = ""
	for i in range(len(s)):
		if (s[i] == "0"):
			t += "1"
		else:
			t += "0"
	return s

def errorTraceback():
	import inspect
	print("Error in", inspect.stack()[1][3])
	for key in reg:
		print(key, "has value", reg[key])
	quit()

def getValue(b):
	global mem
	global reg
	global labels
	global variables


	if (b[0] == "["):
		if (b[1:-1] in variables):
			return variables[b[1:-1]]
		else:
			return mem[getValue(b[1:-1])]

	elif (b[0] == "'"):
		if (b[1:-1] == '\\n'):
			return ord('\n')
		elif (b[1:-1] == '\\t'):
			return ord('\t')
		elif (b[1:-1] == '\\a'):
			return ord('\a')
		elif (b[1:-1] == '\\r'):
			return ord('\r')
		elif (b[1:-1] == '\\f'):
			return ord('\f')
		elif (b[1:-1] == '\\b'):
			return ord('\b')
		elif (b[1:-1] == '\\v'):
			return ord('\v')
		else:
			return ord(b[1])

	elif ((b[0] == "r" and isNum(b[1])) or b == "rsp" or b == "rbp" or b == "rax" or b == "PC"):
		return reg[b]

	elif (b[0:2] == "0d"):
		return int(b[2:])

	elif (b[0:2] == "0x"):
		x = int(b, 16)
		if (x > 0x7FFFFFFF):
			x -= 0x100000000
		return x

	elif (b[0:2] == "0b"):
		return getBin(b[2:])

	elif (isNum(b)):
		return int(b)

	elif (b in labels):
		return int(labels[b])

	elif (b in variables):
		return mem[variables[b]]

	else:
		print("Error when trying to get value of", b)
		errorTraceback()

def assignValue(location, value):
	global mem
	global reg
	global labels
	global variables
	if (location[0] == "["):
		mem[getValue(location[1:-1])] = value

	elif ((location[0] == "r" and isNum(location[1])) or location == "rsp" or location == "rbp" or location == "rax" or location == "PC"):
		reg[location] = value

	elif (location in variables):
		mem[variables[location]] = value

	else:
		print("Error when trying to assign", value, "to", location)
		errorTraceback()

def cleanArgument(s):
	if (s[-1:] == ","):
		return s[:-1]
	else: return s

def dumpMem():
	global mem
	global stack
	global variables
	print("Main memory:", mem)
	print("Stack:", stack)
	print("Variables:", variables)


# dict mapping instruction names to function, must be after function definitions
instructions = {"pop": pop,
				"push": push,
				"add": add,
				"sub": sub,
				"xor": xor,
				"or": langOr,
				"and": langAnd,
				"not": langNot,
				"shiftr": shiftr,
				"shiftl": shiftl,
				"nop": nop,
				"jmp": jmp,
				"jmpe": jmpe,
				"jmpl": jmpl,
				"jmpg": jmpg,
				"inc": inc,
				"dec": dec,
				"mov": mov,
				"print": langPrint,
				"read": read,
				"halt": halt,
				"var": var,
				"debug": debug}

# need sys to open file
import sys

## optionally compile into a python script

if (len(sys.argv) > 2 and sys.argv[1] == "-c"):
	with open(sys.argv[2]) as sourcefile:
		for line in enumerate(sourcefile):
			if (line[1][-2:][0] == ":"):
				labels[line[1][:-2]] = loc
				program.append("nop")
			else:
				program.append(line[1])			
			loc += 1
		sourcefile.close()

	if (len(sys.argv) > 4 and sys.argv[3] == "-o"):
		out = sys.argv[4]
	else:
		out = "out.py"
	with open(out, 'w') as outfile:
		outfile.write("program = [")

		for i in range(len(program)):
			if (i + 1 == len(program)):
				outfile.write("\"{}\"]\n".format(program[i].strip()))

			else:
				outfile.write("\"{}\",\n".format(program[i].strip()))

		outfile.write("loc = {}\n".format(loc))
		outfile.write("labels = {")

		for key in labels:
			outfile.write("\"{}\": {},\n".format(key, labels[key]))

		outfile.write("}\n")

		with open("frame.py", 'r') as framefile:
			for line in enumerate(framefile):
				outfile.write(line[1])
			framefile.close()

		outfile.close()
		quit()



## Do pre execution analysis of file

with open(sys.argv[1]) as sourcefile:
	for line in enumerate(sourcefile):
		if (line[1][-2:][0] == ":"):
			labels[line[1][:-2]] = loc
			program.append("nop")
		else:
			program.append(line[1])			
		loc += 1
	sourcefile.close()

## execute program

while (reg["PC"] < loc):
	executeLine = program[reg["PC"]]
	reg["PC"] += 1
	instruction = executeLine.split()
	if (len(instruction) == 1):
		instructions[instruction[0]]()
	elif (len(instruction) == 2):
		instructions[instruction[0]](cleanArgument(instruction[1]))
	elif (len(instruction) == 3):
		instructions[instruction[0]](cleanArgument(instruction[1]), cleanArgument(instruction[2]))
	elif (len(instruction) == 4):
		instructions[instruction[0]](cleanArgument(instruction[1]), cleanArgument(instruction[2]), cleanArgument(instruction[3]))
	else:
		print("Error trying to execute", reg["PC"] - 1, ":", executeLine)

print("\nExecution Ended")