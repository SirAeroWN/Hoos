# Hoos Assembly language
----------------------
The Hoos assembly language features syntax similar to intel assembly, it runs with a python interpreter. Hoos is turing complete. It has memory restrictions on both the main memory and the stack, these are arbitrary and can easily be increased by editing the interpreter. The number of registers is also arbitrary and can be increased on a whim.

### Interpreter Usage
--------------------
The interpreter can take 1, 2 or 4 arguments. The default is to pass one argument: the filename of the .hoo file to be run.
```
$ python interpreter.py wa.hoo
```

The second option is to pass two arguments which causes the interpreter to compile the .hoo file into a out.py file which can be run with python.
```
$ python interpreter.py -c wa.hoo
$ python out.py
```

The last option is to pass four arguments which causes the interpreter to compile the .hoo file into a file with the name of the last argument
```
$ python interpreter.py -c wa.hoo -o cav.py
$ python cav.py
```

### Language Definition
----------------------
#### Instructions:

|Instruction | Description |
|-------------|---------------|
|`pop a` |				a = stack[rsp]; decrementing rsp is up to program|
|`push a` |				stack[rsp+1] = a; incrementing rsp is up to program|
|`add a, b, c`|			a = b + c|
|`sub a, b, c`	|		a = b - c|
|`xor a, b, c`	|		a = b xor c|
|`or a, b, c`	|		a = b or c|
|`and a, b, c`	|		a = b and c|
|`not a, b`		|	a = not b|
|`shiftr a, b, c` |		a = b shifted c bits right|
|`shiftl a, b, c` |		a = b shifted c bits left|
|`nop`				|	does nothing
|`jmp a` 		|		jump to instruction a|
|`jmpe a, b, c`	|	jump to instruction a if b == c|
|`jmpl a, b, c`	|	jump to instruction a if b < c|
|`jmpg a, b, c`	|	jump to instruction a if b < c|
|`inc a` 		|		a += 1|
|`dec a` 		|		a -= 1|
|`mov a, b` 		|	a = b|
|`print a, b` 	|		if b == 0, prints int value of a, else prints ascii value of a|
|`read a` 		|		reads in single character or entire int|
|`halt`			|	stops execution|
|`call a`		|	pushes `PC` onto stack and jumps to a |
|`ret`			|	pops top of stack into `PC` and jumps to `PC` |
|`var name a` 	|		puts value a into memory, acessable with `nam`, address accessable with `[name]`, name can only be letters and cannot be the same as a register name|
|`debug`			|	dumps memory and registers|
|`label:`		|		label style is "name:"|

#### Arguments
----------------------
Arguments to instructions follow the general pattern `instruction <destination>, <source1>, <source2>`
The destination cannot be a constant value, doing so will result in a runtime error.

#### Constants
----------------------
There are 5 different ways to represent a constant in your code:

|Representation | Type |
|----------------|------|
|`0b1101`		 | Two's compliment binary, must be prefixed with `0b` |
|`0xabad1dea`	 | Two's compliment hex, must be prefixed with `0x` |
|`0d123`		 | Decimal, prefixed with `0d` |
|`123`			 | Decimal, no prefix |
|`'a'`			 | Char, must be within `''` |

#### Registers:
----------------------

| Refister | Description |
|----------|-------------|
|	r0-r15	|			regular registers |
|	rsp		|			stack pointer, supposed to point at top USED slot of stack |
|	rbp		|			base pointer |
|	rax		|			return value for functions, accumulator |
|	PC		|			Program Counter, points to next instruction, that is, what will be executed next, should not be modified directly |

#### Calling Convention
----------------------
`r10`-`r15`used as first 6 parameters, any others must be put on stack.
Any other registers used in function must be backed up and then restored from stack.

#### Memory
----------------------
Main memory is 2^16 slots of python ints.
Stack is 2^8 slots of python ints.
The number labels is not explicitly limited.
The number of variables is limited the the space in mmemory.
