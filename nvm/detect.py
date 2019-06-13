MOV, PUSH, POP, CALL, GOTO, FETCH, STORE, ADD, SUB, MUL, DIV, STRING, INT, FLOAT, VARIABLE, STD, \
	LOCAL, CLEAN = range(18)

def NvmLexer_TagWord(word):
	switch = {
		word == "mov": MOV,
		word == "push": PUSH,
		word == "call": CALL,
		word == "pop": POP,
		word == "goto": GOTO,
		word == "fetch": FETCH,
		word == "add": ADD,
		word == "sub": SUB,
		word == "div": DIV,
		word == "mul": MUL,
		word == "str": STRING,
		word == "int": INT,
		word == "float": FLOAT,
		word == "var": VARIABLE,
		word == "std": STD,
		word == "local": LOCAL,
		word == "clean": CLEAN
	}
	if switch.get(True) == None:
		return word
	return switch.get(True)