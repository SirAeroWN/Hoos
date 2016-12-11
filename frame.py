mem = [0] * (2**16)
stack = [0] * (2**8)
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
variables = {}

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

def var(name, a):
	global variables
	variables[name] = getValue(a)
	return

def debug():
	dumpMem()
	errorTraceback()
	return

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
		return int(variables[b])

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
		variables[location] = value

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

import sys

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